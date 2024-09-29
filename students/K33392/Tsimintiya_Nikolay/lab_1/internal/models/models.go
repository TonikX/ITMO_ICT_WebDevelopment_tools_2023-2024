package models

type Book struct {
	ID     int    `pg:"id"`
	Author string `pg:"author"`
	Name   string `pg:"name"`
}

type ExchangeRequest struct {
	ID         int  `pg:"id"`
	Requester  int  `pg:"requester"`
	Owner      int  `pg:"owner"`
	B          int  `pg:"book"`
	IsAccepted bool `pg:"is_accepted"`
}

type User struct {
	ID    int    `pg:"id"`
	Login string `pg:"login"`
}

type Nested struct {
	User  `json:"user"`
	Books []Book `json:"books"`
}
