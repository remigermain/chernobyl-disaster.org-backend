#!/usr/bin/python3
import argparse
import re
import secrets
import os


def get_random_secret_key():
    allowed_char = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(allowed_char) for i in range(50))


REGEX = r"[\t ]+"
reg_space = re.compile(REGEX)


def main():
    env = {
        "DEBUG": True,
        "SECRET_KEY": f"\"{get_random_secret_key()}\"",
        "DOMAIN_NAME": "",
        "FRONTEND_URL": "http://localhost:3000",
        "DEBUG_TOOLBAR": False,
        "SUFFIX_ADMIN": "",
        "GPG_KEY": "",

        "ADMIN_USERNAME": "",

        "EMAIL_HOST": "postfix",
        "EMAIL_PORT": 587,

        "ALLOWED_HOSTS": "",
        "CORS_ALLOWED_ORIGINS": "",

        "POSTGRES_ENGINE": "django.db.backends.postgresql",
        "POSTGRES_NAME": "",
        "POSTGRES_DB": "",
        "POSTGRES_USER": "",
        "POSTGRES_PASSWORD": "",
        "POSTGRES_HOST": "",
        "POSTGRES_PORT": "",
    }

    if flag.merge and os.path.exists(flag.input) and os.path.isfile(flag.input):
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

    # add/replace new flag
    for n in flag.other:
        _split = n.split("=")
        if len(_split) != 2:
            print(f"wrong flag value {_split}")
            exit(0)
        env[_split[0]] = _split[1]

    with open(flag.output, "w") as f:
        for key, val in env.items():
            if flag.export:
                f.write(f"export {key}={val}\n")
            else:
                f.write(f"{key}={val}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate env files")
    parser.add_argument("-m", "--merge", action="store_true", help="open existing env file, if key with value exsit, do nothing", default=True)
    parser.add_argument("-o", "--output", help="set the outupt file name", default=".env")
    parser.add_argument("-i", "--input", help="set the input file name", default=".env")
    parser.add_argument("-e", "--export", action="store_true", help="ad export prefix", default=False)
    parser.add_argument('other', nargs='*')
    flag = parser.parse_args()
    main()
