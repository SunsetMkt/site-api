# Detect Vercel environment

import os


def isVercel():
    # Check if linux
    if os.name == 'posix':
        # Get all environment variables
        env = os.environ
        # Check if keyword "VERCEL" is in the environment variables
        for key in env:
            if "VERCEL" in key:
                return True
        # Check if "/var/task/vercel.json" exists
        if os.path.exists("/var/task/vercel.json"):
            return True
    else:
        return False

    return False
