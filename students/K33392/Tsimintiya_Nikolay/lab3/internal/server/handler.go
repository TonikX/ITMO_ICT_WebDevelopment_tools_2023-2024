package server

import (
	"context"
	"fmt"
	"github.com/gin-gonic/gin"
	amqp "github.com/rabbitmq/amqp091-go"
	"net/http"
	"time"
)

func (s *Server) parseHandler(c *gin.Context) {
	url := c.Query("url")
	fmt.Println("url:", url)
	conn, err := amqp.Dial(s.cfg.URL)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusServiceUnavailable, gin.H{"rabbit connecting error": err.Error()})
		return
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		c.AbortWithStatusJSON(http.StatusServiceUnavailable, gin.H{"open rabbit channel err": err.Error()})
		return
	}

	q, err := ch.QueueDeclare(
		"parsing", // name
		false,     // durable
		false,     // delete when unused
		false,     // exclusive
		false,     // no-wait
		nil,       // arguments
	)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusServiceUnavailable, gin.H{"open queue err": err.Error()})
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	err = ch.PublishWithContext(ctx,
		"",     // exchange
		q.Name, // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(url),
		})
	if err != nil {
		c.AbortWithStatusJSON(http.StatusServiceUnavailable, gin.H{"publish task err": err.Error()})
		return
	}

	c.AbortWithStatus(http.StatusOK)
}
