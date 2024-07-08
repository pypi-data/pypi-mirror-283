import aiosqlite
import pickle
from asyncio import Lock
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from typing import Any

class SQLiteStorage(BaseStorage):
    """
    Async SQLite storage for aiogram bots.
    Based on https://gist.github.com/KurimuzonAkuma/683eec4d62e111578a42608d4485fc27
    """
    
    __user_data_table = 'user_data'
    __user_states_table = 'user_states'

    def __init__(self, path: str = 'user-states.db'):
        self.__path = path
        self.__connection = None
        self.__cursor = None
        
        self.__lock = Lock()

    async def set_state(self, key: StorageKey, state: StateType):
        _state = state.state if isinstance(state, State) else state
        
        if _state is None:
            await self.__delete_user(self.__user_states_table, key.user_id, key.chat_id)
        
        else: 
            await self.__execute(f"""
                                INSERT INTO {self.__user_states_table}
                                (chatID, userID, state)
                                VALUES (?, ?, ?)
                                ON CONFLICT(chatID, userID) DO UPDATE SET 'state' = ?;
                                """,
                                values = (key.chat_id, key.user_id, _state, _state),
                                commit = True)
    
    async def get_state(self, key: StorageKey) -> str | None:
        await self.__execute(f"""
                            SELECT * FROM {self.__user_states_table} 
                            WHERE chatID = ? AND userID = ?;
                             """,
                            values = (key.chat_id, key.user_id))
        
        user = await self.__cursor.fetchone() # tuple that contains only 'state' column
        return user[0] if user else None

    async def set_data(self, key: StorageKey, data: dict[str, Any]):
        if not data:
            await self.__delete_user(self.__user_data_table, key.user_id, key.chat_id)

        else:
            serialized = pickle.dumps(data)
            await self.__execute(f"""
                                INSERT INTO {self.__user_data_table} 
                                (chatID, userID, data) 
                                VALUES (?, ?, ?) 
                                ON CONFLICT(chatID, userID) DO UPDATE SET 'data' = ?;
                                """,
                                values = (key.chat_id, key.user_id, serialized, serialized),
                                commit = True)
    
    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        await self.__execute(f"""
                            SELECT data FROM {self.__user_data_table} 
                            WHERE chatID = ? AND userID = ?;
                            """,
                            values = (key.chat_id, key.user_id))
        
        user = await self.__cursor.fetchone() # tuple that contains only 'data' column
        return pickle.loads(user[0]) if user else {}

    async def close(self):
        if self.__connected_to_database():
            await self.__cursor.close()
            await self.__connection.close()

    async def __execute(self, query: str, values: tuple = None, commit: bool = False):
        async with self.__lock:
            if self.__connected_to_database() != True:
                await self.__prepare_database()

            await self.__cursor.execute(query, values)

            if commit:
                await self.__connection.commit()


    async def __delete_user(self, table: str, user_id: int, chat_id: int):
        await self.__execute(f'DELETE FROM {table} WHERE chatID = ? AND userID = ?;',
                              values = (chat_id, user_id), 
                              commit = True)

    async def __prepare_database(self):
        self.__connection = await aiosqlite.connect(self.__path)
        self.__cursor = await self.__connection.cursor()

        await self.__create_tables()

    async def __create_tables(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS {}(
        chatID BIGINT NOT NULL,
        userID BIGINT NOT NULL,
        {},
        PRIMARY KEY (chatID, userID)
        );"""

        await self.__cursor.execute(create_query.format(self.__user_data_table, 'data BLOB'))
        await self.__cursor.execute(create_query.format(self.__user_states_table, 'state TEXT'))

    def __connected_to_database(self) -> bool:
        return self.__connection is not None
    
