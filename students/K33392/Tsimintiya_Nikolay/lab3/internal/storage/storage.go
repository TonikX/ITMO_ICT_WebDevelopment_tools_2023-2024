package storage

import (
	"context"
	"github.com/go-pg/pg/v10"
	"lab3/config"
	"log"
)

const SaveTitleQuery = "INSERT INTO parsing (url, header) VALUES (?, ?)"

type Storage struct {
	cfg *config.Config
	db  *pg.DB
}

func New(cfg *config.Config) *Storage {
	return &Storage{cfg: cfg}
}

func (s *Storage) Connect() {
	s.db = pg.Connect(&pg.Options{
		Addr:            s.cfg.Postgres.Host + ":" + s.cfg.Postgres.Port,
		User:            s.cfg.Postgres.Username,
		Password:        s.cfg.Postgres.Password,
		Database:        s.cfg.Database,
		MaxRetries:      3,
		MaxRetryBackoff: 3,
	})

	if err := s.db.Ping(context.Background()); err != nil {
		log.Fatal(err)
	}
}

func (s *Storage) SaveTitle(url, title string) error {
	_, err := s.db.Exec(SaveTitleQuery, url, title)
	return err
}
