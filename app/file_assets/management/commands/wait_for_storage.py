import time
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from file_assets.services.s3storage import S3StorageService


class Command(BaseCommand):
    help = "Wait until the storage backend is available."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3_service = S3StorageService()

    def add_arguments(self, parser):
        parser.add_argument(
            "--stable", "-s", type=int,
            default=5,
            help="how long to observe whether connection is stable (seconds), default: 5",
            )
        parser.add_argument(
            "--timeout", "-t", type=int,
            default=180,
            help="how long to wait for the storage before timing out (seconds), default: 180",
            )
        parser.add_argument(
            "--wait-when-alive", "-a", type=int,
            default=1,
            help="delay between checks when storage is up (seconds), default: 1",
            )
        parser.add_argument(
            "--wait-when-down", "-d", type=int,
            default=2,
            help="delay between checks when storage is down (seconds), default: 2",
            )

    def handle(self, *args, **options):
        stable = options['stable']
        timeout = options['timeout']
        wait_when_alive = options['wait_when_alive']
        wait_when_down = options['wait_when_down']

        start_time = timezone.now()
        start_time_alive = start_time
        start_time_down = start_time
        deadline = start_time + datetime.timedelta(seconds=timeout)
        deadline_elapsed = deadline
        last_exc = None
        previous_alive = False

        while True:
            try:
                self.s3_service.check_connection()
                alive = True
            except Exception as e:
                alive = False
                last_exc = e

            if alive:
                if not previous_alive:
                    start_time_alive = timezone.now()
                    deadline_elapsed = start_time_alive + datetime.timedelta(seconds=stable)
                elapsed = timezone.now() - start_time_alive
                if timezone.now() > deadline_elapsed:
                    break
                self.stdout.write(
                    f"Storage connection alive for > {elapsed.seconds} s"
                    )
                time.sleep(wait_when_alive)
            else:
                if previous_alive:
                    start_time_down = timezone.now()
                elapsed = timezone.now() - start_time_down
                self.stdout.write(
                    f"Waiting for storage (cause: {last_exc}) ... {elapsed.seconds} s"
                    )
                time.sleep(wait_when_down)

            if timezone.now() > deadline:
                raise CommandError("Could not establish storage connection.")

            previous_alive = alive
