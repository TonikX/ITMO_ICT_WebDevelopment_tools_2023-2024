migrate:
	migrate -path migrations -database "postgresql://postgres:1234@localhost:5433/books?sslmode=disable" -verbose up
unmigrate:
	migrate -path migrations -database "postgresql://postgres:1234@localhost:5433/books?sslmode=disable" -verbose down
