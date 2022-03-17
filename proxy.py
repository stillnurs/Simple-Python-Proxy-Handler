import datetime
import http.server
import socketserver
import ssl
import sys
import time
import requests
import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

TARGET_URL = "https://news.ycombinator.com/"
HOST = '127.0.0.1'
PORT = 8080
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}

# timestamp function for logs.
def get_time_stamp():
    return f"{HOST} - - [{str(datetime.datetime.fromtimestamp(time.time()).strftime('%d/%b/%Y %H:%M:%S'))}]"


class Handler(http.server.BaseHTTPRequestHandler):
    """Request handler class

        Serves to capture incoming request stream and sends back to client 

        modified message from the targeted url.

    """

    def do_GET(self):
        self.handle_headers()
        self.modify_content()

    def handle_headers(self):
        self.send_response(200, "HTTP/1.1 Connection established")
        if '.css?' in self.path:
            self.send_header('Content-type', 'text/css')
        elif '.js?' in self.path:
            self.send_header('Content-type', 'application/javascript; ')
        elif '.gif' in self.path:
            self.send_header('Content-type', 'image/gif; ')
        elif '.ico' in self.path:
            self.send_header('Content-type', 'image/x-icon; ')
        
        else:
            self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Proxy-Agent', 'Ultron Jr')
        self.end_headers()

    def append_TM(self, content: list[str]):
        reg_ex = re.compile(r"^(\b\w{6}\b)$", re.IGNORECASE) # compile a pattern for our target string for our convenience
        new_content = []
        for string in content:
            if reg_ex.match(string): 
                match_string = reg_ex.match(string).group();
                if match_string.isalpha():
                    string = reg_ex.sub(f'{match_string}&#x2122;', string, count=1)
                    # print(reg_ex.sub('&#x2122;', match_string, count=1))
            if string == f'a href="{TARGET_URL}">':
                string = f'a href="https://{HOST}:{PORT}">'
            if string == 'href="favicon.ico">':
                string = f'href="{TARGET_URL}/favicon.ico">'
            if string == 'src="y18.gif"':
                string = f'src="{TARGET_URL}/y18.gif"'
            if string == 'href="news.css?HTgGcPawXJ5mMASvvCyk">':
                string = f'href="{TARGET_URL}/news.css?HTgGcPawXJ5mMASvvCyk">'
            if string == "src='hn.js?HTgGcPawXJ5mMASvvCyk'>":
                string = f'src="{TARGET_URL}/hn.js?HTgGcPawXJ5mMASvvCyk">'
            new_content.append(string)
        # print(new_content)
        return new_content

    def modify_content(self):
        url = TARGET_URL + self.path[1:]
        try:
            response = requests.get(url, headers=HEADERS)
            if response.headers['Content-Type'] == 'text/html; charset=utf-8':            
                split_html = re.split('(<[^>]*>|[\W]{1})', str(response.text))
                print()
                html_list = " ".join(split_html).strip().split(" ")
                print(html_list)
                modified_html = self.append_TM(html_list)
                result = re.sub('(?<=>) | (?=<)', '', " ".join(modified_html))
                self.wfile.write(
                    bytes(str(result), 'UTF-8'))
            else:  
                self.wfile.write(
                        bytes(str(response.text), 'UTF-8'))

                
        except Exception as err:
            print(f"{get_time_stamp()} Something went wrong...{err}")


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
