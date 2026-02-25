from django.db import models


class AboutMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=120)
    bio = models.TextField()
    photo = models.CharField(max_length=255, default="about/img/team/member-1.svg")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.name} ({self.role})"
