import os
import aiohttp
from rich.console import Console
from rich.table import Table
import typer

from credio.config import store
from credio.util.type import lazy


DEFAULT_STORAGE_PATH = os.path.expanduser("~")
DEFAULT_CONFIG_FOLDER = ".credio"
DEFAULT_CREDENTIAL_FILE = "credentials"
DEFAULT_AUTH_TOKEN_KEY = "auth_token"
DEFAULT_GATEWAY_BASE_URL = "https://api.credio.network"
DEFAULT_IPFS_GATEWAY = "/dns/ipfs.credio.network/tcp/5001/http"


action = typer.Typer()


@action.command(name="show", help="Show this command-line tool configurations.")
def show():
    table = Table()
    table.add_column("Name", style="cyan")
    table.add_column("Value", style="yellow")
    table.add_column("Default", style="bright_black")
    table.add_row(
        "Credio Gateway URL", store.get("GATEWAY_BASE_URL"), DEFAULT_GATEWAY_BASE_URL
    )
    table.add_row("IPFS Gateway", store.get("IPFS_GATEWAY"), DEFAULT_IPFS_GATEWAY)
    storage_path = store.get("STORAGE_PATH") or DEFAULT_STORAGE_PATH
    table.add_row(
        "Credentials",
        os.path.join(storage_path, DEFAULT_CONFIG_FOLDER, DEFAULT_CREDENTIAL_FILE),
        os.path.join(storage_path, DEFAULT_CONFIG_FOLDER, DEFAULT_CREDENTIAL_FILE),
    )
    Console().print(table)
