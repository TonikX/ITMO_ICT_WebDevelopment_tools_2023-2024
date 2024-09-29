package main

import (
	"fmt"
	"lab3/config"
	"lab3/internal/server"
)

func main() {
	cfg := config.MustLoad()
	fmt.Println(cfg)
	s := server.NewServer(cfg)
	s.Start()
}
