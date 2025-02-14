from sqlmodel import SQLModel, Field
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    name: str = Field(default=None)
    password: str
    active: bool