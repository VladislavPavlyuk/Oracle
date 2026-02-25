from pathlib import Path

from django.conf import settings
from django.templatetags.static import static

from about.models import AboutMember


class AboutMemberService:
    FALLBACK_PHOTO_PATH = "about/img/team/default-member.svg"
    TEAM_IMAGES_DIR = Path(settings.BASE_DIR) / "about" / "static" / "about" / "img" / "team"

    @classmethod
    def _photo_from_name(cls, name: str) -> str:
        filename = f"{name}.jfif"
        candidate = cls.TEAM_IMAGES_DIR / filename
        if candidate.exists():
            return static(f"about/img/team/{filename}")
        return ""

    @classmethod
    def _build_photo_url(cls, photo: str) -> str:
        if photo and (photo.startswith("http://") or photo.startswith("https://")):
            return photo
        if photo:
            return static(photo)
        return static(cls.FALLBACK_PHOTO_PATH)

    @classmethod
    def _map_member(cls, member: dict) -> dict:
        photo_url_by_name = cls._photo_from_name(member["name"])
        if photo_url_by_name:
            photo_url = photo_url_by_name
        else:
            photo_url = cls._build_photo_url(member.get("photo", ""))

        return {
            "name": member["name"],
            "role": member["role"],
            "bio": member["bio"],
            "photo_url": photo_url,
            "fallback_photo_url": static(cls.FALLBACK_PHOTO_PATH),
        }

    @classmethod
    def get_members(cls) -> list[dict]:
        members_qs = list(AboutMember.objects.all())
        if members_qs:
            members = [
                {
                    "name": member.name,
                    "role": member.role,
                    "bio": member.bio,
                    "photo": member.photo,
                }
                for member in members_qs
            ]
        else:
            members = list(getattr(settings, "ABOUT_DEFAULT_MEMBERS", []))

        return [cls._map_member(member) for member in members]
