from django.db import models

# Create your models here.
class Worker(models.Model):
    name = models.CharField(max_length = 50, blank = False, null = False)
    salary = models.IntegerField(default = 0)
    note = models.TextField(blank = True, null = True)

    def __str__(self):
        return f'({self.id}) Worker: {self.name}, {self.salary} $'
