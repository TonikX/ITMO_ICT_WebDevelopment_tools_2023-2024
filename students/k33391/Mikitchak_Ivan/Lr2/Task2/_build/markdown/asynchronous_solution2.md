# asynchronous_solution2

<a id="module-asynchronous_solution2"></a>

### asynchronous_solution2.extract_user(data)

Extracts user information from the provided JSON data.

Args:
: data: A dictionary containing user data in JSON format.

Returns:
: dict: A dictionary containing extracted user fields (email, hashed password, first name, and last name).
  None: If an error occurs during extraction.

Raises:
: Exception: If an error occurs while extracting user data.

### *async* asynchronous_solution2.fetch_data(session)

Fetches JSON data from a predefined URL asynchronously.

Args:
: session: An aiohttp.ClientSession object used to make the HTTP request.

Returns:
: dict: The fetched JSON data if successful.
  None: If an error occurs during the request or parsing.

Raises:
: Exception: If an error occurs while fetching or decoding JSON.

### asynchronous_solution2.hash_password(password)

Hashes the provided password using bcrypt.

* **Return type:**
  `str`

Args:
: password: The plain text password to be hashed.

Returns:
: str: The hashed password.

### *async* asynchronous_solution2.main()

Main function to initiate the asynchronous data fetching and storing tasks.

### *async* asynchronous_solution2.parse_and_save(session)

Fetches user data, extracts relevant fields, and stores them in the database.

Args:
: session: An aiohttp.ClientSession object used to make HTTP requests.

Returns:
: None

### *async* asynchronous_solution2.store_user(user)

Stores user information in the database asynchronously.

Args:
: user: A dictionary containing the user’s email, hashed password, first name, and last name.

Raises:
: Exception: If an error occurs while inserting user data into the database.
