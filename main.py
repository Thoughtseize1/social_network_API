from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends
from src.users.users import auth_backend, fastapi_users, current_active_user
from src.users.schemas import UserRead, UserCreate
from src.database.models import User
from src.posts.router import posts_router


app = FastAPI()


app.include_router(posts_router, prefix="/api")

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/")
def read_root():
    """
    Get the root endpoint.

    Returns:
        dict: A dictionary with a single key "message" and the value "Hello World".
"""
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", reload=True, log_level="info", port=8000)
