package handlers

import "books/internal/services"

type Handler struct {
	storage services.Storage
}

func Create(storage services.Storage) *Handler {
	return &Handler{storage}
}
