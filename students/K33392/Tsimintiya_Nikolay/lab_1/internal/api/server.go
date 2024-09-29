package api

import (
	"books/config"
	handlers2 "books/internal/api/handlers"
	"books/internal/services"
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
)

type Server struct {
	cfg       *config.Config
	storage   services.Storage
	tokenator services.Tokenator

	router *gin.Engine
}

func New(cfg *config.Config, storage services.Storage, tokenator services.Tokenator) *Server {
	s := Server{
		cfg:       cfg,
		storage:   storage,
		tokenator: tokenator,
		router:    gin.Default(),
	}
	s.setRoutes()
	return &s
}

func (s *Server) ListenAndServe() {
	err := http.ListenAndServe(":8080", s.router)
	if err != nil {
		log.Fatalf("Error with listening on port: %v", err)
	}
}

func (s *Server) setRoutes() {
	s.router.POST("/register", s.RegisterUser)
	s.router.POST("auth", s.AuthUser)

	group := s.router.Group("/service")
	handlers := handlers2.Create(s.storage)
	//group.Use(s.AuthMW)
	group.POST("books", handlers.CreateBook)
	group.GET("books", handlers.GetBooks)

	group.POST("lib", handlers.AddBookToLib)
	group.GET("lib", handlers.GetLibForUser)

	// TODO: протестить
	group.POST("requests", handlers.CreateRequest)
	group.GET("requests", handlers.GetRequestsList)
	group.PATCH("requests", handlers.AcceptRequest)

	group.GET("nested", handlers.GetUserLib)
}
