from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member
from query.models import QueryRoom
from org.custom_model_field import Permissions

@receiver(post_save, sender=Member)
def create_query_room(sender, instance, created, **kwargs):
    is_admin = instance.group.perm_obj.permissions[Permissions.IS_ADMIN]

    """
    Creating the QueryRoom only when a new member with 
    staff/volunteer level permissions is created.
    """
    if created and not is_admin:
        QueryRoom.objects.create(
            org= instance.org,
            for_user = instance.user
        )
    else:
        pass
