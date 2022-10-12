# Detect Vercel environment

import os


def isVercel():
    # Get all environment variables
    env = os.environ
    # Check if keyword "VERCEL" is in the environment variables
    for key in env:
        if "VERCEL" in key:
            return True
    return False
