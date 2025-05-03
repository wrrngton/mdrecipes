from setuptools import setup, find_packages

setup(
    name="mdrecipes",
    version="0.1",
    packages=find_packages(),
    install_requires=["click", "toml", "Jinja2", "setuptools", "markdown", "livereload", "frontmatter", "validators", "beautifulsoup4"],
    entry_points={
        "console_scripts": [
            "mdrecipes=cli.__main__:cli",
        ],
    },
)

