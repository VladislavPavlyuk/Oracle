from django.contrib import admin
from team.models import Resume
from team.models import TeamMember

admin.site.register(TeamMember)
admin.site.register(Resume)