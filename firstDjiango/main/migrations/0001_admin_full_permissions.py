from django.db import migrations


def create_admin_group_with_all_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

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


def remove_admin_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Admin").delete()
    Group.objects.filter(name="testGroup").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(
            create_admin_group_with_all_permissions,
            reverse_code=remove_admin_group,
        ),
    ]
