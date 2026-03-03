from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse


class AdminPermissionsTests(TestCase):
    def test_admin_group_exists_and_can_manage_users(self):
        admin_group = Group.objects.get(name="Admin")
        permission_codes = set(
            admin_group.permissions.filter(content_type__app_label="auth").values_list("codename", flat=True)
        )
        self.assertIn("add_user", permission_codes)
        self.assertIn("change_user", permission_codes)
        self.assertIn("delete_user", permission_codes)


class RegisterPermissionsTests(TestCase):
    def test_register_requires_add_user_permission(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 302)

    def test_user_with_add_user_permission_can_access_register(self):
        user = User.objects.create_user(username="manager", password="pass12345")
        permission = Permission.objects.get(codename="add_user")
        user.user_permissions.add(permission)
        self.client.login(username="manager", password="pass12345")

        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
