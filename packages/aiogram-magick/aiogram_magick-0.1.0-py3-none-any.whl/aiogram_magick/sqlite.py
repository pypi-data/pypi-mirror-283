"""SQLite-based storage with caching & automatic commits for Aiogram 3.x."""

from dataclasses import dataclass, field
from sqlite3 import PARSE_DECLTYPES, OperationalError
from time import time
from traceback import print_exception
from typing import TYPE_CHECKING

import aiosqlite
import jsonpickle
from aiogram.fsm.storage.base import BaseStorage, StorageKey

if TYPE_CHECKING:
    from typing import Dict, List, Union

    from aiogram.fsm.storage.base import StateType


@dataclass(slots=True)
class SqliteStorageCache:
    """SQLite cache dataclass."""

    cache: 'List[Union[StateType, Dict[str]]]' = field(default_factory=list)
    # NOTE: Python `list`s are already optimized to hash each item.
    # I believe there won't be any performance improvement if we call to hash() ourselves.
    keys: 'List[StorageKey]' = field(default_factory=list)
    length: int = 0
    capacity: int = field(default=10, compare=False, kw_only=True)

    def get(self, key: StorageKey) -> 'Union[StateType, Dict[str], None]':
        """Get the cache entry of `key` if it exists.

        Args:
            key (StorageKey): Cache key.

        Returns:
            Union[StateType, Dict[str], None]: State, data or `None`
        """
        key_i = self.keys.index(key)
        self.keys.insert(0, self.keys.pop(key_i))
        self.cache.insert(0, self.cache.pop(key_i))
        return self.cache[0]

    def add(self, key: StorageKey, value: 'Union[StateType, Dict[str]]'):
        """Add a new cache entry of `key`.

        Args:
            key (StorageKey): Cache key.
            value (Union[StateType, Dict[str]]): Value
        """
        if self.length == self.capacity:
            self.keys.pop()
            self.cache.pop()
        else:
            self.length += 1

        self.keys.insert(0, key)
        self.cache.insert(0, value)

    def update(self, key: StorageKey, value: 'Union[StateType, Dict[str]]'):
        """Update the value for the cache entry of `key`.

        Args:
            key (StorageKey): Cache key.
            value (Union[StateType, Dict[str]]): New value
        """
        key_i = self.keys.index(key)
        self.keys.insert(0, self.keys.pop(key_i))
        self.cache.insert(0, self.cache.pop(key_i))
        self.cache[0] = value


class SqliteStorage(BaseStorage):
    """SQLite FSM storage."""

    def __init__(self, filepath: str, idle_to_commit: int = 1800):
        """Initalize a SQLite-based storage.

        Args:
            filepath (str): Path to the database file
            idle_to_commit (int): Frequency of idling to commit changes (in seconds). It it notable
                to mention that regardless of this value all changes will be saved anyway when
                `self.close()` is called. Defaults to `1800`.
        """
        self.filepath = filepath
        self.idle_to_commit = idle_to_commit

        self.__last_commit_ts = 0
        self.__commit: Dict[StorageKey, Dict[str, Union[StateType, Dict[str]]]] = {}

        self.__cache_state = SqliteStorageCache(capacity=20)
        self.__cache_data = SqliteStorageCache()

        self.__conn: Union[aiosqlite.Connection, None] = None

    @staticmethod
    def __key_to_sqlite(key: StorageKey) -> str:
        return f'{key.bot_id}:{key.chat_id}:{key.user_id}'

    @staticmethod
    def __sqlite_to_key(value: str) -> StorageKey:
        parts = value.split(':')
        return StorageKey(bot_id=int(parts[0]), chat_id=int(parts[1]), user_id=int(parts[2]))

    async def __connect(self):
        if self.__conn:
            return

        aiosqlite.register_adapter(StorageKey, self.__key_to_sqlite)
        aiosqlite.register_converter('StorageKey', self.__sqlite_to_key)

        # NOTE: Can an aiosqlite connection be handled in a thread-safe way?
        self.__conn = await aiosqlite.connect(
            self.filepath, check_same_thread=False, detect_types=PARSE_DECLTYPES
        )
        self.__conn.isolation_level = None  # TODO: (Python 3.12 needed) Use .autocommit instead
        await self.__conn.executescript(
            'CREATE TABLE IF NOT EXISTS "aiogram_states"('
            '"Key"     StorageKey NOT NULL UNIQUE,'
            '"State"   VARCHAR(100) DEFAULT NULL,'
            '"Data"    TEXT,'
            'PRIMARY KEY("Key")'
            ');'
            'CREATE UNIQUE INDEX IF NOT EXISTS "aiogram_states_keys" ON '
            '"aiogram_states" ("Key");'
        )
        await self.__conn.commit()

    async def _commit(self, *, force: bool = False):
        if force or (int(time()) - self.__last_commit_ts) > self.idle_to_commit:
            await self.__connect()
            cursor = await self.__conn.cursor()

            await cursor.execute('BEGIN')
            try:
                for key, changes in self.__commit.items():  # Not thread-safe
                    is_state_changed = 'state' in changes
                    is_data_changed = 'data' in changes

                    if is_state_changed and is_data_changed:
                        await cursor.execute(
                            (
                                'INSERT INTO aiogram_states (Key, State, Data) VALUES (?, ?, ?)'
                                'ON CONFLICT(Key) DO UPDATE '
                                'SET State=excluded.State,Data=excluded.Data;'
                            ),
                            (
                                key,
                                changes['state'],
                                jsonpickle.encode(changes['data']),
                            ),
                        )
                    elif is_state_changed:
                        await cursor.execute(
                            (
                                'INSERT INTO aiogram_states (Key, State) VALUES (?, ?)'
                                'ON CONFLICT(Key) DO UPDATE SET State=excluded.State;'
                            ),
                            (key, changes['state']),
                        )
                    else:
                        await cursor.execute(
                            (
                                'INSERT INTO aiogram_states (Key, Data) VALUES (?, ?)'
                                'ON CONFLICT(Key) DO UPDATE SET Data=excluded.Data;'
                            ),
                            (key, jsonpickle.encode(changes['data'])),
                        )
                await cursor.execute('COMMIT')
            except OperationalError as exc:
                await cursor.execute('ROLLBACK')
                if not force:
                    raise
                print_exception(exc)

            self.__last_commit_ts = int(time())
