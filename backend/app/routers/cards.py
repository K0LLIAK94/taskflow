from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import BoardColumn, Card, User
from app.schemas import CardCreate, CardMove, CardOut

router = APIRouter(tags=["cards"])


def _owned_column(db: Session, column_id: int, user: User) -> BoardColumn:
    column = db.query(BoardColumn).filter(BoardColumn.id == column_id).first()
    if not column or column.board.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Колонка не найдена")
    return column


@router.post("/columns/{column_id}/cards", response_model=CardOut)
def create_card(
    column_id: int,
    data: CardCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _owned_column(db, column_id, user)
    count = db.query(Card).filter(Card.column_id == column_id).count()
    card = Card(
        title=data.title,
        description=data.description,
        column_id=column_id,
        position=count,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.patch("/cards/{card_id}/move", response_model=CardOut)
def move_card(
    card_id: int,
    data: CardMove,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card or card.column.board.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    _owned_column(db, data.column_id, user)
    card.column_id = data.column_id
    card.position = data.position
    db.commit()
    db.refresh(card)
    return card


@router.delete("/cards/{card_id}", status_code=204)
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card or card.column.board.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    db.delete(card)
    db.commit()
