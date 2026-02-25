from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0003_rename_team_teammember"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="teamMember",
            new_name="TeamMemberEntity",
        ),
    ]
