postgres:
	docker run --name postgres -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=secret -d postgres:16

createdb:
	docker exec -it postgres createdb --username=root --owner=root parsing

migrateup:
	migrate -path migrations -database "postgresql://root:secret@localhost:5432/parsing?sslmode=disable" -verbose up
