"""Traefik certificate exporter."""

import os

from .exceptions import CertExporterError
from .handlers import get_file_content
from .models import Provider


def get_providers(file_path: str) -> list[Provider]:
    """A function that retrieves providers from a file path, converts the contents to a list of
    Provider objects, and filters out values where both the "Account" and "Certificates" keys are
    present.

    Args:
        file_path (str): The path to the file containing provider information.

    Returns:
        list[Provider]: A list of Provider objects extracted from the file contents.

    Raises:
        CertExporterError: If no providers with a valid account and certificates are found in the
        storage file.
    """
    contents = get_file_content(file_path)

    providers = [
        Provider.from_dict(value)
        for value in contents.values()
        if all([value["Account"], value["Certificates"]])
    ]
    if len(providers) == 0:
        msg = "No providers with a valid account and certificates found in storage file"
        raise CertExporterError(msg)
    return providers


def export_certificates(file_path: str, output_dir_path: str):
    """Export certificates from a file to a specified output directory.

    Args:
        file_path (str): The path to the file containing provider information.
        output_dir_path (str): The path to the directory where the certificates will be exported.

    Raises:
        CertExporterError: If the output directory is not a valid directory.
    """
    providers = get_providers(file_path)

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    if not os.path.isdir(output_dir_path):
        raise CertExporterError("Output path is not a directory")

    for provider in providers:
        for cert in provider.certificates:
            path = os.path.join(output_dir_path, cert.domain.main.replace("*", "_"))
            os.makedirs(path, exist_ok=True)

            cert_tuple = cert.decoded_single_certs
            file_mapping = {
                "privkey": cert.decoded_key,
                "fullchain": cert.decoded_full_chain,
                "cert": cert_tuple[0],
                "chain": b"".join(cert_tuple[1:]),
            }

            for key, value in file_mapping.items():
                with open(os.path.join(path, f"{key}.pem"), "wb") as f:
                    f.write(value)
