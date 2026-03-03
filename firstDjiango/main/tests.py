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


class TestGroupPermissionsTests(TestCase):
    def test_test_group_has_project_crud_permissions_without_user_group_management(self):
        test_group = Group.objects.get(name="testGroup")
        permission_codes = set(test_group.permissions.values_list("codename", flat=True))

        expected = {
            "add_teammember",
            "change_teammember",
            "delete_teammember",
            "add_resume",
            "change_resume",
            "delete_resume",
            "add_contact",
            "change_contact",
            "delete_contact",
            "add_post",
            "change_post",
            "delete_post",
        }
        self.assertTrue(expected.issubset(permission_codes))
        self.assertNotIn("add_user", permission_codes)
        self.assertNotIn("change_user", permission_codes)
        self.assertNotIn("delete_user", permission_codes)
        self.assertNotIn("add_group", permission_codes)
        self.assertNotIn("change_group", permission_codes)
        self.assertNotIn("delete_group", permission_codes)


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

    def test_registered_user_added_to_test_group(self):
        manager = User.objects.create_user(username="manager", password="pass12345")
        manager.user_permissions.add(Permission.objects.get(codename="add_user"))
        self.client.login(username="manager", password="pass12345")

        response = self.client.post(
            reverse("register"),
            data={
                "username": "newuser",
                "password1": "StrongPass12345",
                "password2": "StrongPass12345",
            },
        )

        self.assertEqual(response.status_code, 302)
        created_user = User.objects.get(username="newuser")
        self.assertTrue(created_user.groups.filter(name="testGroup").exists())
