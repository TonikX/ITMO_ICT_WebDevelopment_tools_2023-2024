package helpers

import "github.com/gin-gonic/gin"

func NewJSONErr(err error) gin.H {
	return gin.H{"error": err.Error()}
}
