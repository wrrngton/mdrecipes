import click
from .build import build_book
from .init import init_book
from .serve import serve_book

@click.group()
def cli():
    pass

@click.command()
def init():
    init_book()

@click.command()
def build():
    build_book()

@click.command()
def serve():
    serve_book()

cli.add_command(init)
cli.add_command(build)
cli.add_command(serve)

if __name__ == "__main__":
    cli()
