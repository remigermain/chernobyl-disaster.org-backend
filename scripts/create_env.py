#!/usr/bin/python3
from django.core.management.utils import get_random_secret_key
import argparse
import re

REGEX = r"[\t ]+"
reg_space = re.compile(REGEX)


def main():
    env = {
        "DEBUG": True,
        "SECRET_KEY": f"\"{get_random_secret_key()}\"",
        "SITE_NAME": "",
        "DOMAIN_NAME": "",
        "SITE_URL": "http://localhost:8000",

        "EMAIL_HOST": "localhost",
        "EMAIL_PORT": 587,

        "SQL_DATABASE": "",
        "SQL_USER": "",
        "SQL_PASSWORD": "",
        "SQL_HOST": "",
        "SQL_PORT": "",
    }

    if flag.merge:
        with open(flag.input, "r") as f:
            _file = reg_space.sub(" ", f.read()).split("\n")
            for line in _file:
                _split = line.split("=")
                key = _split[0].strip()
                value = _split[1].strip() if len(_split) == 2 else None
                if key[:6] == "export":
                    key = key[6:].strip()
                if key in env and value:
                    env[key] = value

    with open(flag.output, "w") as f:
        for key, val in env.items():
            if flag.export:
                f.write(f"export {key}={val}\n")
            else:
                f.write(f"{key}={val}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate env files")
    parser.add_argument("-m", "--merge", action="store_true", help="open existing env file, if key with value exsit, do nothing", default=False)
    parser.add_argument("-o", "--output", help="set the outupt file name", default=".env")
    parser.add_argument("-i", "--input", help="set the input file name", default=".env")
    parser.add_argument("-e", "--export", action="store_true", help="ad export prefix", default=False)
    flag = parser.parse_args()
    main()
