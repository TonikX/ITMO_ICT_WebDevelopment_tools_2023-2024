# multiprocessing_solution2

<a id="module-multiprocessing_solution2"></a>

### multiprocessing_solution2.extract_user(data)

Extracts user information from the API response data.

Args:
: data: A dictionary containing user data fetched from the API.

Returns:
: dict: A dictionary containing extracted user information (email, hashed password, first name, last name), or None if an error occurs.

Raises:
: Exception: If an error occurs while extracting user information.

### multiprocessing_solution2.fetch_data(session)

Fetches random user data from a public API using the provided session.

Args:
: session: A requests.Session object used to make the HTTP request.

Returns:
: dict: The fetched user data as a dictionary, or None if an error occurs.

Raises:
: Exception: If an error occurs while fetching or decoding the response.

### multiprocessing_solution2.hash_password(password)

Hashes a given password using bcrypt.

* **Return type:**
  `str`

Args:
: password: The plain text password to be hashed.

Returns:
: str: The hashed password.

### multiprocessing_solution2.log(msg)

Logs a message to the console in a thread-safe manner.

Args:
: msg: The message to be printed to the console.

### multiprocessing_solution2.main()

Main function that initializes environment variables and starts multiple processes to fetch and store user data concurrently.

### multiprocessing_solution2.parse_and_save(session)

Fetches user data, extracts the user information, and stores it in the database.

Args:
: session: A requests.Session object used to make the HTTP request.

### multiprocessing_solution2.store_user(user)

Stores user data into the PostgreSQL database.

Args:
: user: A dictionary containing user information to be stored in the database.

Raises:
: Exception: If an error occurs while connecting to the database or storing user data.
