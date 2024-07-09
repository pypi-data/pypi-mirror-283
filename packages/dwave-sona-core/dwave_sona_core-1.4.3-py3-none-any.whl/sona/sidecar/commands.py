import asyncio

import typer
from sona.worker.producers import create_producer

from .sidecars import Scanner

app = typer.Typer()
create_producer()


@app.command()
def run():
    scanner = Scanner()
    asyncio.run(scanner.scan_files())
