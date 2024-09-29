# Конфигурация приложения
```yaml
Rabbit:
  url: amqp://guest:guest@rabbit:5672/

Server:
  host: api
  port: 8080

Postgres:
  host: 'postgres'
  port: '5432'
  username: 'root'
  password: 'secret'
  database: 'parsing'


```

# Compose-файл
```dockerfile
version: "3.9"
services:
  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=parsing

  api:
    image: api:latest
    ports:
      - "8080:8080"
    depends_on:
      - postgres

  rabbit:
    image: rabbitmq:3.13-management
    ports:
      - "5672:5672"
      - "15672:15672"
    depends_on:
      - api

  worker:
    image: worker:latest
    depends_on:
      - rabbit

```

# API 
```go
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

```

# Worker 
```go
package main

import (
	"errors"
	"fmt"
	amqp "github.com/rabbitmq/amqp091-go"
	"golang.org/x/net/html"
	"lab3/config"
	"lab3/internal/storage"
	"log"
	"net/http"
	"strings"
	"time"
)

func main() {
	cfg := config.MustLoad()
	fmt.Println(cfg)
	s := storage.New(cfg)
	s.Connect()

	// Забрать данные из Rabbit
	time.Sleep(5 * time.Second)
	conn, err := amqp.Dial(cfg.URL)
	if err != nil {
		log.Fatalf("Error connecting to RabbitMQ: %s", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"parsing", // name
		false,     // durable
		false,     // delete when unused
		false,     // exclusive
		false,     // no-wait
		nil,       // arguments
	)
	failOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	var forever chan struct{}

	go func() {
		for d := range msgs {
			url := string(d.Body)
			title, err := parsePage(url)
			if err != nil {
				log.Println(err)
			} else {
				err = s.SaveTitle(url, title)
				if err != nil {
					log.Println(err)
				}
			}
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Panicf("%s: %s", msg, err)
	}
}

func parsePage(url string) (string, error) {
	resp, _ := http.Get(url)
	defer resp.Body.Close()

	z := html.NewTokenizer(resp.Body)

	for {
		tt := z.Next()
		if tt == html.ErrorToken {
			break
		}

		t := z.Token()

		if t.Type == html.StartTagToken && t.Data == "title" {
			if z.Next() == html.TextToken {
				title := strings.TrimSpace(z.Token().Data)
				return title, nil
			}
		}

	}

	return "", errors.New("Title not found")
}

```