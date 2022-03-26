

from argparse import ArgumentError
import os
import socketserver
import ssl
import sys
import time

from src.socket_server.proxy import get_time_stamp, Handler
from utils import proxy_globals


def main():

    # Simple code that handles arguments to select a desired port.
    arguments = sys.argv
    if len(arguments) != 2:
        if os.name == "posix":
            print("""
            [Startup Error]
            
            Too few commandline arguments, should be 2

            usage: python[version(optional)] [./main.py] [PORT]
            """)
        elif os.name == "nt":
            print("""
            [Startup Error]

            Too few commandline arguments, should be 2

            usage: python[version(optional)] [main.py] [PORT]
            """)
        return
    PORT = 0
    try:
        HOST = proxy_globals.HOST
        PORT = int(arguments[-1])
        if ((PORT > 65535) or (PORT < 0)):
            print("Invalid port number, range of port number should be between 0 and 65535 yours were = ", PORT)
            return
    except:
        print("Invalid second argument, can't convert it into a valid portnumber == ", PORT)
        return
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        context.load_cert_chain(certfile='./docs/cert.pem',
                                keyfile='./docs/cert_pkey.pem')
        print(f"{get_time_stamp()} Starting server...")
        time.sleep(.5)
        with socketserver.ThreadingTCPServer(("", PORT), Handler) as handler:
            print(f"{get_time_stamp()} Connection established... ")
            time.sleep(.5)
            with context.wrap_socket(handler.socket, server_side=True) as handler.socket:
                print(f"{get_time_stamp()} Proxy-Server listening at [https://{HOST}:{PORT}]")
                time.sleep(.5)
                try:
                    handler.serve_forever()
                except Exception as error:
                    print(f"{get_time_stamp()} Something went wrong...")
                    print(
                        f"{get_time_stamp()} Program stopped, because of: [{error}]")

    except KeyboardInterrupt:
        print(f'{get_time_stamp()}   Interrupting Server.')
        time.sleep(.5)

    finally:
        print(f'{get_time_stamp()}   Stopping Server...')
        sys.exit()


if __name__ == "__main__":
    main()
