# API Overview

The Bookcrossing App exposes several endpoints for user, book, and request management. 

## Endpoints

- **GET /**: Returns a welcome message.
  
- **GET /users_list**: Retrieves a list of all users.
  
- **GET /user/{name}**: Retrieves a user by their name.
  
- **POST /user**: Creates a new user.
  
- **POST /profile**: Creates a new profile.
  
- **GET /books**: Retrieves a list of all books.
  
- **GET /book/{name}**: Retrieves a book by its title.
  
- **POST /book**: Creates a new book.
  
- **DELETE /book/{book_id}**: Deletes a book by its ID.
  
- **POST /ownership**: Creates a new book ownership entry.
  
- **POST /request**: Creates a new request.
  
- **GET /requests/**: Retrieves a list of all requests.
  
- **GET /request/{id}**: Retrieves a request by its ID.
  
- **PUT /request/{id}**: Responds to a request.

