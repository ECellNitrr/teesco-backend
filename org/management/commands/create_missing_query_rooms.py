from django.core.management.base import BaseCommand, CommandError
from org.models import Member
from query.models import QueryRoom
from org.custom_model_field import Permissions

class Command(BaseCommand):
    help = "Creates query room for a member-org \
        combination if it doesn't exist already"

    def handle(self, *args, **options):
        members = Member.objects.all()
        created = 0

        # Checking whether a queryroom object exists for all staff/volunteer.
        for member in members:
            if not member.group.perm_obj.permissions[Permissions.IS_ADMIN]:
                try:
                    QueryRoom.objects.get(
                        org = member.org,
                        for_user = member.user
                    )
                except:
                    # If queryroom does not exist, creating a queryroom.
                    QueryRoom.objects.create(
                        org = member.org,
                        for_user = member.user
                    )
                    created+=1
                    self.stdout.write(
                        "Successfully created QueryRoom object for", ending=' '
                    )
                    self.stdout.write(
                        f"{member.user.email} in {member.org} organization"
                    )
            else:
                pass

        # Keeping a count of queryrooms created helps in printing the final success message.
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Completed creating QueryRoom objects for {created} members.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                'Queryrooms for all required members already exist.'
                )
            )
