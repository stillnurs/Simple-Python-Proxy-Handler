import datetime
import http.server
import socketserver
import ssl
import sys
import time
import requests
import re

TARGET_URL = "https://news.ycombinator.com/"
HOST = '127.0.0.1'
PORT = 8080


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
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Proxy-Agent', 'Ultron Jr')
        self.end_headers()

    def modify_content(self):
        url = TARGET_URL + self.path[1:]
        html = requests.get(url)
        split_html = re.split('(<[^>]*>)', html.text)
        html_list = [i for i in " ".join(split_html).split(" ")]
        result = []
        try:
            for item in html_list:
                if len(item) == 6 and item.isalpha():
                    item = item + "&#x2122;"
                result.append(item)
            self.wfile.write(bytes(re.sub('(?<=>) | (?=<)', '', " ".join(result)), 'UTF-8'))
        except Exception as err:
            print(f"{get_time_stamp()} Something went wrong...{err}")


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        context.load_cert_chain(certfile='./cert.pem', keyfile='./cert_pkey.pem')
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
                    print(f"{get_time_stamp()} Program stopped, because of: {error}")

    except KeyboardInterrupt:
        print(f'{get_time_stamp()}   Interrupting Server.')
        time.sleep(.5)

    finally:
        print(f'{get_time_stamp()}   Stopping Server...')
        sys.exit()
