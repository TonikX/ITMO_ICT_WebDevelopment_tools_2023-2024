package config

import (
	"github.com/ilyakaznacheev/cleanenv"
	"log"
	"time"
)

type Config struct {
	Server
	Postgres
}

type Server struct {
	Port        string        `yaml:"port" env-default:"8080"`
	Host        string        `yaml:"host" env-default:"localhost"`
	Timeout     time.Duration `yaml:"timeout" env-default:"4s"`
	IdleTimeout time.Duration `yaml:"idle_timeout" env-default:"60s"`
}

type Postgres struct {
	Host     string `yaml:"postgres_host"`
	DBName   string `yaml:"postgres_db_name"`
	UserName string `yaml:"postgres_user_name"`
	Password string `yaml:"postgres_password"`
	Port     string `yaml:"postgres_port"`
}

func MustLoad() *Config {
	var config Config
	if err := cleanenv.ReadConfig("config/config.yaml", &config); err != nil {
		log.Fatalf("cannot read config: %s", err)
	}
	return &config
}
