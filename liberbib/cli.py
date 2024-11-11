import pathlib
from .library_manager import LibraryManager
import click

_DEFAULT_CACHE_FILE = pathlib.Path("~/.config/liberbib/cache.json").expanduser()


@click.group()
@click.option(
    "--cache", type=str, help="Use a specific cache file", default=_DEFAULT_CACHE_FILE
)
@click.option("--nocache", "-n", is_flag=True, help="Do not use cache")
@click.pass_context
def cli(ctx, nocache, cache):
    ctx.ensure_object(dict)
    ctx.obj["nocache"] = nocache
    ctx.obj["cache"] = cache
    ctx.obj["libmgr"] = LibraryManager(cache_file=cache, use_cache=not nocache)


@cli.command()
@click.argument("search_term", type=str, required=True)
@click.option("--bibtex", "-b", is_flag=True, help="Output in bibtex format")
@click.pass_context
def search(ctx, search_term: str, bibtex: bool):
    libmgr = ctx.obj["libmgr"]
    work = libmgr.get_work_by_search(search_term)
    if bibtex:
        click.echo(work.to_bibtex())
    else:
        click.echo(work)


@cli.command()
def dropdb():
    click.echo("Dropped the database")
