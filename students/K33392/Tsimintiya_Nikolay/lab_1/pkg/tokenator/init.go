package tokenator

import "math/rand"

var secretKey []byte

func init() {
	letterRunes := []byte("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

	b := make([]byte, 10)
	for i := range b {
		b[i] = letterRunes[rand.Intn(len(letterRunes))]
	}
	secretKey = b
}
