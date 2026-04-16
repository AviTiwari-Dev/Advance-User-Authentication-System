"""

"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import endpoints, models
from .bases.user_management import UserManagementBase
from .config.env_variables import environment_variables
from .engines.user_management import user_management_engine
from .routers.user_profile import user_profile_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    
    """
    async with user_management_engine.begin() as connection:
        await connection.run_sync(UserManagementBase.metadata.create_all)
    yield


api = FastAPI(
    title="User Management",
    version="0.1",
    description="User management project.",
    summary="""User management with FastAPI, SQLAlchemy, PostgreSQL and Asyncpg, all with async programming""",
    deprecated=False,
    debug=environment_variables.DEBUG,
    include_in_schema=True,
    lifespan=lifespan,
    docs_url="/documentation/Swagger",
    redoc_url="/documentation/ReDoc",
    openapi_url="/documentation/openapi.json",
    contact={
        "name": "Avi Tiwari",
        "email": "avi_tiwari@example.com",
    },
    license_info={
        "name": "MIT Licence",
        "identifier": "MIT",
    },
)

api.include_router(user_profile_router)
