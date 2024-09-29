package errs

import "errors"

var UserAlreadyRegistered = errors.New("User already registered")
var WrongCredentials = errors.New("Wrong credentionals")
