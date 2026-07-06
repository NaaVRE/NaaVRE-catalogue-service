from django.contrib.auth.models import Permission, User
from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Create a user with read and write permissions on BinderEnvironment"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument(
            "-p", "--permission",
            action="append",
            dest="permissions",
            default=[],
            help="Permission in the form app_label.model.codename",
            )
        parser.add_argument(
            "-t", "--token",
            nargs='?',
            const=True,
            default=False,
            help="Create an API token (leave empty to generate one)",
            )

    def handle(self, *args, **options):
        username = options["username"]
        permission_specs = options["permissions"]
        token_key = options["token"]

        if User.objects.filter(username=username).exists():
            raise CommandError(f"User already exists: {username}")

        user = User.objects.create_user(username=username)
        self.stdout.write(
            self.style.SUCCESS(f"Created user: {username}")
            )

        permissions = []
        for spec in permission_specs:
            try:
                app_label, model, codename = spec.split(".")
            except ValueError:
                raise CommandError(
                    f"Invalid permission format: '{spec}'. "
                    "Use app_label.model.codename"
                    )
            try:
                perm = Permission.objects.get_by_natural_key(
                    codename, app_label, model.lower()
                    )
            except Permission.DoesNotExist:
                raise CommandError(f"Permission does not exist: '{spec}'")
            permissions.append(perm)

        if permissions:
            user.user_permissions.add(*permissions)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Permissions: {"".join([f"\n  {p}" for p in permissions])}"
                    )
                )

        # token_key is str or bool
        # when truthy, it is True or a non-empty str
        if token_key:
            if token_key is True:
                token_obj = Token.objects.create(user=user)
                self.stdout.write(
                    self.style.SUCCESS(f"Created token: {token_obj.key}")
                    )
            else:
                # token_key is str
                if token_key and Token.objects.filter(key=token_key).exists():
                    raise CommandError(
                        "Token is already in use by another user. "
                        "Provide another value or delete the existing token."
                        )
                Token.objects.create(user=user, key=token_key)
                self.stdout.write(
                    self.style.SUCCESS(
                        "Created token: (using the provided value)"
                        )
                    )
