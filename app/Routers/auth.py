from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database
from .. import model
from .. import schemas
from .. import utils
from .. import oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(cred: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
   #OAuth2PasswordRequestForm =>{"username": "asdf","password": "alsdjf"} 
   #also in postman we have to fill these in form-data
    borrower = db.query(model.Borrower).filter(model.Borrower.email == cred.username).first()
    if not borrower:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Invalid Credentials")
    hashed_password = borrower.password
    if (not utils.verify(cred.password,hashed_password)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"borrower_id": str(borrower.borrower_id)}) 
    # data -> currently only the borrower id, later can add roles
    return {"access_token":access_token,
            "bearer_token":"bearer_token"}
    