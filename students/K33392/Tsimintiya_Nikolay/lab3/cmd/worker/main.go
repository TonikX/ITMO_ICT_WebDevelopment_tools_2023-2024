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
