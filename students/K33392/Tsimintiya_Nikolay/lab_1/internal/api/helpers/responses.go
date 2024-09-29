package helpers

import "books/internal/models"

type GetLibResp struct {
	User  string
	Books []models.Book
}
