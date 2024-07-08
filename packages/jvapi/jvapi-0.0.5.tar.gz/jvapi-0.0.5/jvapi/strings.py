INIT_DOCSTRING = """
Initializes JVApi with the given API key.

Args:
    apikey (str): The API key to access the API.
"""

HANDLE_RESPONSE_DOCSTRING = """
Handles HTTP response and raises exceptions for non-successful responses.

Args:
    response (requests.Response): The HTTP response object.

Returns:
    dict: Parsed JSON response from the API.

Raises:
    requests.HTTPError: If the HTTP request fails.
    Exception: If the API returns an error status.
"""

REQUEST_DOCSTRING = """
Makes an HTTP request to the JV API.

Args:
    method (str): HTTP method ('GET', 'POST', 'PUT', etc.).
    path (str): API endpoint path.
    headers (dict, optional): Additional HTTP headers.
    params (dict, optional): Query parameters.
    data (dict, optional): Request payload data.
    files (dict, optional): Files to upload.
    is_json (bool, optional): Whether the payload is JSON.

Returns:
    dict: Parsed JSON response from the API.

Raises:
    requests.HTTPError: If the HTTP request fails.
    Exception: If the API returns an error status.
"""

YOUTUBEDL_DOCSTRING = """
Retrieves YouTubedl information from the API.

Args:
    query (str): The YouTubedl query.

Returns:
    dict: YouTubedl information from the API response.
"""

TIKTOKDL_DOCSTRING = """
Retrieves TikTok download information from the API.

Args:
    url (str): The TikTok video URL.

Returns:
    dict: TikTok download information from the API response.
"""

SMULE_DOCSTRING = """
Retrieves Smule information from the API.

Args:
    username (str): The Smule username.

Returns:
    dict: Smule information from the API response.
"""
SMULEDL_DOCSTRING = """
Retrieves Smule information from the API.

Args:
    username (str): The Smule username.

Returns:
    dict: Smule information from the API response.
"""


TIKTOK_DOCSTRING = """
Retrieves TikTok information from the API.

Args:
    username (str): The TikTok username.

Returns:
    dict: TikTok information from the API response.
"""

CLASS_DOCSTRING = """
A class to interact with JV API.

Attributes:
    apikey (str): The API key used for authentication.
    base_url (str): The base URL for API requests.
    headers (dict): HTTP headers including User-Agent and Apikey.
    session (requests.Session): HTTP session for making requests.
"""
