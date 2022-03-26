"""
    Global variables defined for poject use.
"""
import sys

HOST = '127.0.0.1'
PORT = sys.argv[-1]
TARGET_URL = "https://news.ycombinator.com"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
