#!/usr/bin/env python
from datetime import datetime as dt
import logging
import pathlib
import frontmatter
import http.server
import os
import socketserver
import sys
from argparse import ArgumentParser, Namespace
from contextlib import suppress

from livereload import Server

from blog.build import build

# [TODO] Have live reload only rebuild the blog posts that have changed


def serve_handler(args: Namespace) -> None:
    if args.watch:
        server = Server()
        targets = ["posts/*.md", "templates/", "static/"]
        for target in targets:
            server.watch(target, "blog build")
        server.serve(root="public", open_url_delay=args.browser, port=args.port)
    else:
        os.chdir("public")
        Handler = http.server.SimpleHTTPRequestHandler
        logging.info(f"serving on port: {args.port}")
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", args.port), Handler) as httpd:
            with suppress(KeyboardInterrupt):
                httpd.serve_forever()
            httpd.shutdown()


def build_handler(args: Namespace) -> None:
    posts = build(args.drafts)
    logging.info(f"Built {len(posts)} posts")


def new_handler(args: Namespace) -> None:
    fpath = pathlib.Path(args.fname)
    with fpath.open("wb+") as f:
        metadata = {
            "title": fpath.stem,
            "date": dt.now().date(),
            "draft": True,
        }
        post = frontmatter.Post("", None, **metadata)
        frontmatter.dump(post, f)


def main() -> None:

    parser = ArgumentParser(prog="Blog")
    subparsers = parser.add_subparsers()

    # parser for the "build" command
    parser_new = subparsers.add_parser("new")
    parser_new.set_defaults(func=new_handler)
    parser_new.add_argument("fname")

    # parser for the "build" command
    parser_build = subparsers.add_parser("build")
    parser_build.add_argument(
        "-D", "--drafts", action="store_true", help="whether to include draft posts",
    )
    parser_build.add_argument(
        "-v", "--verbose", action="store_true", help="verbose",
    )
    parser_build.set_defaults(func=build_handler)

    # parser for the "serve" command
    parser_serve = subparsers.add_parser("serve")
    parser_serve.add_argument(
        "-b",
        "--browser",
        action="store_true",
        help="opens the site in a browser window",
    )
    parser_serve.add_argument(
        "-D", "--drafts", action="store_true", help="whether to include draft posts",
    )
    parser_serve.add_argument(
        "-p", "--port", action="store_true", help="port to serve on", default=8080
    )
    parser_serve.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="whether to watch files for changes",
        default=False,
    )
    parser_serve.add_argument(
        "-v", "--verbose", action="store_true", help="verbose",
    )
    parser_serve.set_defaults(func=serve_handler)

    logging.basicConfig(level=logging.INFO)

    # Dispatch to the corresponding handler
    args = parser.parse_args()

    # Set verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if vars(args):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(0)
