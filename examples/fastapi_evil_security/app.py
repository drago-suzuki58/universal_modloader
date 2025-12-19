import secrets
from collections.abc import Generator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlmodel import Session, SQLModel, create_engine, select

from models import (
    AuthResponse,
    User,
    UserCreate,
    UserLogin,
    UserRead,
    UserUpdate,
)

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
MAX_BCRYPT_BYTES = 72

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_auth = HTTPBearer(auto_error=False)
active_tokens: dict[str, int] = {}


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Secure FastAPI User Service", lifespan=lifespan)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_user_or_404(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


def to_user_read(user: User) -> UserRead:
    return UserRead.model_validate(user)


def ensure_password_length(password: str) -> None:
    if len(password.encode("utf-8")) > MAX_BCRYPT_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be 72 bytes or fewer when UTF-8 encoded.",
        )


def hash_password(raw_password: str) -> str:
    ensure_password_length(raw_password)
    try:
        return pwd_context.hash(raw_password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


def require_active_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(token_auth),
    ],
) -> tuple[int, str]:
    if (
        credentials is None
        or credentials.scheme.lower() != "bearer"
        or credentials.credentials not in active_tokens
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Valid bearer token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = active_tokens[credentials.credentials]
    return user_id, credentials.credentials


AuthDep = Annotated[tuple[int, str], Depends(require_active_token)]


@app.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
def create_user(user_in: UserCreate, session: SessionDep) -> UserRead:
    statement = select(User).where(User.email == user_in.email)
    if session.exec(statement).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        is_active=user_in.is_active,
        hashed_password=hash_password(user_in.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return to_user_read(user)


@app.get("/users", response_model=list[UserRead], tags=["users"])
def list_users(
    session: SessionDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[UserRead]:
    statement = select(User).offset(offset).limit(limit)
    users = session.exec(statement).all()
    return [to_user_read(user) for user in users]


@app.get("/users/{user_id}", response_model=UserRead, tags=["users"])
def read_user(user_id: int, session: SessionDep) -> UserRead:
    return to_user_read(get_user_or_404(user_id, session))


@app.patch("/users/{user_id}", response_model=UserRead, tags=["users"])
def update_user(
    user_id: int,
    user_in: UserUpdate,
    session: SessionDep,
    auth: AuthDep,
) -> UserRead:
    current_user_id, _ = auth
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You may only update your own user record.",
        )

    user = get_user_or_404(user_id, session)
    updates = user_in.model_dump(exclude_unset=True)

    if "email" in updates:
        statement = select(User).where(User.email == updates["email"])
        existing = session.exec(statement).first()
        if existing and existing.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered by another user.",
            )

    if "password" in updates:
        user.hashed_password = hash_password(updates.pop("password"))

    for field, value in updates.items():
        setattr(user, field, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return to_user_read(user)


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"],
)
def delete_user(user_id: int, session: SessionDep, auth: AuthDep) -> None:
    current_user_id, _ = auth
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You may only delete your own user record.",
        )

    user = get_user_or_404(user_id, session)
    session.delete(user)
    session.commit()


@app.post("/auth/login", response_model=AuthResponse, tags=["auth"])
def login(credentials: UserLogin, session: SessionDep) -> AuthResponse:
    statement = select(User).where(User.email == credentials.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    ensure_password_length(credentials.password)
    try:
        password_ok = pwd_context.verify(
            credentials.password,
            user.hashed_password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if not password_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User ID is missing and cannot issue token.",
        )

    user_id = user.id
    token = secrets.token_urlsafe(32)
    active_tokens[token] = user_id
    return AuthResponse(access_token=token)


@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT, tags=["auth"])
def logout(auth: AuthDep) -> None:
    _, token = auth
    active_tokens.pop(token, None)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
