package services

import "books/internal/models"

type Storage interface {
	CreateUser(login, password string) error
	GetUser(login string) (*models.User, error)
	AuthUser(login, password string) (bool, error)

	CreateBook(author, name string) error
	GetBooks() ([]models.Book, error)

	AddBookToLib(login string, bookID int) error
	CreateRequest(requester, owner string, bookID int) error
	GetLibForUser(user string) ([]models.Book, error)
	GetRequestsList(user string) ([]models.ExchangeRequest, error)
	AcceptRequest(id int) error

	Connect() error
}

type Tokenator interface {
	Generate(login string) (string, error)
	Check(token string) (bool, string)
}
