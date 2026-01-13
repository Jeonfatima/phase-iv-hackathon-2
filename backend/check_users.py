from sqlmodel import Session, select
from database.engine import engine
from models import User  # ← import your User model (from models/user.py or wherever it is)

with Session(engine) as session:
    statement = select(User)
    users = session.exec(statement).all()
    
    if not users:
        print("No users in database!")
    else:
        print("Users in database:")
        for user in users:
            print(f"ID: {user.id} | Email: {user.email} | Hashed PW: {user.hashed_password}")
            # If you have username: print(f"Username: {user.username}")