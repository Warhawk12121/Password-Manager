from bcrypt import hashpw, checkpw, gensalt
from typing import Union, Optional
from base64 import b64encode, b64decode
from hashlib import sha256


def _enforceUTF8(s: Union[bytes, str]) -> bytes:
    if type(s) is bytes:
        pass
    elif type(s) is str:
        s = s.encode("utf8")
    else:
        raise TypeError

    return s


def hashPassword(pwrd: bytes, level: Optional[int] = 12) -> bytes:
    """Generates a hash of the given password.

    Args:
        pwrd (bytes): The password to be hashed.
        level (Optional[int], optional): The work factor required.
            The minimum allowed value is 5.
            It is recommended that a value lower than 18 is used.
            Defaults to 12.

    Returns:
        bytes: A forward hash.
    """
    b64Pwrd = b64encode(sha256(pwrd).digest())
    encryptedPwrd = hashpw(b64Pwrd, gensalt(rounds=level))
    return encryptedPwrd


def checkPassword(testStr: bytes, encPwrd: bytes) -> bool:
    """Verifies if a given password matches the correct hash. 

    Args:
        testStr (bytes): The password to be tested.
        encPwrd (bytes): The hash corresponding to the correct password.

    Returns:
        bool: True if the password was correct, otherwise False.
    """
    b64Pwrd = b64encode(sha256(testStr).digest())
    result = checkpw(b64Pwrd, encPwrd)
    return result
