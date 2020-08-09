from tartiflette_request_context_hooks import BaseRequestContextHooks


class SQLAlchemyRequestContextHooks(BaseRequestContextHooks):
    label = 'SA'

    def __init__(self, *, db_manager):
        BaseRequestContextHooks.__init__(self)
        self.db_manager = db_manager

    async def __aenter__(self):
        session = self.db_manager.get_scoped_session()
        await self.store_request_data(session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        session = await self.get_request_data()
        session.remove()
