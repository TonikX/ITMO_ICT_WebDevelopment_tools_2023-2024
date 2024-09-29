package handlers

import (
	"books/internal/api/helpers"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"strconv"
)

func (h *Handler) CreateBook(c *gin.Context) {
	author := c.Query("author")
	name := c.Query("name")

	err := h.storage.CreateBook(author, name)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
		return
	}

	c.AbortWithStatus(http.StatusOK)
}

func (h *Handler) GetBooks(c *gin.Context) {
	res, err := h.storage.GetBooks()
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
		return
	}
	c.IndentedJSON(http.StatusOK, res)
}

func (h *Handler) AddBookToLib(c *gin.Context) {
	user := c.Query("login")
	bookStr := c.Query("bookID")
	bookID, _ := strconv.Atoi(bookStr)
	fmt.Println("book id: ", bookID)

	err := h.storage.AddBookToLib(user, bookID)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
		return
	}

	c.AbortWithStatus(http.StatusOK)
}
