package storage

import (
	"books/config"
	"books/internal/services"
	"context"
	"github.com/go-pg/pg/v10"
)

type storage struct {
	cfg config.Config
	db  *pg.DB
}

func New(cfg *config.Config) services.Storage {
	return &storage{cfg: *cfg}
}

func (p *storage) Connect() error {
	p.db = pg.Connect(&pg.Options{
		Addr:            p.cfg.Postgres.Host + ":" + p.cfg.Postgres.Port,
		User:            p.cfg.UserName,
		Password:        p.cfg.Password,
		Database:        p.cfg.DBName,
		MaxRetries:      3,
		MaxRetryBackoff: 3,
	})

	if err := p.db.Ping(context.Background()); err != nil {

		return err
	}

	return nil
}
