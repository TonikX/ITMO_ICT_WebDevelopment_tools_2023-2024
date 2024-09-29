package queries

const (
	CreateUser = `
	INSERT INTO users(login, password) VALUES
	(?, ?);
`
	GetUser = ` 
	SELECT id, login FROM Users WHERE login = ?;
`

	AuthUser = `
	SELECT EXISTS (SELECT login FROM users WHERE login=? and password = ?)
`
	CreateBook = `
	INSERT INTO books(author, name) VALUES 
	(?, ?);
`
	GetBooks = `
	SELECT * FROM books;
`
	AddBookToLib = `
	INSERT INTO sharing(owner, book) VALUES 
	((SELECT id from users where login = ?), ?);
`
	GetLib = `
	SELECT * from books 
	where id = (SELECT book from sharing 
	where owner = (select id from users where login = ?));
`
	CreateRequest = `
	insert into requests(requester, owner, book) values 
	((select id from users where login = ?), (select id from users where login = ?), ?);
`
	GetRequestsList = `
	SELECT * from requests 
	where owner = (select id from users where login = ?);
`
	AcceptRequest = `
	UPDATE requests 
	set is_accepted = true 
	where id = ?;
`
)
