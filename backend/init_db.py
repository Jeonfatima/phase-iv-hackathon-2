from sqlmodel import SQLModel, create_engine, Session
from models.conversation import Conversation, Message
from datetime import datetime

# Database URL (SQLite for local test; replace with Neon/Postgres if needed)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables
SQLModel.metadata.create_all(engine)
print("OK Tables created successfully!")

# Optional: create a test conversation so chatbot responds properly
with Session(engine) as session:
    test_convo = Conversation(user_id="2", created_at=datetime.now(), updated_at=datetime.now())
    session.add(test_convo)
    session.commit()
    print(f"OK Test conversation created with ID: {test_convo.id}")