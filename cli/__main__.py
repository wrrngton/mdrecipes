import click
from .build import build_book
from .init import init_book
from .serve import serve_book
from .add import add_recipes

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

@click.command()
@click.option('-u', '--url', type=str, required=True)
def add(url):
    add_recipes(url)

cli.add_command(init)
cli.add_command(build)
cli.add_command(serve)
cli.add_command(add)

if __name__ == "__main__":
    cli()
