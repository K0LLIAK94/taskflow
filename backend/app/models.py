from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from app.database import Base

# many-to-many: карточки ↔ метки
card_labels = Table(
    "card_labels",
    Base.metadata,
    Column("card_id", ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True),
    Column("label_id", ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    boards = relationship("Board", back_populates="owner", cascade="all, delete-orphan")


class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    owner_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="boards")
    columns = relationship(
        "BoardColumn", back_populates="board", cascade="all, delete-orphan"
    )


class BoardColumn(Base):
    __tablename__ = "columns"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    position = Column(Float, default=0)
    board_id = Column(ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)

    board = relationship("Board", back_populates="columns")
    cards = relationship(
        "Card", back_populates="column", cascade="all, delete-orphan"
    )


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    position = Column(Float, default=0)
    column_id = Column(ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)

    column = relationship("BoardColumn", back_populates="cards")
    labels = relationship("Label", secondary=card_labels, back_populates="cards")


class Label(Base):
    __tablename__ = "labels"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String, default="#999999")

    cards = relationship("Card", secondary=card_labels, back_populates="labels")
