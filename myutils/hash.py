import hashlib


def sha256(string):
    """
    SHA-2 (Secure Hash Algorithm 2) is a set of cryptographic hash functions designed by the United States National Security Agency (NSA) and first published in 2001. They are built using the Merkle–Damgård construction, from a one-way compression function itself built using the Davies–Meyer structure from a specialized block cipher.
    """
    return hashlib.sha256(string.encode()).hexdigest()


def sha1(string):
    return hashlib.sha1(string.encode()).hexdigest()


def md5(string):
    return hashlib.md5(string.encode()).hexdigest()


def sha512(string):
    return hashlib.sha512(string.encode()).hexdigest()
