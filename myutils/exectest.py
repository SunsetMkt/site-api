# Exec API Testing Utility
# /api/v1/exec
import pyotp
import requests

from . import keybase

# API URL
url = "https://api.lwd-temp.top/api/v1/exec"

# API Keys
api_key = "API_KEY"
totp_key = "TOTP_KEY"


def send_request(code):
    # TOTP
    totp = pyotp.TOTP(totp_key)
    totp_token = totp.now()

    # Args
    args = {
        "pass": api_key,
        "totp": totp_token,
        'jsonerror': 1
    }

    # Req args: args
    # Req body: code
    r = requests.post(url, data=code, params=args)

    return r


def get_code():
    import os
    import subprocess
    import tempfile
    from pathlib import Path
    if os.name == "nt":
        # Create a tmp file, open with notepad, wait user save and close, get code, delete file

        # Create tmp file with random name
        tmp_file = Path(tempfile.gettempdir(
        )) / Path(tempfile.gettempprefix() + next(tempfile._get_candidate_names()))

        print(tmp_file)
        with open(tmp_file, "w") as f:
            f.write("print('Hello World')")

        # Open with notepad and wait until the process exits
        ntp = subprocess.Popen(["notepad.exe", tmp_file])
        ntp.wait()

        # Get code
        with open(tmp_file, "r") as f:
            code = f.read()

        # Delete file
        os.remove(tmp_file)
    elif os.name == "posix":
        # Create a tmp file, open with deafult cli editor, wait user save and close, get code, delete file

        # Create tmp file with random name
        tmp_file = Path(tempfile.gettempdir(
        )) / Path(tempfile.gettempprefix() + next(tempfile._get_candidate_names()))

        print(tmp_file)
        with open(tmp_file, "w") as f:
            f.write("print('Hello World')")

        # Open with deafult cli editor and wait until the process exits
        ntp = subprocess.Popen(["xdg-open", tmp_file])
        ntp.wait()

        # Get code
        with open(tmp_file, "r") as f:
            code = f.read()

        # Delete file
        os.remove(tmp_file)
    else:
        # Get code from input
        print("Please input code:")
        code = input()

    return code


def main():
    global api_key, totp_key

    # Get api_key
    print("Please input api_key:")
    api_key = input()

    # Get totp_key
    print("Please input totp_key:")
    totp_key = keybase.TOTP_KEY

    while True:
        # Get code
        code = get_code()

        # Send request
        r = send_request(code)

        # Print response
        print(r.status_code)
        print(r.text)

        # Wait for user input
        print("Press Enter to continue, or input 'q' to quit")
        if input() == "q":
            break


if __name__ == "__main__":
    main()
