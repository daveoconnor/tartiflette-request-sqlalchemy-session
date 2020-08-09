from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Database:
    _conn_string = None
    _connection = None
    _engine = None
    _session_factory = None
    _session = None

    def __init__(self, *, db, engine, **kwargs):
        if not self._conn_string:
            self._conn_string = self._form_connection_string(
                db,
                engine,
                **kwargs,
            )

        if not self._engine:
            self._engine = create_engine(self._conn_string)

        if not self._connection:
            self._connection = self._engine.connect()

        if not self._session_factory:
            self._session_factory = sessionmaker(bind=self._engine)

    @staticmethod
    def _form_connection_string(db, engine, user=None, password=None,
                                host=None, port=None):
        conn_str = f'{engine}://'
        if user and password:
            conn_str += f'{user}:{password}'
        if host:
            conn_str += f'@{host}'
        if port:
            conn_str += f':{port}'
        conn_str += f'/{db}'
        return conn_str

    def get_scoped_session(self):
        return scoped_session(self._session_factory)

    @property
    def connection_string(self):
        return self._conn_string

    @property
    def connection(self):
        return self._connection

    @property
    def engine(self):
        return self._engine
