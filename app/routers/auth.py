from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import oauth2

from .. import database, schemas, models, utils

router = APIRouter(tags=['Authentication'],
                   prefix='/api/v1'
                   )


@router.post('/login')
def login( user_credentials : OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    user=db.query(models.User).filter(
        models.User.username==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #create token
    access_token =oauth2.create_access_token(data={"user_id":user.id})
    return {"access token":access_token, "token type":"Bearer"}
    