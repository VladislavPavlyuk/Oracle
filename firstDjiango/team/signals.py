from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import Group
from team.models import TeamMember, Notification

def notify_hr(text: str):
    hr_group = Group.objects.get(name='HR')
    hr_users = hr_group.user_set.all()
#    for user in hr_users:
#        Notification.objects.create(
#            recipient=user,
#            text=text
#        )
    notifications = [Notification(recipient=user, text=text) for user in hr_users]
    Notification.objects.bulk_create(notifications)

@receiver(post_save, sender=TeamMember)
def notify_hr_on_teamMember_create(sender, instance, created, **kwargs):
    if not created:
        return

    notify_hr(f'Team Member {instance.name} created')

@receiver(post_delete, sender=TeamMember)
def notify_hr_on_teamMember_delete(sender, instance, using, **kwargs):
    notify_hr(f'Team Member {instance.name} deleted')