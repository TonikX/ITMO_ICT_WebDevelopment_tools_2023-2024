# asynchronous_solution

<a id="module-asynchronous_solution"></a>

### asynchronous_solution.extract_headers(html)

A function for extracting the headers section of html page.

Args:
: html: a string containing HTML page

Returns:
: HTML as plain text or None if an error has occured

Raises:
: Exception: An error occurred while extracting headers

### *async* asynchronous_solution.fetch_html(session, url)

A function for fetching html from provided URL.

Args:
: session: requests.Session object
  url: URL string

Returns:
: HTML as plain text or None if an error has occured.

Raises:
: Exception: An error occurred while decoding text for <URL>
  Exception: Request to <URL> failed with status code <status code>
  Exception: An error occurred while fetching html from <URL>

### *async* asynchronous_solution.main()

The main function.

### *async* asynchronous_solution.parse_and_save(session, url)

The task function for fetching html and storing it in the database.

Args:
: session: requests.Session object
  url: URL string

### *async* asynchronous_solution.store_headers(url, headers)

A function for storing headers in the database.

Args:
: url: URL string
  headers: string containing the headers section

Raises:
: Exception: An error occurred while storing headers for <URL>
