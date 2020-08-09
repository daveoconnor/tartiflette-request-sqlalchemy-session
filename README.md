# Tartiflette Request SQLAlchemy Session

Middleware for the [tartiflette](https://tartiflette.io/) GraphQL
server implementation to have a SQLAlchemy Session generated on each server
request which is then injected into the resolver context.

1. A provided session is unique to the request.
1. A provided session is shared across queries on a request. 
1. Must work for queries, mutations, and subscriptions.

## Installation

```bash
pip install tartiflette-request-sqlalchemy-session
```

## Configuration

Note: If you have a working project you won't need to change the Alembic 
configuration. This is mainly useful for a new project.

### Alembic configuration

In ```env.py``` add:

```python
from tartiflette_request_sa_session import Database

db_config = Database(
    db='db_name',
    engine='db_engine', # e.g. postgres+psycopg2
    host='db_host',
    password='db_password',
    port='db_port',
    user='db_username',
)
database = Database(**db_config)
```

Update ```env.py``` to use:

```python
config = context.config
config.set_main_option('sqlalchemy.url', database.connection_string)
```

### App.py configuration

This configuration will not usually provide an out of the box working example
of a tartiflette aiohttp setup. This should be used as guidance to fit into
your configuration.

```python
from tartiflette_request_context_hooks.middleware.aiohttp import\
    get_hooks_service_middleware
from tartiflette_request_sa_session import Database,\
    SQLAlchemyRequestContextHooks

def run():
    # As with Alembic add:
    db_config = Database(
        db='db_name',
        engine='db_engine', # e.g. postgres+psycopg2
        host='db_host',
        password='db_password',
        port='db_port',
        user='db_username',
    )

    # database request-based middleware setup
    sa_request_context_service = SQLAlchemyRequestContextHooks(
        db_manager=Database(**db_config)
    )
    sa_request_session_middleware = get_hooks_service_middleware(
        context_service=sa_request_context_service
    )

    # configure app - tweak to fit own configuration
    app = web.Application(middlewares=[
        sa_request_session_middleware,
    ])
    engine = create_engine(
        sdl=os.path.dirname(os.path.abspath(__file__)) + '/sdl',
        modules=[
            # configure as necessary
        ],
    )

    ctx = {
        'db_session_service': sa_request_context_service,
    }
    web.run_app(
        register_graphql_handlers(
            # ... your other settings ...
            executor_context=ctx,
        )
    )
```

## Use

In your resolver you can now access a new session for each request.

Resolver example: ```query_resolvers.py```

```python
async def resolve_new_request(parent, args, ctx, info):
    session = await ctx['db_session_service']()
    u = session.query(YourModel).filter_by(uuid=args['uuid']).first()
    return u
```

# Notes

1. Currently works using "Tartiflette Request Context Hooks" for middleware
handling which only supports aiohttp. Other servers supporting tartiflette
could be supported via pull requests on that project.
