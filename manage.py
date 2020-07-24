#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def check_settings():
    for arg in sys.argv:
        _s = arg.split('=')
        if _s[0] == "--settings":
            return False
    return True


if __name__ == '__main__':
    if check_settings():
        if len(sys.argv) > 1 and sys.argv[1] in ["--prod", "prod", "--production", "production"]:
            del sys.argv[1]
            sys.argv.append("--settings=core.settings.prod")
        else:
            sys.argv.append("--settings=core.settings.dev")
    main()
