package api

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func (s *Server) AuthMW(c *gin.Context) {
	token := c.GetHeader("token")
	res, login := s.tokenator.Check(token)

	if res {
		c.AddParam("login", login)
		c.Next()
	} else {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}
}
