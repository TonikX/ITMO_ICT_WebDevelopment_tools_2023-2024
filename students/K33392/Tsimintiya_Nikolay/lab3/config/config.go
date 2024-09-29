package config

import (
	"github.com/ilyakaznacheev/cleanenv"
)

type Server struct {
	Host string `yaml:"host"`
	Port string `yaml:"port"`
}

type Worker struct {
}

type Postgres struct {
	Host     string `yaml:"host"`
	Port     string `yaml:"port"`
	Username string `yaml:"username"`
	Password string `yaml:"password"`
	Database string `yaml:"database"`
}

type Rabbit struct {
	URL string `yaml:"url"`
}

type Config struct {
	Server   `yaml:"Server"`
	Rabbit   `yaml:"Rabbit"`
	Postgres `yaml:"Postgres"`
}

func MustLoad() *Config {
	var cfg Config
	err := cleanenv.ReadConfig("config.yaml", &cfg)
	if err != nil {
		panic(err)
	}
	return &cfg
}
