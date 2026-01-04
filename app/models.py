from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# Shared properties
class UserBase(SQLModel):
    username: str = Field(index=True)
    email: Optional[str] = None

# Database model
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    tasks: List["Task"] = Relationship(back_populates="owner")

# Shared properties
class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = None
    is_completed: bool = False

# Database model
class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="tasks")

# Properties for creation
class UserCreate(UserBase):
    password: str

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
