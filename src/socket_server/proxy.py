import datetime
import http.server
import time
import re
from typing import Any, Tuple
import requests  # type: ignore
from re import error as RegexException
from requests import Response, HTTPError
from bs4 import BeautifulSoup

from utils import proxy_globals

TARGET_URL = proxy_globals.TARGET_URL
HOST = proxy_globals.HOST
PORT = proxy_globals.PORT
HEADERS = proxy_globals.HEADERS


# timestamp function for logs.
def get_time_stamp():
    return f"{HOST} - - [{str(datetime.datetime.fromtimestamp(time.time()).strftime('%d/%b/%Y %H:%M:%S'))}]"


class Handler(http.server.BaseHTTPRequestHandler):
    """Request handler class

        Serves the client with identified http request
        by modifying the outgoing response data.
    """

    def do_GET(self):
        response, static_content = self.do_request()
        self.send_response(response.status_code, response.reason)
        self.handle_headers(response.headers)
        try:
            if not static_content:
                parsed_content = self.parse_content(content=response.text)
                self.wfile.write(parsed_content)
            else:
                self.wfile.write(response.content)
        except HTTPError as err:
            print(
                f"{get_time_stamp()} Request call was not successful, reason: [{err}]")

    def handle_headers(self, headers: str) -> None:
        """Method builds and sends headers to the client
        """
        self.send_header("Content-Type", headers["Content-Type"])  # type: ignore
        self.send_header('Proxy-Agent', 'Master Ultron')
        self.end_headers()

    def do_request(self) -> Tuple[Response, bool]:
        """Methods implements Requests module to defined "TARGET_URL"

        Returns:
            Response: Response object

            bool: if True static content skipped from modifying
        """
        response = Response
        url = f'{TARGET_URL}/{self.path[1:]}'
        static_content = bool(
            re.search(".js", self.path[1:]) or re.search(".css", self.path[1:]) or
            re.search(".gif", self.path[1:]) or re.search("favicon.ico", self.path[1:])
        )
        try:
            response = requests.get(url, headers=HEADERS)
        except HTTPError as err:
            print(
                f"{get_time_stamp()} Request call was not successful, reason: [{err}]")
        finally:
            return response, static_content

    def parse_content(self, content: str) -> bytes | Any:
        """Method parses html content to find all matching string
        using regex pattern and replace with new modified strings
        Args:
            content (str): Content of the response page
        Returns:
            bytes: new content in bytes
        """
        soup = BeautifulSoup(content, 'html.parser')
        try:
            for element in soup.find_all(text=True):
                split_el = re.split(r"(\W+)", element)
                new_element = "".join(self.append_TM(string) for string in split_el)
                element.replace_with(new_element)

            # find original "TARGET_URL" and replace with address of our proxy "(HOST:PORT)"
            for url in soup.find_all(href=f"{TARGET_URL}"):
                if url:
                    url['href'] = f"https://{HOST}:{PORT}"

        except Exception as error:
            print(f"{get_time_stamp()} Content parse unsuccessful, reason: [{error}]")
        finally:
            return soup.encode()

    def append_TM(self, string: str):
        """Method appends TradeMark logo -> (™)
            to words match with specified regex
        Args:
            string (str): target string
        Returns:
            str: modified string | original string
        """
        if "™" in string:
            string = re.sub("™", "", string)
        reg_ex = re.compile(r"(\b\w{6}\b)", re.IGNORECASE)
        try:
            match = reg_ex.match(string) or None
            match_string = match.group() if match is not None else str()
            if match_string.isalpha():
                return reg_ex.sub(f'{match_string}™', string, count=1)
            return string
        except RegexException as err:
            print(
                f"{get_time_stamp()} Regex error, invalid regular expression , reason: [{err}]")
