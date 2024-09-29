package handlers

import (
	"books/internal/api/helpers"
	"github.com/gin-gonic/gin"
	"net/http"
	"strconv"
)

func (h *Handler) CreateRequest(c *gin.Context) {
	requester := c.Query("requester")

	var req helpers.CreateRequestReq
	err := c.BindJSON(&req)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, helpers.NewJSONErr(err))
		return
	}

	err = h.storage.CreateRequest(requester, req.Owner, req.BookID)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
		return
	}

	c.AbortWithStatus(http.StatusOK)
}

func (h *Handler) GetRequestsList(c *gin.Context) {
	user := c.Query("login")

	list, err := h.storage.GetRequestsList(user)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
		return
	}

	c.JSON(http.StatusOK, &list)
}

func (h *Handler) AcceptRequest(c *gin.Context) {
	id := c.Query("id")
	idInt, _ := strconv.Atoi(id)

	err := h.storage.AcceptRequest(idInt)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
		return
	}

	c.AbortWithStatus(http.StatusOK)
}
