import sys
from sqlmodel import SQLModel, create_engine
from passlib.context import CryptContext

try:
    print("Checking imports...")
    from app.models import User, Task
    from app.db import engine
    print("Imports success.")

    print("Checking DB creation...")
    SQLModel.metadata.create_all(engine)
    print("DB creation success.")

    print("Checking Password Hashing...")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hash = pwd_context.hash("test")
    print(f"Hashing success: {hash}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
