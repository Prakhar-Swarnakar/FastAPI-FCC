from fastapi import FastAPI, HTTPException, status , Depends, APIRouter
from typing import Optional
from .. import model
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas
from typing import List
from .. import oauth2
from datetime import date
from sqlalchemy import func,case

    ##BOOKS
router = APIRouter(
    prefix="/Book",
    tags=['Book']
)


@router.get('/', response_model=List[schemas.BookOut])
async def get_all_books(db: Session = Depends(get_db),
                        limit: int = 15, skip: int = 0, search: Optional[str] = ""):
    # Base query with outer join to count upvotes
    query = db.query(model.Book, func.count(model.BookRating.book_id).label("UpVotes")).join(
        model.BookRating, model.BookRating.book_id == model.Book.book_id, isouter=True)
    
    # Apply search filter if search parameter is provided
    if search:
        query = query.filter(model.Book.title.contains(search))
    
    # Group by book_id to aggregate UpVotes, apply limit and skip for pagination
    result = query.group_by(model.Book.book_id).order_by(model.Book.book_id).limit(limit).offset(skip).all()

    # Correctly use the schemas to restructure the results
    resultsRestructured = [
        schemas.BookOut(
            Book=schemas.BookInfo2(
                book_id=book.book_id,
                title=book.title,
                genre=book.genre,
                available_issues=book.available_issues,
                available=book.available,
                published=book.published
            ),
            UpVotes=upvotes
        )
        for book, upvotes in result
    ]

    return resultsRestructured
      

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BookInfo)
async def add_new_book(book: schemas.CreateBook, db: Session = Depends(get_db) ):# admin access
    print(book)
    new_book = model.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_book_details(id: int, db: Session = Depends(get_db)):
    
    result = db.query(model.Book, func.count(model.BookRating.book_id).label("UpVotes")).join(
        model.BookRating, model.BookRating.book_id == model.Book.book_id, isouter=True).group_by(
            model.Book.book_id).filter(model.Book.book_id == id).first()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id={id} was not found")
    
    book, upvotes = result
    resultRestructured = schemas.BookOut(
        Book=schemas.BookInfo2(
            book_id=book.book_id,
            title=book.title,
            genre=book.genre,
            available_issues=book.available_issues,
            published=book.published,
            available=book.available
        ),
        UpVotes=upvotes
    )
    
    return resultRestructured

#delete -> in case of adult content
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #if the Admin/teacher/author then only delete 
async def remove_book(id: int, db: Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.book_id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id={id} was not found")
    existing_borrows = db.query(model.Transaction).filter(model.Transaction.book_Id == id 
                                                          and model.Transaction.returned== False).all()
    if existing_borrows:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not all books have been returned")
    #if book.author == author then only delete else not authorised
    db.delete(book)
    db.commit()
    return {"message": f"Book with id={id} has been deleted"}

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_book_details(id: int, updated_book: schemas.Update_book,
                              db: Session = Depends(get_db)):
    existing_book = db.query(model.Book).filter(model.Book.book_id == id).first()
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id={id} was not found")
    for key, value in updated_book.model_dump().items():
        setattr(existing_book, key, value)
    db.commit()
    db.refresh(existing_book)
    return {"updated_book": existing_book}

@router.put("/issue/{id}", status_code=status.HTTP_200_OK)
async def issue_book(id: int, db: Session = Depends(get_db),
                     borrower_data: schemas.TokenData = Depends(oauth2.get_current_borrower)):
    existing_book = db.query(model.Book).filter(model.Book.book_id == id).first()
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id={id} was not found")
    if not existing_book.available:
        return {"message": f"Book with id={id} has been issued out"}
    else:
        existing_book.available_issues = existing_book.available_issues - 1
        new_transaction = model.Transaction(book_Id=id, borrower_id=borrower_data.id,
                                            borrow_date=date.today(), 
                                            returned=False, return_date = None)
        db.add(new_transaction)
        if existing_book.available_issues == 0:
            existing_book.available = False
        db.commit()
        db.refresh(existing_book)
        db.refresh(new_transaction)
        return {"message": f"Book with id={id} has been issued",
                "book details": existing_book}


@router.put("/return/{id}", status_code=status.HTTP_200_OK)
async def return_book(id: int, db: Session = Depends(get_db),
                      borrower_data: schemas.TokenData = Depends(oauth2.get_current_borrower)):
    existing_book = db.query(model.Book).filter(model.Book.book_id == id).first()
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id={id} was not found")
    else:
        existing_transaction = db.query(model.Transaction).filter(
            model.Transaction.borrower_id == borrower_data.id and 
            model.Transaction.book_Id == id and
            model.Transaction.returned == False).first()
        if not existing_transaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Transaction not found for book id {id} and borrower id {borrower_data.id}")
        existing_book.available_issues = existing_book.available_issues + 1
        existing_transaction.return_date = date.today()
        existing_transaction.returned = True
        
    db.commit()
    db.refresh(existing_book)
    db.refresh(existing_transaction)
    return {"message": f"Book with id={id} has been returned",
            "book details": existing_book}
