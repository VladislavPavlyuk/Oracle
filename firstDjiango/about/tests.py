from django.templatetags.static import static
from django.test import TestCase, override_settings

from about.models import AboutMember
from about.services import AboutMemberService


class AboutMemberServiceTests(TestCase):
    def test_get_members_uses_database_records_when_present(self):
        AboutMember.objects.create(
            name="DB Member",
            role="Engineer",
            bio="Bio from database.",
            photo="about/img/team/member-2.svg",
            sort_order=1,
        )

        members = AboutMemberService.get_members()

        self.assertEqual(len(members), 1)
        self.assertEqual(members[0]["name"], "DB Member")
        self.assertEqual(members[0]["photo_url"], static("about/img/team/member-2.svg"))
        self.assertEqual(
            members[0]["fallback_photo_url"],
            static("about/img/team/default-member.svg"),
        )

    @override_settings(
        ABOUT_DEFAULT_MEMBERS=[
            {
                "name": "Fallback One",
                "role": "PM",
                "bio": "Fallback bio.",
                "photo": "about/img/team/member-1.svg",
            }
        ]
    )
    def test_get_members_uses_fallback_when_database_is_empty(self):
        members = AboutMemberService.get_members()

        self.assertEqual(len(members), 1)
        self.assertEqual(members[0]["name"], "Fallback One")
        self.assertEqual(members[0]["photo_url"], static("about/img/team/member-1.svg"))

    @override_settings(
        ABOUT_DEFAULT_MEMBERS=[
            {
                "name": "External",
                "role": "QA",
                "bio": "External image.",
                "photo": "https://example.com/avatar.png",
            },
            {
                "name": "Local",
                "role": "Dev",
                "bio": "Local image.",
                "photo": "about/img/team/member-3.svg",
            },
        ]
    )
    def test_photo_url_normalization_for_external_and_local_paths(self):
        members = AboutMemberService.get_members()

        self.assertEqual(members[0]["photo_url"], "https://example.com/avatar.png")
        self.assertEqual(members[1]["photo_url"], static("about/img/team/member-3.svg"))

    @override_settings(
        ABOUT_DEFAULT_MEMBERS=[
            {
                "name": "Broken Link User",
                "role": "Designer",
                "bio": "Image can fail.",
                "photo": "https://example.com/missing.png",
            }
        ]
    )
    def test_fallback_image_behavior_is_present_in_template(self):
        response = self.client.get("/about/")
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn("onerror=\"this.onerror=null;this.src='", content)
        self.assertIn("default-member.svg", content)
