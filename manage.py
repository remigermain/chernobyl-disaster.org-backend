#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# fix for pydot
os.environ["PATH"] += os.pathsep + ""


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


def defined_settings():
    for arg in sys.argv:
        _s = arg.split('=')
        if _s[0] == "--settings":
            return True
    return False


if __name__ == '__main__':
    if not defined_settings():
        settings = ['--settings=core.settings.dev']
        if len(sys.argv) > 1 and sys.argv[1] in ["--prod", "prod", "--production", "production"]:
            del sys.argv[1]
            print("---- PROD MODE ----")
            settings = ['--settings=core.settings.prod']
        else:
            print("---- DEV MODE ----")
        if len(sys.argv) == 1:
            settings = ['help'] + settings
        sys.argv.extend(settings)
    main()
