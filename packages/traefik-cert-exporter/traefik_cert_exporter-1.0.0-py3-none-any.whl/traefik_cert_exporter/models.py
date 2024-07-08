"""Traefik certificate exporter models."""

import base64
from abc import ABC


class Model(ABC):
    """A base class representing a model object.

    This class is intended to be subclassed by concrete model classes. It is an abstract base class
    and cannot be instantiated directly.
    """

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self) -> None:
        raise NotImplementedError("Subclass must implement __str__()")


class Registration(Model):  # pylint: disable=too-few-public-methods
    """Represents a registration object with a body and a URI."""

    def __init__(self, body: dict, uri: str):
        self.body = body
        self.uri = uri

    def __str__(self) -> str:
        return f"body={self.body}, uri={self.uri}"


class Account(Model):
    """Represents an account object with email, registration details, private key, and key type."""

    def __init__(self, email: str, registration: dict, private_key: str, key_type: str):
        self.email = email
        self.registration = Registration(**registration)
        self.private_key = private_key
        self.key_type = key_type

    def __str__(self) -> str:
        return self.email

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        """A class method to create an Account instance from a dictionary containing email,
        registration details, private key, and key type.

        Args:
            data (dict): A dictionary containing the necessary data to create an Account instance.

        Returns:
            Account: An instance of the Account class
        """
        return cls(
            email=data["Email"],
            registration=data["Registration"],
            private_key=data["PrivateKey"],
            key_type=data["KeyType"],
        )


class Domain(Model):  # pylint: disable=too-few-public-methods
    """Represents a domain with a main domain and a list of sans domains."""

    def __init__(self, main: str, sans: list[str] = None):
        self.main = main
        self.sans = sans

    def __str__(self) -> str:
        return self.main


class Certificate(Model):
    """Represents a certificate with associated domain, certificate, and key."""

    def __init__(self, domain: dict, certificate: str, key: str, store: str):
        """Initialize the Certificate object with the provided domain, certificate, and key.

        Args:
            domain (dict): The domain associated with the certificate.
            certificate (str): The certificate string.
            key (str): The key string.
        """
        self.domain = Domain(**domain)
        self.certificate = certificate
        self.key = key
        self.store = store

    def __str__(self) -> str:
        return str(self.domain)

    @classmethod
    def from_dict(cls, data: dict) -> "Certificate":
        """A class method to create a Certificate instance from a dictionary containing domain,
        certificate, key, and store information.

        Args:
            data (dict): A dictionary containing the necessary data to create a Certificate
            instance.

        Returns:
            Certificate: An instance of the Certificate class
        """
        return cls(
            domain=data["domain"],
            certificate=data["certificate"],
            key=data["key"],
            store=data["Store"],
        )

    @property
    def decoded_full_chain(self) -> bytes:
        """Certificate attribute decoded as bytes."""
        return base64.b64decode(self.certificate)

    @property
    def decoded_single_certs(self) -> tuple[bytes]:
        """Tuple of bytes representing individual certificates in the decoded full chain"""
        separator = b"-----BEGIN CERTIFICATE-----"
        single_certs = self.decoded_full_chain.split(separator)
        return tuple(separator + c for c in single_certs if c)

    @property
    def decoded_key(self) -> bytes:
        """Certificate key attribute decoded as bytes."""
        return base64.b64decode(self.key)


class Provider(Model):
    """Represents a provider of certificates."""

    account: Account
    certificates: list[Certificate]

    def __init__(self, account: dict, certificates: list):
        self.account = Account.from_dict(account)
        if not certificates is None:
            certificates = [Certificate.from_dict(cert) for cert in certificates]
        self.certificates = certificates

    def __str__(self) -> str:
        return f"account={self.account}, certificates={self.certificates}"

    @classmethod
    def from_dict(cls, data: dict) -> "Provider":
        """Create a Provider instance from a dictionary containing account and certificates data.

        Args:
            data (dict): A dictionary containing the necessary data to create a Provider instance.
                It should have the following keys:
                - "Account" (dict): The account data for the Provider.
                - "Certificates" (list): The list of certificates for the Provider.

        Returns:
            Provider: An instance of the Provider class.
        """
        return cls(account=data["Account"], certificates=data["Certificates"])
