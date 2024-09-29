package storage

import (
	"books/internal/models"
	"books/internal/storage/queries"
)

func (p *storage) CreateUser(login, password string) error {
	_, err := p.db.Exec(queries.CreateUser, login, password)
	return err
}

func (p *storage) GetUser(login string) (*models.User, error) {
	var result models.User
	_, err := p.db.Query(&result, queries.GetUser, login)
	return &result, err
}

func (p *storage) AuthUser(login, password string) (bool, error) {
	var exists queries.Exsts
	_, err := p.db.Query(&exists, queries.AuthUser, login, password)
	return exists.Exst, err
}

func (p *storage) CreateBook(author, name string) error {
	_, err := p.db.Exec(queries.CreateBook, author, name)
	return err
}

func (p *storage) GetBooks() ([]models.Book, error) {
	var res []models.Book
	_, err := p.db.Query(&res, queries.GetBooks)
	return res, err
}

func (p *storage) AddBookToLib(login string, bookID int) error {
	_, err := p.db.Exec(queries.AddBookToLib, login, bookID)
	return err
}

func (p *storage) GetLibForUser(user string) ([]models.Book, error) {
	var res []models.Book
	_, err := p.db.Query(&res, queries.GetLib, user)
	return res, err
}

func (p *storage) CreateRequest(requester, owner string, bookID int) error {
	_, err := p.db.Exec(queries.CreateRequest, requester, owner, bookID)
	return err
}

func (p *storage) GetRequestsList(user string) ([]models.ExchangeRequest, error) {
	var res []models.ExchangeRequest
	_, err := p.db.Query(&res, queries.GetRequestsList, user)
	return res, err
}

func (p *storage) AcceptRequest(id int) error {
	_, err := p.db.Exec(queries.AcceptRequest, id)
	return err
}
