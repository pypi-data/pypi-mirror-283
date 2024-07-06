import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_rtk import FastapiReactToolkit, User, session_manager
from fastapi_rtk.manager import UserManager

from .base_data import add_base_data

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.INFO)


class CustomUserManager(UserManager):
    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        await super().on_after_login(user, request, response)
        print("User logged in: ", user)

    pass


toolkit = FastapiReactToolkit(
    config_file="./app/config.py",
    auth={
        "user_manager": CustomUserManager,
        # "password_helper": FABPasswordHelper(),  #! Add this line to use old password hash
    },
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run when the app is starting up
    toolkit.connect_to_database()

    # Not needed if you setup a migration system like Alembic
    await session_manager.create_all()

    # Creating permission, apis, roles, and connecting them
    await toolkit.init_database()

    # Add base data
    await add_base_data()

    yield

    # Run when the app is shutting down
    if session_manager._engine:
        await session_manager.close()


app = FastAPI(lifespan=lifespan, docs_url="/openapi/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:6006"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
toolkit.initialize(app)


from .apis import *

toolkit.mount()
