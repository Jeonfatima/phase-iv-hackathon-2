from sqlmodel import SQLModel, Session, select
from database.engine import engine
from models.user import User
import hashlib
import secrets

def test_login():
    # Test credentials
    email = "fati.salman31@gmail.com"
    password = "1111"

    # Create a new session
    with Session(engine) as session:
        # Find user by email
        db_user = session.exec(select(User).where(User.email == email)).first()

        if not db_user:
            print(f"No user found with email: {email}")
            return False

        print(f"User found: ID={db_user.id}, Email={db_user.email}")

        # Verify password using the same method as in auth.py
        stored_hash, salt = db_user.hashed_password.split(':')
        computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000).hex()

        print(f"Stored hash: {stored_hash}")
        print(f"Computed hash: {computed_hash}")
        print(f"Password match: {stored_hash == computed_hash}")

        if stored_hash == computed_hash:
            print("Login successful!")
            return True
        else:
            print("Login failed - incorrect password")
            return False

if __name__ == "__main__":
    test_login()