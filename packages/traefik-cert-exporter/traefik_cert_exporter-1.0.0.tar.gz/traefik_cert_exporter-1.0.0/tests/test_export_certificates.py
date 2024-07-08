"""Unit tests for the `export_certificates` function."""

import json
import os
from base64 import b64encode

import pytest

from src.traefik_cert_exporter import export_certificates


@pytest.fixture(name="mock_file_path")
def fixture_mock_file_path(tmpdir):
    """Fixture that creates a temporary file with mock ACME data and returns its path.

    Args:
        tmpdir (py.path.local): The temporary directory object.

    Returns:
        pathlib.Path: The path to the temporary file.
    """
    certs = b"-----BEGIN CERTIFICATE-----\nCERTIFICATE\n-----END CERTIFICATE-----\n" * 3
    key = b"-----BEGIN PRIVATE KEY-----\nKEY\n-----END PRIVATE KEY-----"

    acccount = {
        "Email": "user@example.com",
        "Registration": {
            "body": {
                "status": "valid",
                "contact": ["mailto:user@example.com"],
            },
            "uri": "https://acme-staging-v02.api.letsencrypt.org/acme/acct/103657894",
        },
        "PrivateKey": "PRIVATE_KEY",
        "KeyType": "4096",
    }

    certificates1 = [
        {
            "domain": {"main": "*.example.com", "sans": ["example.com"]},
            "certificate": b64encode(certs).decode(),
            "key": b64encode(key).decode(),
            "Store": "default",
        }
    ]

    certificates2 = [
        {
            "domain": {"main": "example.org"},
            "certificate": b64encode(certs).decode(),
            "key": b64encode(key).decode(),
            "Store": "default",
        },
        {
            "domain": {"main": "example.net"},
            "certificate": b64encode(certs).decode(),
            "key": b64encode(key).decode(),
            "Store": "default",
        },
        {
            "domain": {"main": "example.io"},
            "certificate": b64encode(certs).decode(),
            "key": b64encode(key).decode(),
            "Store": "default",
        },
    ]

    acme = {
        "provider1": {
            "Account": acccount,
            "Certificates": certificates1,
        },
        "provider2": {
            "Account": acccount,
            "Certificates": certificates2,
        },
    }

    path = tmpdir.join("acme.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(acme, f, indent=2)

    return path


@pytest.fixture(name="tmp_output")
def fixture_tmp_output(tmpdir):
    """Generate a string representing the path to a temporary output directory.

    Args:
        tmpdir (py.path.local): The temporary directory object.

    Returns:
        str: The path to the output directory as a string.
    """
    return str(tmpdir.join("output"))


def test_create_output_dir(mock_file_path, tmp_output):
    """Test case to verify that the `export_certificates` function creates the output directory.

    Args:
        mock_file_path (str): The path to the mock file.
        tmpdir (py.path.local): The temporary directory object.
    """
    export_certificates(mock_file_path, tmp_output)

    assert os.path.isdir(tmp_output)


def test_write_certificates_to_files(mock_file_path, tmp_output):
    """Test case to verify that the `export_certificates` function successfully writes certificates
    to files in the specified output directory.

    Args:
        mock_file_path (str): The path to the mock file.
        tmp_output (str): The temporary output directory path.
    """
    export_certificates(mock_file_path, tmp_output)

    assert os.path.exists(os.path.join(tmp_output, "_.example.com", "privkey.pem"))
    assert os.path.exists(os.path.join(tmp_output, "_.example.com", "fullchain.pem"))
    assert os.path.exists(os.path.join(tmp_output, "_.example.com", "cert.pem"))
    assert os.path.exists(os.path.join(tmp_output, "_.example.com", "chain.pem"))

    assert os.path.exists(os.path.join(tmp_output, "example.org", "privkey.pem"))
    assert os.path.exists(os.path.join(tmp_output, "example.org", "fullchain.pem"))
    assert os.path.exists(os.path.join(tmp_output, "example.org", "cert.pem"))
    assert os.path.exists(os.path.join(tmp_output, "example.org", "chain.pem"))

    assert os.path.exists(os.path.join(tmp_output, "example.net", "privkey.pem"))
    assert os.path.exists(os.path.join(tmp_output, "example.net", "fullchain.pem"))
    assert os.path.exists(os.path.join(tmp_output, "example.net", "cert.pem"))
    assert os.path.exists(os.path.join(tmp_output, "example.net", "chain.pem"))

    assert os.path.exists(os.path.join(tmp_output, "example.io", "privkey.pem"))
    assert os.path.exists(os.path.join(tmp_output, "example.io", "fullchain.pem"))
    assert os.path.exists(os.path.join(tmp_output, "example.io", "cert.pem"))
    assert os.path.exists(os.path.join(tmp_output, "example.io", "chain.pem"))
