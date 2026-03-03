from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        post_migrate.connect(sync_admin_group_permissions, dispatch_uid="main.sync_admin_group_permissions")


def sync_admin_group_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    admin_group, _ = Group.objects.get_or_create(name="Admin")
    admin_group.permissions.set(Permission.objects.all())
    test_group, _ = Group.objects.get_or_create(name="testGroup")
    test_group.permissions.set(
        Permission.objects.filter(
            codename__in=[
                "add_teammember",
                "change_teammember",
                "delete_teammember",
                "add_resume",
                "change_resume",
                "delete_resume",
                "add_contact",
                "change_contact",
                "delete_contact",
                "add_post",
                "change_post",
                "delete_post",
            ]
        )
    )
