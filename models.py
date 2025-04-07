import atexit
import os
from datetime import datetime

from dotenv import load_dotenv

from sqlalchemy import create_engine, func, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5431/{DB_NAME}"

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    announcements = relationship("Announcement", back_populates="owner_relationship")


class Announcement(Base):
    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    owner: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner_relationship = relationship("User", back_populates="announcements")

    @property
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "owner": self.owner
        }


Base.metadata.create_all(engine)
print("Tables created")

atexit.register(engine.dispose)
