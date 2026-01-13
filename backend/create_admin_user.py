from sqlmodel import SQLModel, Session, select
from database.engine import engine
from models.user import User
import hashlib
import secrets
from datetime import datetime

def create_admin_user():
    # Create tables if they don't exist
    SQLModel.metadata.create_all(bind=engine)

    # Admin user details
    email = "fati.salman31@gmail.com"
    username = "fatima"
    password = "1111"  # Plain text password

    # Hash the password using the same method as in auth.py
    salt = secrets.token_hex(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000)
    hashed_password_hex = hashed_password.hex()
    final_hashed_password = f"{hashed_password_hex}:{salt}"

    # Create a new session
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == email)).first()

        if existing_user:
            print(f"User with email {email} already exists!")
            print(f"User ID: {existing_user.id}")
            return

        # Create new user
        user = User(
            email=email,
            username=username,
            hashed_password=final_hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"Admin user created successfully with ID: {user.id}")

if __name__ == "__main__":
    create_admin_user()