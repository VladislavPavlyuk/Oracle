from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0004_rename_teammember_to_teammemberentity"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="TeamMemberEntity",
            new_name="TeamMember",
        ),
    ]
