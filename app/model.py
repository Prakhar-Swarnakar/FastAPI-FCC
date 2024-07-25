from .database import Base 
from sqlalchemy import Column, String, Integer, Boolean,TIMESTAMP,DATE, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
class Book(Base):
    __tablename__ = "books"  

    book_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    #author_Id = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    available_issues =Column(Integer,nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    # published_date = Column(DATE,nullable=False, server_default=text("now()"))
    available = Column(Boolean,nullable=False)
    
class Author(Base):
    __tablename__= "authors"
    
    author_Id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String, nullable=False) 
    #birthdate
    #nationality

class BookRating(Base):
    __tablename__ = "ratings"
    
    #rating_id = Column(Integer,primary_key=True,nullable=False)
    book_id = Column(Integer,ForeignKey(column="books.book_id", ondelete="CASCADE"),primary_key=True,nullable=False)
    borrower_id = Column(Integer,ForeignKey(column="borrowers.borrower_id", ondelete="NO ACTION")
                         ,nullable=False,primary_key=True) #making it unique that 1 person can give 1 rating
    upVote = Column(Integer,nullable=False)
    
class Borrower(Base):
    __tablename__ = "borrowers"
    borrower_id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column (String, nullable=False, unique=True)
    password = Column (String, nullable=False)
     
class Transaction(Base):
    __tablename__= 'transactions'
    transactionID = Column(Integer,primary_key=True, nullable=False)
    book_Id = Column(Integer, ForeignKey(column="books.book_id",ondelete="CASCADE"), nullable=False) #you can cascade as well
    borrower_id = Column(Integer, ForeignKey(column="borrowers.borrower_id", ondelete="CASCADE"),nullable=False,)
    borrow_date = Column(DATE,nullable=False, server_default=text("now()"))
    return_date = Column(DATE,nullable=True)
    returned = Column(Boolean,nullable=False)
    Upvote= Column(Boolean,nullable=True)
    book_details = relationship("Book") 
    borrower_details = relationship("Borrower")

