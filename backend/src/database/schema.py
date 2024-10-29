from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    surname: str
    email: str = Field(unique=True)
    user_level: str = Field(index=True, nullable=False)
    password: str = Field(nullable=False)


class Counter(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    endpoint_name: str = Field(index=True)
    count: int = Field(default=0)
