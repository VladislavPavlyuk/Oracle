from django.db import migrations


def create_admin_group_with_all_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    admin_group, _ = Group.objects.get_or_create(name="Admin")
    admin_group.permissions.set(Permission.objects.all())


def remove_admin_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Admin").delete()


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
