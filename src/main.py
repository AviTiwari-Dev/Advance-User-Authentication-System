"""

"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config.env_variables import environment_variables


@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    
    """
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
        "email": "avi_tiwari@hotmail.com",
    },
    license_info={
        "name": "MIT Licence",
        "identifier": "MIT",
    },
)
