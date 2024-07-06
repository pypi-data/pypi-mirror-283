import contextlib
from typing import Iterator, Literal

from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..db import BaseDatabaseSessionManager


class SyncDatabaseSessionManager(BaseDatabaseSessionManager):
    _engine: Engine | None = None
    _sessionmaker: sessionmaker[Session] | None = None
    _engine_dict: dict[str, Engine] = {}
    _sessionmaker_dict: dict[str, sessionmaker[Session]] = {}

    def init_db(self, url: str, binds: dict[str, str] | None = None):
        """
        Initialize the database connection and session makers.

        Args:
            url (str): The URL of the main database.
            binds (dict[str, str] | None, optional): A dictionary of additional database URLs to bind. Defaults to None.
        """
        self._engine = create_engine(url)
        self._sessionmaker = sessionmaker(
            self._engine,
            class_=Session,
            autocommit=False,
        )

        if binds:
            self._engine_dict = {}
            self._sessionmaker_dict = {}
            for key, value in binds.items():
                self._engine_dict[key] = create_engine(value)
                self._sessionmaker_dict[key] = sessionmaker(
                    self._engine_dict[key],
                    class_=Session,
                    autocommit=False,
                )

    def close(self):
        """
        Closes the database connection and disposes the engine.

        Raises:
            Exception: If the database engine is not initialized.
        """
        if not self._engine:
            raise Exception("Database engine is not initialized")
        self._engine.dispose()
        self._engine = None
        self._async_sessionmaker = None

        if self._engine_dict:
            for engine in self._engine_dict.values():
                engine.dispose()
            self._engine_dict = None
            self._async_sessionmaker_dict = None

    @contextlib.contextmanager
    def connect(self, bind: str | None = None) -> Iterator[Connection]:
        """
        Establishes a connection to the database.

        Args:
            bind (str, optional): The database URL to bind to. If none, the default database is used. Defaults to None.

        Raises:
            Exception: If the DatabaseSessionManager is not initialized.

        Yields:
            Connection: The database connection.

        Returns:
            None
        """
        if bind:
            if self._engine_dict is None:
                raise Exception("DatabaseSessionManager is not initialized")
            with self._engine_dict[bind].begin() as connection:
                try:
                    yield connection
                except Exception:
                    connection.rollback()
                    raise
        else:
            if self._engine is None:
                raise Exception("DatabaseSessionManager is not initialized")
            with self._engine.begin() as connection:
                try:
                    yield connection
                except Exception:
                    connection.rollback()
                    raise

    @contextlib.contextmanager
    def session(self, bind: str | None = None) -> Iterator[Session]:
        """
        Provides a database session for performing database operations.

        Args:
            bind (str, optional): The database URL to bind to. If none, the default database is used. Defaults to None.

        Raises:
            Exception: If the DatabaseSessionManager is not initialized.

        Yields:
            Session: The database session.

        Returns:
            None
        """
        if bind:
            if self._sessionmaker_dict is None:
                raise Exception("DatabaseSessionManager is not initialized")
            session = self._sessionmaker_dict[bind]()
            try:
                yield session
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            if self._sessionmaker is None:
                raise Exception("DatabaseSessionManager is not initialized")
            session = self._sessionmaker()
            try:
                yield session
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

    def create_all(self, binds: list[str] | None | Literal["all"] = "all"):
        raise NotImplementedError(
            "For now, create_all is not implemented in the sync version of the database session manager"
        )

    def drop_all(self, binds: list[str] | None | Literal["all"] = "all"):
        raise NotImplementedError(
            "For now, drop_all is not implemented in the sync version of the database session manager"
        )


sync_db = SyncDatabaseSessionManager()
