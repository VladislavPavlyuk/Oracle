from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from team.models import Notification


class NotificationAdminTests(TestCase):
    def test_notification_marked_as_read_when_opened_in_admin_change_view(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="StrongPass12345",
        )
        recipient = User.objects.create_user(
            username="employee",
            password="StrongPass12345",
        )
        notification = Notification.objects.create(
            recipient=recipient,
            text="Test notification",
            is_read=False,
        )

        self.client.force_login(admin_user)
        response = self.client.get(reverse("admin:team_notification_change", args=[notification.pk]))

        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
