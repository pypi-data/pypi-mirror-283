"""Traefik certificate exporter CLI."""

import click

from .exceptions import CertExporterError
from .exporter import export_certificates

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("storage", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def export_certs(storage, output):
    """Export certificates from Traefik's STORAGE file to a specified OUTPUT directory.

    \b
    STORAGE is the location where Traefik saves the ACME certificates.
    OUTPUT is the path to a directory where the certificate files will be exported to.
    """
    try:
        export_certificates(storage, output)
    except CertExporterError as e:
        raise click.UsageError(str(e)) from e
