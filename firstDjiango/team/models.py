from django.db import models

# Create your models here.
class teamMember(models.Model):
    name = models.CharField(max_length = 50, blank = False, null = False)
    salary = models.IntegerField(default = 0)
    note = models.TextField(blank = True, null = True)

    class Meta:
        db_table = "team_member"

    def __str__(self):
        return f'({self.id}) Team member: {self.name}, {self.salary} $'
