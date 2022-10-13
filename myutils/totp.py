import pyotp


def get_random_secret():
    return pyotp.random_base32()


def get_totp(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()


def verify_totp(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)


if __name__ == '__main__':
    secret = 'base32secret3232'
    print(secret)
    uri = pyotp.totp.TOTP(secret).provisioning_uri("myuser")
    print(uri)
    print(get_totp(secret))
    print(verify_totp(secret, get_totp(secret)))
