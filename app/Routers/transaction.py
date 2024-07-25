from fastapi import FastAPI, HTTPException, status , Depends, APIRouter
from .. import model
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import schemas
from typing import List
from .. import oauth2
from datetime import date

    ##BOOKS
router = APIRouter(
    prefix="/transaction",
    tags=['Transaction']
)

#all must be admin access only 
""" @router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = model.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction """

@router.get("/{transaction_id}", response_model=schemas.TransactionInfo)
async def get_transactions_detail(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(model.Transaction).filter(model.Transaction.transactionID == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction

@router.get("/book/{book_id}", response_model=schemas.TransactionInfo)
async def get_all_book_transactions(book_id: int, db: Session = Depends(get_db)):
    transaction = db.query(model.Transaction).filter(model.Transaction.book_Id == book_id).all()
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction

@router.get("/borrower/{borrower_id}", response_model=schemas.TransactionInfo)
async def get_all_borrower_transactions(borrower_id: int, db: Session = Depends(get_db)):
    transaction = db.query(model.Transaction).filter(model.Transaction.borrower_id == borrower_id).all()
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction
""" 
@router.put("/{transaction_id}", response_model=schemas.TransactionInfo)
async def update_transaction(transaction_id: int, transaction: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = db.query(model.Transaction).filter(model.Transaction.transactionID == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction """

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(model.Transaction).filter(model.Transaction.transactionID == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return None

