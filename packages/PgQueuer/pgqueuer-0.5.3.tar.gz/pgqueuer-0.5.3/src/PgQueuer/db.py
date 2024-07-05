"""Database Abstraction Layer for PgQueuer.

This module provides database driver abstractions and a specific implementation
for AsyncPG to handle database operations asynchronously.
"""

from __future__ import annotations

import asyncio
import functools
import os
import re
from typing import TYPE_CHECKING, Any, Callable, Protocol

from PgQueuer.logconfig import logger
from PgQueuer.tm import TaskManager

if TYPE_CHECKING:
    import asyncpg
    import psycopg


def dsn(
    host: str = "",
    user: str = "",
    password: str = "",
    database: str = "",
    port: str = "",
) -> str:
    host = os.getenv("PGHOST", host or "localhost")
    user = os.getenv("PGUSER", user or "testuser")
    password = os.getenv("PGPASSWORD", password or "testpassword")
    database = os.getenv("PGDATABASE", database or "testdb")
    port = os.getenv("PGPORT", port or "5432")
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


class Driver(Protocol):
    """
    Defines a protocol for database drivers with essential database operations.
    """

    async def fetch(
        self,
        query: str,
        *args: Any,
    ) -> list[dict]:
        """Fetch multiple records from the database."""
        raise NotImplementedError

    async def execute(
        self,
        query: str,
        *args: Any,
    ) -> str:
        """Execute a single query and return a status message."""
        raise NotImplementedError

    async def add_listener(
        self,
        channel: str,
        callback: Callable[[str | bytes | bytearray], None],
    ) -> None:
        """Add a listener for a specific PostgreSQL NOTIFY channel."""
        raise NotImplementedError

    async def fetchval(
        self,
        query: str,
        *args: Any,
    ) -> Any:
        """Fetch a single value from the database."""
        raise NotImplementedError


class AsyncpgDriver(Driver):
    """
    Implements the Driver protocol using AsyncPG for PostgreSQL database operations.
    """

    def __init__(
        self,
        connection: asyncpg.Connection,
    ) -> None:
        """Initialize the driver with an AsyncPG connection."""
        self.lock = asyncio.Lock()
        self.connection = connection

    async def fetch(
        self,
        query: str,
        *args: Any,
    ) -> list[dict]:
        """Fetch records with query locking to ensure thread safety."""
        async with self.lock:
            return [dict(x) for x in await self.connection.fetch(query, *args)]

    async def execute(
        self,
        query: str,
        *args: Any,
    ) -> str:
        """Execute a query with locking to avoid concurrent access issues."""
        async with self.lock:
            return await self.connection.execute(query, *args)

    async def fetchval(
        self,
        query: str,
        *args: Any,
    ) -> Any:
        """Fetch a single value with concurrency protection."""
        async with self.lock:
            return await self.connection.fetchval(query, *args)

    async def add_listener(
        self,
        channel: str,
        callback: Callable[[str | bytes | bytearray], None],
    ) -> None:
        """Add a database listener with locking to manage concurrency."""
        async with self.lock:
            await self.connection.add_listener(
                channel,
                lambda *x: callback(x[-1]),
            )


@functools.cache
def _replace_dollar_named_parameter(query: str) -> str:
    """
    Replaces all instances of $1, $2, etc. with %(parameter_1)s in a
    given SQL query string.
    """
    return re.sub(r"\$(\d+)", r"%(parameter_\1)s", query)


def _named_parameter(args: tuple) -> dict[str, Any]:
    return {f"parameter_{n}": arg for n, arg in enumerate(args, start=1)}


class PsycopgDriver:
    def __init__(self, connection: psycopg.AsyncConnection) -> None:
        self.lock = asyncio.Lock()
        self.connection = connection
        self.tm = TaskManager()

    async def fetch(
        self,
        query: str,
        *args: Any,
    ) -> list[dict]:
        async with self.lock:
            cursor = await self.connection.execute(
                _replace_dollar_named_parameter(query),
                _named_parameter(args),
            )
            cols = (
                [col.name for col in description]
                if (description := cursor.description)
                else []
            )
            return [dict(zip(cols, val)) for val in await cursor.fetchall()]

    async def execute(
        self,
        query: str,
        *args: Any,
    ) -> str:
        async with self.lock:
            return (
                await self.connection.execute(
                    _replace_dollar_named_parameter(query),
                    _named_parameter(args),
                )
            ).statusmessage or ""

    async def fetchval(
        self,
        query: str,
        *args: Any,
    ) -> Any:
        async with self.lock:
            cursor = await self.connection.execute(
                _replace_dollar_named_parameter(query),
                _named_parameter(args),
            )
            result = await cursor.fetchone()
            return result[0] if result else None

    async def add_listener(
        self,
        channel: str,
        callback: Callable[[str | bytes | bytearray], None],
    ) -> None:
        assert self.connection.autocommit

        async def notify_handler_wrapper(
            channel: str,
            callback: Callable[[str | bytes | bytearray], None],
        ) -> None:
            await self.execute(f"LISTEN {channel};")

            async for note in self.connection.notifies():
                if note.channel == channel:
                    callback(note.payload)

        def log_exception(x: asyncio.Task) -> None:
            try:
                x.result()
            except asyncio.exceptions.CancelledError:
                ...
            except Exception:
                logger.exception(
                    "Got an exception on notify on channel: %s",
                    channel,
                )

        task = asyncio.create_task(
            notify_handler_wrapper(channel, callback),
            name=f"notify_handler_wrapper_{channel}",
        )
        task.add_done_callback(log_exception)
        self.tm.add(task)
