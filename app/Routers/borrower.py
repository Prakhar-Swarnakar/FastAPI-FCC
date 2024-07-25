from fastapi import FastAPI, HTTPException, status , Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app import oauth2
from .. import model
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas
from .. import utils

router = APIRouter(
    prefix='/borrower',
    tags=['Borrower']
)
#Borrower
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BorrowerInfo)
async def create_borrower_details(user: schemas.Borrower, db: Session = Depends(get_db)):
    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    db_borrower = model.Borrower(**user.model_dump())
    db.add(db_borrower)
    db.commit()
    db.refresh(db_borrower)
    return db_borrower

""" @router.get("/{id}", response_model=schemas.BorrowerInfo)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.Borrower).filter(model.Borrower.borrower_id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id={id} not found")
    return user """
    
@router.get("/", response_model=schemas.BorrowerInfo)
async def get_user( db: Session = Depends(get_db),
                    borrower_data: schemas.TokenData = Depends(oauth2.get_current_borrower)):
    user = db.query(model.Transaction).filter(model.Transaction.borrower_id == borrower_data.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id={id} not found")
    return user

@router.get("/transactions", response_model=schemas.BorrowerInfo)
async def get_all_My_Transaction( db: Session = Depends(get_db),
                    borrower_data: schemas.TokenData = Depends(oauth2.get_current_borrower)):
    transactions = db.query(model.Borrower).filter(model.Borrower.borrower_id == borrower_data.id).all()
    return transactions

@router.put("/edit_username", response_model=schemas.BorrowerInfo)
async def edit_username( username: schemas.UpdateUsername, db: Session = Depends(get_db),
                        borrower_data: schemas.TokenData = Depends(oauth2.get_current_borrower)):
    existing_borrower = db.query(model.Borrower).filter(model.Borrower.borrower_id == borrower_data.id).first()
    if not existing_borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id={borrower_data.id} not found")
    else:
        existing_borrower.name = username.name
        db.commit()
        db.refresh(existing_borrower)
        return {"message":f"User with id={id} has been renamed"}
    
@router.put("/edit_credentials", response_model=schemas.BorrowerInfo)
async def edit_credential(credentials: schemas.Credential, db: Session = Depends(get_db),
                          borrower_data: schemas.TokenData = Depends(oauth2.get_current_borrower)):
    existing_borrower = db.query(model.Borrower).filter(model.Borrower.borrower_id == borrower_data.id).first()
    if not existing_borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id={borrower_data.id} not found")
    else:
        existing_borrower.email = credentials.email
        existing_borrower.password = credentials.password
        db.commit()
        db.refresh(existing_borrower)
        return {"message":f"User's credentials with id={id} has been updated"}    

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user( db: Session = Depends(get_db),
                       borrower_data: schemas.TokenData = Depends(oauth2.get_current_borrower)):
    db_borrower = db.query(model.Borrower).filter(model.Borrower.borrower_id == borrower_data.id).first()
    if not db_borrower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id={borrower_data.id} not found")
    existing_borrows = db.query(model.Transaction).filter(model.Transaction.borrower_id == borrower_data.id 
                                                          and model.Transaction.returned== False).all()
    if existing_borrows:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Borrower with id {borrower_data.id} has not returned all books")
    db.delete(db_borrower)
    db.commit()
    return