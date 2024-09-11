# multiprocessing_solution

<a id="module-multiprocessing_solution"></a>

### multiprocessing_solution.extract_headers(html)

Extracts the headers section from an HTML page.

Args:
: html: A string containing the HTML page content.

Returns:
: str: The HTML headers as plain text, or None if an error occurs or no headers are found.

Raises:
: Exception: If an error occurs while parsing the HTML or extracting the headers.

### multiprocessing_solution.fetch_html(session, url)

Fetches HTML content from the specified URL using a given session.

Args:
: session: A requests.Session object used to make the HTTP request.
  url: The URL to fetch the HTML content from.

Returns:
: str: The HTML content of the page as plain text, or None if an error occurs.

Raises:
: Exception: If an error occurs while fetching the page or decoding the response.

### multiprocessing_solution.log(msg)

Logs a message to the console in a thread-safe manner.

Args:
: msg: The message to be printed to the console.

### multiprocessing_solution.main()

Main function to run the process of fetching, extracting, and storing headers concurrently using multiprocessing.

### multiprocessing_solution.parse_and_save(session, url)

Fetches HTML from a URL, extracts headers, and stores them in the database.

Args:
: session: A requests.Session object used to make the HTTP request.
  url: The URL to fetch, extract headers from, and store in the database.

### multiprocessing_solution.store_headers(url, headers)

Stores the extracted headers in the database.

Args:
: url: The URL from which the headers were extracted.
  headers: A string containing the HTML headers.

Raises:
: Exception: If an error occurs while connecting to the database or storing the headers.
