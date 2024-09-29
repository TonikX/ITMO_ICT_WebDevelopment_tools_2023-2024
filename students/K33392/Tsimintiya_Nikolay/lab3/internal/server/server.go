package server

import (
	"github.com/gin-gonic/gin"
	"lab3/config"
)

type Server struct {
	cfg *config.Config
	r   *gin.Engine
}

func NewServer(cfg *config.Config) *Server {
	s := &Server{
		cfg: cfg,
		r:   gin.Default(),
	}
	s.r.POST("", s.parseHandler)
	return s
}

func (s *Server) Start() {
	s.r.Run(s.cfg.Server.Host + ":" + s.cfg.Server.Port)
}
