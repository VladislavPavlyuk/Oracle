from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class TeamMember(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    salary = models.IntegerField(default=0)
    note = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to="team_member_photos/")

    class Meta:
        db_table = "team_member"

    def __str__(self):
        return f"({self.id}) Team member: {self.name}, {self.salary} $"


class Resume(models.Model):
    team_member = models.OneToOneField(
        TeamMember,
        on_delete=models.CASCADE,
        related_name="resume",
    )
    date_created = models.DateField(auto_now_add=True)
    description =models.TextField(blank=True, null=True)
    position = models.CharField(max_length=120)
    summary = models.TextField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "team_resume"

    def __str__(self):
        return f"Resume for {self.team_member.name}"


class Contact(models.Model):
    digits_only_validator = RegexValidator(
        regex=r"^\d+$",
        message="Use numbers only.",
    )

    team_member = models.ForeignKey(
        TeamMember,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    address = models.CharField(max_length=255, blank=True)
    home_phone = models.CharField(max_length=30, blank=True, validators=[digits_only_validator])
    mobile_phone = models.CharField(max_length=30, blank=True, validators=[digits_only_validator])
    email = models.EmailField(blank=True)

    class Meta:
        db_table = "team_contact"

    def __str__(self):
        return f"Contacts for {self.team_member.name}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    text = models.TextField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.text}"