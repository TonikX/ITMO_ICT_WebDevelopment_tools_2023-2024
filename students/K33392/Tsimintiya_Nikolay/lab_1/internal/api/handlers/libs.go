package handlers

import (
	"books/internal/api/helpers"
	"github.com/gin-gonic/gin"
	"net/http"
)

func (h *Handler) GetLibForUser(c *gin.Context) {
	user := c.Query("user")
	books, err := h.storage.GetLibForUser(user)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
		return
	}

	resp := helpers.GetLibResp{
		User:  user,
		Books: books,
	}

	c.JSON(http.StatusOK, &resp)
}
