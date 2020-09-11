from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        env = [
            "DEBUG",
            "SECRET_KEY",
            "PGSQL_DATABASE",
            "PGSQL_USER",
            "PGSQL_PASSWORD",
            "PGSQL_HOST",
            "PGSQL_PORT"
        ]

        with open(".env", "w") as f:
            for e in env:
                f.write(f"{e}=\n")
