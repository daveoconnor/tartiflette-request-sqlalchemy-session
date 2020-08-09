import sqlalchemy
from tartiflette_request_sa_session import Database


def sqlite_credentials():
    return {
        'db': ':memory:',
        'engine': 'sqlite',
    }


def fake_credentials():
    return {
        'db': 'fake_db',
        'engine': 'nengine',
        'host': 'fake_host',
        'password': 'fake_pass',
        'port': '11',
        'user': 'fake_user'
    }


class TestDatabase:
    def test_init(self):
        db = Database(**sqlite_credentials())
        assert 'sqlite:///:memory:' == db._conn_string
        assert isinstance(db._engine, sqlalchemy.engine.base.Engine)
        assert isinstance(db._connection, sqlalchemy.engine.base.Connection)
        assert isinstance(db._session_factory,
                          sqlalchemy.orm.session.sessionmaker)

    def test_form_connection_string(self):
        assert 'nengine://fake_user:fake_pass@fake_host:11/fake_db' == \
            Database._form_connection_string(**fake_credentials())

    def test_properties(self):
        db = Database(**sqlite_credentials())
        assert db.connection_string == 'sqlite:///:memory:'
        assert isinstance(db.engine, sqlalchemy.engine.base.Engine)
        assert isinstance(db.connection, sqlalchemy.engine.base.Connection)

    def test_get_scoped_session(self):
        db = Database(**sqlite_credentials())
        scoped_sess1 = db.get_scoped_session()
        assert isinstance(scoped_sess1, sqlalchemy.orm.scoping.scoped_session)
        sess_factory_id = id(db._session_factory)
        scoped_sess2 = db.get_scoped_session()
        assert isinstance(scoped_sess2, sqlalchemy.orm.scoping.scoped_session)
        # check the session factory is reused
        assert id(db._session_factory) == sess_factory_id
        # check for uniqueness in the scoped sessions
        assert id(scoped_sess1) != id(scoped_sess2)
