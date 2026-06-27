from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Board, BoardColumn, User
from app.schemas import BoardCreate, BoardOut, ColumnCreate, ColumnOut

router = APIRouter(tags=["boards"])


@router.get("/boards", response_model=list[BoardOut])
def list_boards(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Board).filter(Board.owner_id == user.id).all()


@router.post("/boards", response_model=BoardOut)
def create_board(
    data: BoardCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    board = Board(title=data.title, owner_id=user.id)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


@router.get("/boards/{board_id}", response_model=BoardOut)
def get_board(
    board_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    board = (
        db.query(Board)
        .filter(Board.id == board_id, Board.owner_id == user.id)
        .first()
    )
    if not board:
        raise HTTPException(status_code=404, detail="Доска не найдена")
    return board


@router.post("/boards/{board_id}/columns", response_model=ColumnOut)
def create_column(
    board_id: int,
    data: ColumnCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    board = (
        db.query(Board)
        .filter(Board.id == board_id, Board.owner_id == user.id)
        .first()
    )
    if not board:
        raise HTTPException(status_code=404, detail="Доска не найдена")
    count = db.query(BoardColumn).filter(BoardColumn.board_id == board_id).count()
    column = BoardColumn(title=data.title, board_id=board_id, position=count)
    db.add(column)
    db.commit()
    db.refresh(column)
    return column
