import click

# from .add_url import add_url
# from .build import build_book
from .init import init_book
# from .serve import serve_book


@click.group()
def cli():
    pass


@click.command()
def init():
    init_book()


# @click.command()
# def build():
#     build_book()
#
#
# @click.command()
# def serve():
#     serve_book()
#

# @click.command()
# @click.option("-u", "--url", type=str, required=True)
# @click.option("-f", "--filename", type=str, required=True)
# @click.option("-c", "--category", type=str)
# @click.option("-t", "--tags", type=str)
# def add(url, filename, category, tags):
#     add_url(url, filename, category, tags)


cli.add_command(init)
# cli.add_command(build)
# cli.add_command(serve)
# cli.add_command(add)

if __name__ == "__main__":
    cli()
