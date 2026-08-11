import uuid
from datetime import datetime, timezone

from sqlalchemy import create_engine, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


DB_URL = "sqlite:///pycoder.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(200), default="New Chat")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda:datetime.now(timezone.utc))

    messages: Mapped[list['Message']]= relationship(
        back_populates='conversation',
        cascade="all, delete-orphan",
        order_by = "Message.id"
    )


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"))
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
 
    conversation: Mapped["Conversation"] = relationship(back_populates="messages")


def init_db():
    Base.metadata.create_all(engine)

def create_conversation(title: str = "New chat") -> str:
    with SessionLocal() as session:
        conv = Conversation(title=title)
        session.add(conv)
        session.commit()
        return conv.id


def add_message(conversation_id: str, role:str, content: str)->None:
    with SessionLocal() as session:
        session.add(Message(conversation_id=conversation_id, role=role, content=content))

        conv = session.get(Conversation, conversation_id)
        if conv and conv.title == "New chat" and role == "user":
            conv.title = (content[:40]+"..." if len(content) > 40 else content)

        session.commit()


def get_history(conversation_id: str)->list[dict]:
    with SessionLocal() as session:
        conv = session.get(Conversation, conversation_id)
        if not conv:
            return []
        
        return [{"role": m.role, 'content': m.content} for m in conv.messages]


def list_conversations(limit: int = 50) -> list[dict]:
    with SessionLocal() as session:
        convs = (
            session.query(Conversation)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
            .all()
        )
        return [{"id": c.id, "title": c.title, "created_at": c.created_at.isoformat()} for c in convs]
 
 
def delete_conversation(conversation_id: str) -> None:
    with SessionLocal() as session:
        conv = session.get(Conversation, conversation_id)
        if conv:
            session.delete(conv)