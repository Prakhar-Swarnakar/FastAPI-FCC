#responses and requests
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

#
class vote(BaseModel):
    book_id:int
    vote_direction:int 
    
class Upvotes(BaseModel):
    upvote: Optional[bool]
    borrower_id: int
    class Config:
        from_attributes:True
    
#request
class Book(BaseModel): 
    title: str
    genre: str
    available_issues: int
    available: bool = True 
    
class CreateBook(Book):
    pass
class Update_book(Book):
    pass

#response
class BookInfo(BaseModel):
    title: str
    genre: str
    available: bool
    published: bool = False
    
    class Config:
        from_attributes = True

class BookInfo2(BaseModel):
    book_id: int
    title: str
    genre: str
    available_issues: int
    available: bool
    published: bool = False
    
    class Config:
        from_attributes = True
        
class BookOut(BaseModel):
    Book: BookInfo2
    UpVotes: int
    
    class Config:
        from_attributes = True
        
#request
class Credential(BaseModel):
    email:EmailStr
    password:str
  
class UpdateUsername(BaseModel):
    name: str
        
class Borrower(Credential, UpdateUsername):
    pass

#response 
class BorrowerInfo(BaseModel):
    borrower_id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True
    
class Token(BaseModel):
    access_token: str
    token_type:str 
     
class TokenData(BaseModel):
    id: Optional[str] = None 
    #rn only id , later can add roles
    
#Response
class TransactionInfo(BaseModel):
    transactionID:int
    book_Id:int
    borrower_id:int
    borrow_date :date
    return_date :Optional[date] #note : keep in mind about optional 
    returned :bool
    book_details: BookInfo
    borrower_details: BorrowerInfo
    
    class Config:
        from_attributes = True