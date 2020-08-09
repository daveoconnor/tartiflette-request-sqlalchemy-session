import pytest
from unittest.mock import Mock
from tartiflette_request_sa_session import SQLAlchemyRequestContextHooks


class TestRequestContextHooks:
    def test_init(self):
        db_manager = Mock()
        hook = SQLAlchemyRequestContextHooks(db_manager=db_manager)
        assert hook.db_manager is db_manager
        assert hook.label == 'SA'

    @pytest.mark.asyncio
    async def test_context(self):
        db_manager = Mock()
        session_mock = Mock()
        db_manager.get_scoped_session = Mock(return_value=session_mock)
        hook = SQLAlchemyRequestContextHooks(db_manager=db_manager)
        hook.request = {}
        async with hook:
            assert await hook.get_request_data() == session_mock
            db_manager.get_scoped_session.assert_called()
        # testing exited values here
        session_mock.remove.assert_called()

