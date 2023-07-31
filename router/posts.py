from fastapi import HTTPException, Response, status, Depends, APIRouter
from typing import List, Optional
import schema
from database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
import models
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get('/', response_model=List[schema.PostOut])
def get_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 1, skip: int = 0, term: Optional[str] = ""):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(term)).limit(limit).offset(
        skip).all()
    return post


@router.get('/{post_id}', response_model=schema.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(
        models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found.")
    return post.first()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    if new_post == None:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED, detail=f"Post: {new_post} was created")
    return new_post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(
        models.Post.id == post_id).first()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail=f"No post left to delete")
    if deleted_post.owner_id == user_id.id:
        db.delete(deleted_post)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Forbidden action")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{post_id}', response_model=schema.Post)
def update_post(post_id: int, post: schema.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(
        models.Post.id == post_id)
    updated_post_instance = updated_post.first()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found.")
    if updated_post_instance.owner_id == user_id.id:
        updated_post.update(post.dict())
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Forbidden action")
    return updated_post_instance
