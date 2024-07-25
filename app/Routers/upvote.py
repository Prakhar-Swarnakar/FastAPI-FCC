from fastapi import APIRouter,status,Depends,HTTPException
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from .. import model
from .. import utils


router = APIRouter(prefix="/upvotes",
                   tags=["upvotes"])

@router.post("/", status_code=status.HTTP_200_OK)
async def rate_book(vote: schemas.vote, db: Session = Depends(get_db),
                    borrower_data: schemas.TokenData = Depends(oauth2.get_current_borrower)):
    existing_book = db.query(model.Book).filter(model.Book.book_id == vote.book_id).first()
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id={id} was not found")
    if  not utils.upvoteValidator(vote.vote_direction):   
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"vote is not valid")
    existing_rating = db.query(model.BookRating).filter(model.BookRating.book_id == vote.book_id and model.BookRating.borrower_id == borrower_data.id).first()
    if existing_rating: #if vote already exist -> modify old vote or delete old vote
        if existing_rating.upVote == vote.vote_direction: #clicked on the same button 
            db.delete(existing_rating)
            db.commit()
            return {"message": "old vote deleted"}
            #raise   HTTPException(status_code=status.HTTP_409_CONFLICT,
            #                detail=f"same vote by borrower, borrower id:{borrower_data.id}, for the book, book id:{vote.book_id} , is already done")
        else: #didnt click on the same button then -> update vote
            existing_rating.upVote = vote.vote_direction
            db.commit()
            db.refresh(existing_rating)
            return {"message": "old vote modified",
                    "book details": existing_book}
    else:
        new_rating = model.BookRating(book_id = vote.book_id, borrower_id = borrower_data.id, upVote = vote.vote_direction)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return {"message": "new voting done",
                "book details": existing_book}
        
    