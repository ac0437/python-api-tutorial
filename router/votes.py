from fastapi import HTTPException, Response, status, Depends, APIRouter
from typing import List, Optional
import schema
from database import get_db
from sqlalchemy.orm import Session
import models
import oauth2

router = APIRouter(
    prefix="/votes",
    tags=["votes"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_post(vote: schema.Vote, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == user_id.id)
    found_vote = vote_query.first()
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    found_post = post_query.first()
    if found_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found.")
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"Post already voted on.")
        new_vote = models.Vote(post_id=vote.post_id, user_id=user_id.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'sucessful vote'}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found.")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message': 'success'}


@router.post('/{post_id}', status_code=status.HTTP_201_CREATED)
def create_post(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found.")
    vote = models.Vote(post_id=post.id, user_id=user_id.id)
    db.add(vote)
    db.commit()
    db.refresh(vote)

    return "liked"
