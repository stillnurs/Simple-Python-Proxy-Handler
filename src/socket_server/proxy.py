import datetime
import http.server
import socketserver
import ssl
import sys
import time
import re
import requests  # type: ignore
from re import error as RegexException
from requests import Response, HTTPError


TARGET_URL = "http://example.com"
HOST = '127.0.0.1'
PORT = 8080
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}

# timestamp function for logs.


def get_time_stamp():
    return f"{HOST} - - [{str(datetime.datetime.fromtimestamp(time.time()).strftime('%d/%b/%Y %H:%M:%S'))}]"


class Handler(http.server.BaseHTTPRequestHandler):
    """Request handler class

        Serves the client with identified http request
        by modifying the outgoing response data.
    """

    def do_GET(self):
        response = self.do_request()
        self.send_response(response.status_code, response.reason)
        self.handle_headers(response.headers['content-type'])
        try:
            split_content = self.split_content(content=response.text)
            modified_content = self.modify_content_list(split_content)
            if new_content := self.compose_new_content(modified_content):
                self.wfile.write(new_content)
            else:
                print(f"{get_time_stamp()} Content was not modified.")
                self.wfile.write(response.content)
        except HTTPError as error:
            print(
                f"{get_time_stamp()} Request call was not successful, reason: {error}")

    def handle_headers(self, content_type: str) -> None:
        """Function to handle build and send headers back to the client
        """
        self.send_header('Content-Type', content_type)
        self.send_header('Proxy-Agent', 'Master Ultron')
        self.end_headers()

    def do_request(self) -> Response:
        """Functions makes a request to defined TARGET_URL
           and returns a Response object
        Returns:
            Response: Response object
        """
        url = f'{TARGET_URL}/{self.path[1:]}'
        try:
            response: Response = requests.get(url, headers=HEADERS)
        except HTTPError as error:
            print(
                f"{get_time_stamp()} Request call was not successful, reason: {error}")
        return response

    def split_content(self, content: str) -> list:
        """Function to spli content to list of strings using regex pattern
        Args:
            content (str): Content of the response page

        Returns:
            list: Splitted list of strings
        """
        try:
            # split to list strings of the content using regex pattern and built-in Python module "re"
            # pattern helps to separate the html tags from its child text           
            content_splitted = re.split('(<[^>]*>)', content)
            content_list = "".join(content_splitted).split(" ")
            print(content_list)
        except Exception as error:
            print(f"{get_time_stamp()} Content splitting unsuccessful, reason: {error}")
        finally:
            return content_list
    
    def modify_content_list(self, content_list: list[str]) -> list[str]:
        """Compile new list from html page contents
            modifying targeted words
        Args:
            content_list (list[str]): original list of contents
        Returns:
            list: new modified list of contents
        """
        new_content_list = []
        try:
            for string in content_list:
                if len(string) >= 6:
                    string = self.append_TM(string)
                string = self.replace_urls(string)
                new_content_list.append(string)
        except Exception as error:
            print(
                f"{get_time_stamp()} Request call was not successful, reason: {error}")
        finally:
            return new_content_list
    
    def compose_new_content(self, new_content_list) -> bytes:
        try:
            result = re.sub('(?<=>) | (?=<)', '',
                            " ".join(new_content_list))
            new_content = bytes(str(result), 'UTF-8')
        except Exception as error:
            print(f"{get_time_stamp()} Could not modify the content, reason: {error}")
        finally:
            return new_content

    def append_TM(self, string: str):
        """Function to append TradeMark logo -> (&#x2122;)
            to words match with specified regex
        Args:
            string (str): target word
        Returns:
            str: modified word
        """
        try:
            reg_ex = re.compile(r"^(\b\w{6}\b)|$", re.I)
            match = reg_ex.match(string) or None
            match_string = match.group() if match is not None else str()
            if match_string.isalpha():
                return reg_ex.sub(f'{match_string}&#x2122;', string, count=1)
        except RegexException as error:
            print(
                f"{get_time_stamp()} Regex error, invalid regular expression , reason: {error}")
        return string

    def replace_urls(self, url):
        """Function to replace existing attributes
            default URL values, to make sure static files served from
            original source, not from localhost.

        Args:
            string (str): URL string

        Returns:
            str: modified URL string
        """
        if url == f'href="{TARGET_URL}">':
            url = f'href="https://{HOST}:{PORT}">'
        if url == 'href="favicon.ico">':
            url = f'href="{TARGET_URL}/favicon.ico">'
        if url == 'src="y18.gif"':
            url = f'src="{TARGET_URL}/y18.gif"'
        if url == 'src="s.gif"':
            url = f'src="{TARGET_URL}/s.gif"'
        if url == 'href="news.css?HTgGcPawXJ5mMASvvCyk">':
            url = f'href="{TARGET_URL}/news.css?HTgGcPawXJ5mMASvvCyk">'
        if url == "src='hn.js?HTgGcPawXJ5mMASvvCyk'>":
            url = f'src="{TARGET_URL}/hn.js?HTgGcPawXJ5mMASvvCyk">'
        return url

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        context.load_cert_chain(certfile='../../docs/cert.pem',
                                keyfile='../../docs/cert_pkey.pem')
        print(f"{get_time_stamp()} Starting server...")
        time.sleep(.5)
        with socketserver.ThreadingTCPServer(("", PORT), Handler) as handler:
            print(f"{get_time_stamp()} Connection established... ")
            time.sleep(.5)
            with context.wrap_socket(handler.socket, server_side=True) as handler.socket:
                print(f"{get_time_stamp()} Server listening at port [{PORT}]")
                time.sleep(.5)
                try:
                    handler.serve_forever()
                except Exception as error:
                    print(f"{get_time_stamp()} Something went wrong...")
                    print(
                        f"{get_time_stamp()} Program stopped, because of: {error}")

    except KeyboardInterrupt:
        print(f'{get_time_stamp()}   Interrupting Server.')
        time.sleep(.5)

    finally:
        print(f'{get_time_stamp()}   Stopping Server...')
        sys.exit()
