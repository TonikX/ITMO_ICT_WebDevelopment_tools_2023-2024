package helpers

type AddBookToLibReq struct {
	BookID     int
	OwnerLogin string
}

type CreateRequestReq struct {
	BookID int    `json:"book_id"`
	Owner  string `json:"owner"`
}
