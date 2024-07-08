"""File handlers for Traefik certificate exporter."""
import json

from .exceptions import CertExporterError


def get_file_content(path: str) -> dict:
    """Read the content of a JSON file and return it as a dictionary.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file as a dictionary.

    Raises:
        CertExporterError: If the file is not a valid JSON file.
    """
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError as e:
            raise CertExporterError('Invalid JSON file') from e
