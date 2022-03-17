import datetime
import http.server
import socketserver
import ssl
import sys
import time
import requests
import re
from re import error as RegexException
from requests.models import Response
from requests.exceptions import HTTPError

TARGET_URL = "https://news.ycombinator.com"
HOST = '127.0.0.1'
PORT = 8080
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}

# timestamp function for logs.


def get_time_stamp():
    return f"{HOST} - - [{str(datetime.datetime.fromtimestamp(time.time()).strftime('%d/%b/%Y %H:%M:%S'))}]"


class Handler(http.server.BaseHTTPRequestHandler):
    """Request handler class

        Serves to capture incoming request stream and sends back to client 

        modified message from the targeted url.

    """

    def do_GET(self):
        response = self.do_request()
        self.send_response(response.status_code, response.reason)
        self.handle_headers(response.headers['content-type'])
        try:
            if modified_content := self.modify_content(content=response.text):
                self.wfile.write(modified_content)
            else:
                print(f"{get_time_stamp()} Content was not modified.")
                self.wfile.write(response.content)
        except HTTPError as error:
            print(f"{get_time_stamp()} Request call was not successful, reason: {error}")

    def handle_headers(self, content_type):
        self.send_header('Content-Type', content_type)
        self.send_header('Proxy-Agent', 'Master Ultron')
        self.end_headers()

    def do_request(self) -> Response:
        url = f'{TARGET_URL}/{self.path[1:]}'
        try:
            response: Response = requests.get(url, headers=HEADERS)
        except HTTPError as error:
            print(
                f"{get_time_stamp()} Request call was not successful, reason: {error}")
        return response

    def append_TM(self, string:str):
        """Function to append specified logo -> "TM"
            to words match with specified regex 
        Args:
            string (str): target word
        Returns:
            str: modified word
        """
        try:
            reg_ex = re.compile(r"^(\b\w{6}\b)|$", re.I)
            match_string = reg_ex.match(string).group() if reg_ex.match(string) else ""
            if match_string.isalpha():
                return reg_ex.sub(f'{match_string}&#x2122;', string, count=1)
        except RegexException:
            print(
                f"{get_time_stamp()} Regex error, invalid regular expression , reason: {error}")
        return string

    def modify_content_list(self, content_list: list[str]) -> list:
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
        return new_content_list

    def replace_urls(self, string):
        if string == f'href="{TARGET_URL}">':
            string = f'href="https://{HOST}:{PORT}">'
        if string == 'href="favicon.ico">':
            string = f'href="{TARGET_URL}/favicon.ico">'
        if string == 'src="y18.gif"':
            string = f'src="{TARGET_URL}/y18.gif"'
        if string == 'src="s.gif"':
            string = f'src="{TARGET_URL}/s.gif"'
        if string == 'href="news.css?HTgGcPawXJ5mMASvvCyk">':
            string = f'href="{TARGET_URL}/news.css?HTgGcPawXJ5mMASvvCyk">'
        if string == "src='hn.js?HTgGcPawXJ5mMASvvCyk'>":
            string = f'src="{TARGET_URL}/hn.js?HTgGcPawXJ5mMASvvCyk">'
        return string

    def modify_content(self, content):
        try:
            split_content = re.split('(<[^>]*>)', str(content))
            content_list = " ".join(split_content).split(" ")
            modified_content_list = self.modify_content_list(content_list)
            result = re.sub('(?<=>) | (?=<)', '',
                            " ".join(modified_content_list))
            modified_content = bytes(str(result), 'UTF-8')
        except Exception as error:
            print(f"{get_time_stamp()} Could not modify the content, reason: {error}")
        finally:
            return modified_content


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        context.load_cert_chain(certfile='./cert.pem',
                                keyfile='./cert_pkey.pem')
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
