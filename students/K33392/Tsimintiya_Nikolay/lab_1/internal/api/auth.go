package api

import (
	"books/internal/api/helpers"
	"books/internal/errs"
	"github.com/gin-gonic/gin"
	"net/http"
)

func (s *Server) RegisterUser(c *gin.Context) {
	login := c.Query("login")
	password := c.Query("password")

	err := s.storage.CreateUser(login, password)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
		return
	}

	c.AbortWithStatus(http.StatusOK)
}

func (s *Server) AuthUser(c *gin.Context) {
	login := c.Query("login")
	password := c.Query("password")

	res, err := s.storage.AuthUser(login, password)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
		return
	}

	if res {
		token, err := s.tokenator.Generate(login)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusInternalServerError, helpers.NewJSONErr(err))
			return
		}
		c.AbortWithStatusJSON(http.StatusOK, gin.H{"token": token})
		return
	} else {
		c.AbortWithStatusJSON(http.StatusBadRequest, helpers.NewJSONErr(errs.WrongCredentials))
		return
	}
}
