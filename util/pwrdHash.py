from bcrypt import hashpw, checkpw, gensalt, kdf
from typing import Union, Optional
from base64 import b64encode, urlsafe_b64encode, urlsafe_b64decode
from hashlib import sha256
from cryptography.fernet import Fernet
from os import urandom


def _enforceUTF8(s: Union[bytes, str]) -> bytes:

    if type(s) is bytes:
        pass
    elif type(s) is str:
        s = s.encode("utf8")
    else:
        raise TypeError

    return s


def hashPassword(pwrd: Union[bytes, str], level: Optional[int] = 12) -> bytes:
    """Generates a hash of the given password.

    Args:
        pwrd (Union[bytes, str]): The password to be hashed.
        level (Optional[int], optional): The work factor required.
            The minimum allowed value is 5.
            It is recommended that a value lower than 18 is used.
            Defaults to 12.

    Returns:
        bytes: A forward hash.
    """
    b64Pwrd = b64encode(sha256(_enforceUTF8(pwrd)).digest())
    encryptedPwrd = hashpw(b64Pwrd, gensalt(rounds=level))
    return encryptedPwrd


def checkPassword(testStr: Union[bytes, str], encPwrd: bytes) -> bool:
    """Verifies if a given password matches the correct hash. 

    Args:
        testStr (Union[bytes, str]): The password to be tested.
        encPwrd (bytes): The hash corresponding to the correct password.

    Returns:
        bool: True if the password was correct, otherwise False.
    """
    b64Pwrd = b64encode(sha256(_enforceUTF8(testStr)).digest())
    result = checkpw(b64Pwrd, encPwrd)
    return result


def encryptSecret(pwrd: bytes, secret: Union[bytes, str]) -> str:
    """Encrypts a given secret string using Fernet.

    Args:
        pwrd (bytes): The bcrypt hash of the master password.
        secret (bytes): A plaintext secret.

    Returns:
        str: A URL-safe B64 encoded string.
    """

    # * Length of the salt here affects the prefix of the resultant secret
    salt = urandom(60)

    key = kdf(pwrd, salt, 32, 2000)
    key = urlsafe_b64encode(key)
    fnet = Fernet(key)

    encryptedSecret = fnet.encrypt(_enforceUTF8(secret))

    # ? Is this additional b64encode actually needed?
    encryptedSecret = urlsafe_b64encode(urlsafe_b64encode(salt) + encryptedSecret)

    return encryptedSecret.decode("utf8")


def decryptSecret(pwrd: bytes, secret: Union[bytes, str]) -> str:
    """Decrypts an encrypted secret.

    Args:
        pwrd (bytes): The bcrypt hash of the master password.
        secret (Union[bytes, str]): An encrypted secret.

    Returns:
        str: A decrypted, plaintext secret.
    """

    secret = urlsafe_b64decode(secret)
    # * The length of the prefixed salt depends on the initial length of the salt
    salt = urlsafe_b64decode(secret[:80])

    key = kdf(pwrd, salt, 32, 2000)
    key = urlsafe_b64encode(key)
    fnet = Fernet(key)
    decryptedSecret = fnet.decrypt(secret[80:])
    return decryptedSecret.decode("utf8")
