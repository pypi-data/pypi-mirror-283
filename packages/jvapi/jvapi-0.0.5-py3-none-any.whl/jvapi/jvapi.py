import json
import requests
from . import strings

class JVApi:
    __doc__ = strings.CLASS_DOCSTRING

    def __init__(self, apikey):
        """
        {docstring}
        """.format(docstring=strings.INIT_DOCSTRING)
        self.base_url = "https://jvselfbots.site"
        self.apikey = apikey
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/51.0.2704.64 Safari/537.36",
            "Apikey": apikey
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _handle_response(self, response):
        """
        {docstring}
        """.format(docstring=strings.HANDLE_RESPONSE_DOCSTRING)
        response.raise_for_status()
        result = response.json()
        if result["status"] != 200:
            raise Exception(result["message"])
        return result

    def _request(self, method, path, headers=None, params=None, data=None, files=None, is_json=False):
        """
        {docstring}
        """.format(docstring=strings.REQUEST_DOCSTRING)
        url = self.base_url + path
        headers = headers or {}
        headers.update(self.headers)

        if method.upper() not in ["GET", "POST", "PUT"]:
            raise ValueError(f"Unsupported HTTP method: {method}")

        kwargs = {
            "url": url,
            "headers": headers,
            "params": params,
            "data": json.dumps(data) if is_json else data,
            "files": files
        }

        response = self.session.request(method, **kwargs)
        return self._handle_response(response)

    def _generic_api_method(self, endpoint, query=None, url=None):
        """
        Generic method to call API endpoints.
        """
        if query:
            path = f"/{endpoint}={query}"
        elif url:
            path = f"/{endpoint}={url}"
        else:
            path = f"/{endpoint}"

        return self._request("GET", path)
    def youtubedl(self, url):
        """
        {docstring}
        """.format(docstring=strings.YOUTUBEDL_DOCSTRING)
        return self._generic_api_method("youtubedl", url)

    def smule(self, username):
        """
        {docstring}
        """.format(docstring=strings.SMULE_DOCSTRING)
        return self._generic_api_method("smule", username)

    def smuledl(self, url):
        """
        {docstring}
        """.format(docstring=strings.SMULEDL_DOCSTRING)
        return self._generic_api_method("smuledl", url)

    def tiktok(self, username):
        """
        {docstring}
        """.format(docstring=strings.TIKTOK_DOCSTRING)
        return self._generic_api_method("tiktok", username)

    def tiktokdl(self, url):
        """
        {docstring}
        """.format(docstring=strings.TIKTOKDL_DOCSTRING)
        return self._generic_api_method("tiktokdl", url)
