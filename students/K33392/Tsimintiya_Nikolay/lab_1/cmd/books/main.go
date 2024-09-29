package main

import (
	"books/config"
	"books/internal/api"
	"books/internal/storage"
	"books/pkg/tokenator"
	"log"
)

func main() {
	cfg := config.MustLoad()
	s := storage.New(cfg)
	err := s.Connect()
	if err != nil {
		log.Fatalf("Error connecting to database: %v", err)
	}
	t := tokenator.New()

	serv := api.New(cfg, s, t)
	serv.ListenAndServe()
}
