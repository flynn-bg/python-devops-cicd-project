import logging
import click
from typing import Collection

from .checker import check_urls

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@click.command()
@click.argument("urls", nargs=-1)
@click.option("--timeout", default=5, help="Timeout in seconds for each request.")
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
def main(urls: Collection, timeout: int, verbose: bool):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose Logging Enabled")

    logger.debug(f"Received urls: {urls}")
    logger.debug(f"Received timeout: {timeout}")
    logger.debug(f"Received verbose: {verbose}")

    if not urls:
        logger.warning("NoURLs provided to check")
        click.echo("Usages: chech-urls <URL1> <URL2> ..")
        return

    logger.info(f"Starting check for {len(urls)}")

    results = check_urls(urls, timeout)

    click.echo("\n---Results---")
    for url, status in results.items():
        if "OK" in status:
            click.secho(f"{url}:<40 -> {status}", fg="green")
        else:
            click.secho(f"{url}:<40 -> {status}", fg="red")
