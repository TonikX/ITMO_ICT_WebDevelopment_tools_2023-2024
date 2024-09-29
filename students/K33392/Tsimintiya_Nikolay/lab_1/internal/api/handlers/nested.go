package handlers

import (
	"books/internal/models"
	"github.com/gin-gonic/gin"
	"net/http"
)

func (h *Handler) GetUserLib(c *gin.Context) {
	user := c.Query("user")
	userModel, err := h.storage.GetUser(user)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	books, err := h.storage.GetLibForUser(user)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	resp := models.Nested{
		User:  *userModel,
		Books: books,
	}

	c.JSON(http.StatusOK, resp)
}
