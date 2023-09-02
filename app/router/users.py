from fastapi import Response, status, Depends, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session

from .. import schema, models, utils

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get('/', response_model=List[schema.UserOut])
def root(db: Session = Depends(get_db)):
    my_user = db.query(models.User).all()
    return my_user


@router.get('/{user_id}', response_model=schema.UserOut)
def root(user_id: int, db: Session = Depends(get_db)):
    my_user = db.query(models.User).filter(models.User.id == user_id)
    return my_user.first()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = db.query(models.User).filter(
        models.User.id == user_id).first()
    db.delete(deleted_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{user_id}', response_model=schema.UserOut)
def update_post(user_id: int, user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_pw = utils.hash(user.password)
    user.password = hashed_pw
    new_user = user.dict()
    update_user = db.query(models.User).filter(models.User.id == user_id)
    update_user.update(new_user)
    db.commit()

    return update_user.first()
