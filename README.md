# FastApiFCC
Free Code Camp Couse for python FastAPI development --> Notes

- create virtual environment in command prompt using py -3 -m venv venv
- select venv Interpreter from command pallete
- Activate the Script using venv\Scripts\activate.bat

Intalling Dependency

Make a 

To run the code: uvicorn app.main:app (earlier we were using "uvicorn main:app --reload" when main file wasnt in any module) 

To see the swagger documentation use "/docs"
SQlAchemy -> ORM: 
SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
sql alchemy cant do migration -> if there is an change in the table post table creation, it will ignore the changes
Alembic -> used for migration 

 cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
 (post.title, post.content, post.published))
 new_post = cursor.fetchone ()
 conn.commit()

 # Models
BookID (Primary Key)
Title
AuthorID (Foreign Key referencing Authors table)
Genre
AvailableIssues
PublishedDate
Available (Boolean indicating availability status)
Authors

AuthorID (Primary Key)
Name
BirthDate
Nationality
Borrowers

BorrowerID (Primary Key)
Name
Address
Phone
Email
Transactions

TransactionID (Primary Key)
BookID (Foreign Key referencing Books table)
BorrowerID (Foreign Key referencing Borrowers table)
BorrowDate
ReturnDate
Returned (Boolean indicating whether the book has been returned)

pip install passlib[bcrypt] -> 

authentication -> session based, JWT token based(stateless)(not encrypted)

when logging in -> create a access token which is encoded with data and expiration time 

when issuing book -> u need the user to be login/ protected API endpoint, we will create a dependancy on auth/ access token / current user which will get the access token from the /login url and if the user has not logged in create access token never ran and thus no access token thus no access

automate the JWT token set
in the login, within test add the command " pm.environment.set("JWT",pm.response.json().access_token); "

fastapi takes all the parameter of function as query parameter -> refer to get all

import os
path = os.getenv("Path")
print(path)

config.py -> we use pydantic_settings
.env file

addiding git ignore -> just create a file named .gitignore
venv/
.pyc
.env

setting 2 columns as primary key makes it a composite key


books = db.query(model.Book).filter(model.Book.title.contains(search)).limit(limit).offset(skip).all() --> using search, limit and offset -> search and pagenation

lastClockTime = 

Migration tool -> alembic
alembic init <alembicFileName>  -> to create a alemic File, will be created outside app
env.py -> main file for alembic --> need to give access to base file
Alembic.ini -> need to give sql url ==> but we use env.py to overide the config

now delete all table 
alembic revison -m "create book database" --> to create a alembic revision for database 
alembic current -> to see the current migration stage
alembic upgrade <code>
alembic downgrade base --> go before first alembic
alembic upgrade head  --> go to the top most revisin
 alembic revision --autogenerate -m "auto-generate-tables" --> checks the current base and makes changes accordingly requires the first revision

CORS -> add middleware in main.py
you can add multiple Cors for different domains

git -> .gitignore
requirement file -> use pip freeze to add information into the requirement file 