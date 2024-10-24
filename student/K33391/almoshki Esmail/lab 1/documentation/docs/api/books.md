# Book Endpoints

## Get All Books
**GET /books**  
Response: Returns a list of books in JSON format.

## Get Book by Title
**GET /book/{name}**  
Response: Returns the book data matching the provided title.

## Create Book
**POST /book**  
Request Body:  
``` json
{
    "title": "New Book",
    "author": "Author Name"
}
