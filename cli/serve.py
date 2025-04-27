import os
import socketserver
from functools import partial
from http.server import (BaseHTTPRequestHandler, HTTPServer,
                         SimpleHTTPRequestHandler)

import click

from .build import build_book
from .helpers.load_config import get_user_config

PORT = 1234
PATHS = ["/style.css", "/lunr.js", "/script.js"]


def serve_book():

    click.echo("Starting local server...")

    book_root_dir = get_user_config()["book"]["directory"]
    book_static_dir = os.path.join(book_root_dir, "book")

    class CustomHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path not in PATHS:
                build_book()
            super().do_GET()

    handler = partial(CustomHandler, directory=book_static_dir)
    httpd = HTTPServer(("localhost", PORT), handler)

    click.echo(f"serving at http://localhost:{PORT}")
    httpd.serve_forever()
