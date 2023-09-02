from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema, models, utils, oauth2

router = APIRouter(tags=["authentication"])


@router.post('/login', response_model=schema.Token)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials Not Found.")

    verify = utils.verify(user_credentials.password, user.password)
    if not verify:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials Not Found.")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    oauth2.get_current_user(access_token, db)
    return {"access_token": access_token, "token_type": "bearer"}
