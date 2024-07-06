import subprocess
import sys
import urllib.request
from typing import Optional

import click
from loguru import logger


@click.command()
@click.option(
    "--access-key",
    help="access key to install",
)
@click.option(
    "--version",
    default="latest",
    help="version to install",
)
@click.option(
    "--yes",
    is_flag=True,
    help="install without confirmation",
)
@click.option(
    "--list-versions",
    is_flag=True,
    help="list available versions",
)
def install_toolkit_pro(
    access_key: Optional[str], version: str, yes: bool, list_versions: bool
):
    """Install Toolkit Pro.

    Examples:

     \b
     $ labelmetk install-toolkit-pro  # install latest
     $ labelmetk install-toolkit-pro --version 1.0.0
     $ labelmetk install-toolkit-pro --access-key xxxxxxxx

    """
    logger.info("Installing the Labelme Toolkit Pro...")

    url_path = "https://toolkit-pro.labelme.io"

    with urllib.request.urlopen(f"{url_path}/versions") as response:
        data = response.read()
        versions = [version.strip() for version in data.decode("utf-8").splitlines()]

    if list_versions:
        for i, version in enumerate(versions):
            click.echo(version)
        return

    logger.info(f"Available versions: {versions}")

    if version == "latest":
        version = versions[-1]
        logger.info(f"Installing version: {version} (latest)")
    elif version not in versions:
        logger.error(f"Version {version} is not available")
        return
    else:
        logger.info(f"Installing version: {version}")

    if access_key is None:
        access_key = click.prompt("Enter access key")

    if not yes:
        if not click.confirm("Do you want to install?"):
            click.echo("Installation is canceled.")
            return

    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        f"{url_path}/{access_key}/labelme_toolkit_pro-{version}-py3-none-any.whl",
    ]
    logger.info(" ".join(cmd))
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        logger.error("Failed to install. Is the access key correct?")
        return
