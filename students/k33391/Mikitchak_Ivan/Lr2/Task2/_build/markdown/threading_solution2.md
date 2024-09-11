# threading_solution2

<a id="module-threading_solution2"></a>

### threading_solution2.extract_user(data)

Extracts user information from the fetched data.

Args:
: data: The JSON data containing user information.

Returns:
: dict: A dictionary with user details (email, hashed_password, first_name, last_name),
  : or None if an error occurs.

Raises:
: Exception: If an error occurs while extracting user information from the data.

### threading_solution2.fetch_data(session)

Fetches user data from the specified URL using the provided session.

Args:
: session: A requests.Session object used to make the HTTP request.

Returns:
: dict: The JSON data received from the request, or None if an error occurs.

Raises:
: Exception: If an error occurs while making the request or decoding the response.

### threading_solution2.hash_password(password)

Hashes a password using bcrypt.

* **Return type:**
  `str`

Args:
: password: The plaintext password to be hashed.

Returns:
: str: The hashed password.

### threading_solution2.log(msg)

Logs a message to the console in a thread-safe manner.

Args:
: msg: The message to be printed to the console.

### threading_solution2.main()

Main function that initializes environment variables and starts multiple threads to process user data concurrently.

### threading_solution2.parse_and_save(session)

Fetches user data, extracts user information, and stores it in the database.

Args:
: session: A requests.Session object used to make the HTTP request.

### threading_solution2.store_user(user)

Stores the user information in the PostgreSQL database.

Args:
: user: A dictionary containing user details (email, hashed_password, first_name, last_name).

Raises:
: Exception: If an error occurs while connecting to the database or executing the SQL command.
