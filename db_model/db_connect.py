import os
from typing import Iterator
from contextlib import contextmanager
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, Session


# Load environment variables from .env file
load_dotenv()


class PostgresSqlConnect(object):
    def __init__(self, user: str, password: str, host: str, port: str, database: str):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.engine = None
        self._session_local = None

    def connect(self):
        if not self.engine:
            self.engine = create_engine(
                f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
            self._session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # print(f"Connected to database: [{self.database}] at [{self.host}:{self.port}] as user [{self.user}]")
    
    
    @contextmanager
    def get_session(self) -> Iterator[Session]:
        """
        Session 生產器。
        使用 with 語法時會自動打開 Session，離開 with 時會自動 close！
        """
        if not self.engine:
            self.connect()
            
        session = self._session_local()
        
        try:
            yield session  
            session.commit()
            # print(f"[Session] Committed successfully.")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            # print("[Session] Closed safely.")
            
    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None
    
    def __enter__(self) -> "PostgresSqlConnect":
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            self.disconnect()
            # print(f"Disconnected from database: [{self.database}] at [{self.host}:{self.port}] as user [{self.user}]\n")



login_db_connect = PostgresSqlConnect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    database=os.getenv("POSTGRES_DATABASE"),
)


@contextmanager
def db_session() -> Iterator[Session]:
    with login_db_connect.get_session() as session:
        yield session