import random

from django.db import transaction

from team.models import Contact, Resume, TeamMember


class TeamDataFabric:
    first_names = [
        "Liam",
        "Emma",
        "Noah",
        "Olivia",
        "Elijah",
        "Ava",
        "James",
        "Sophia",
        "Benjamin",
        "Mia",
        "Lucas",
        "Charlotte",
        "Henry",
        "Amelia",
        "Alexander",
        "Harper",
        "Daniel",
        "Evelyn",
        "Michael",
        "Abigail",
    ]

    last_names = [
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Martinez",
        "Lopez",
        "Wilson",
        "Anderson",
        "Thomas",
        "Taylor",
        "Moore",
        "Jackson",
        "Martin",
        "Lee",
        "Perez",
        "Thompson",
        "White",
    ]

    positions = [
        "Backend Engineer",
        "Frontend Engineer",
        "QA Engineer",
        "Project Manager",
        "Business Analyst",
        "DevOps Engineer",
        "UI/UX Designer",
        "Data Analyst",
        "Team Lead",
        "Product Manager",
    ]

    skills = [
        "Python, Django, PostgreSQL",
        "JavaScript, React, REST API",
        "Docker, CI/CD, Linux",
        "Testing, Selenium, Pytest",
        "Figma, UX Research, Prototyping",
        "SQL, Analytics, Reporting",
    ]

    streets = [
        "Main St",
        "Oak Ave",
        "Maple Rd",
        "Cedar Blvd",
        "Sunset Dr",
        "Lakeview Ln",
        "Pine St",
    ]

    cities = [
        "New York",
        "Austin",
        "Seattle",
        "Chicago",
        "San Diego",
        "Denver",
        "Boston",
    ]

    @classmethod
    def generate_team_data(cls, amount=20):
        with transaction.atomic():
            for _ in range(amount):
                first_name = random.choice(cls.first_names)
                last_name = random.choice(cls.last_names)
                full_name = f"{first_name} {last_name}"
                salary = random.randint(2500, 12000)

                member = TeamMember.objects.create(
                    name=full_name,
                    salary=salary,
                    note=f"{random.choice(cls.positions)} in {random.choice(cls.cities)} office.",
                )

                Resume.objects.create(
                    team_member=member,
                    description=f"{full_name} is a valuable team member focused on high-quality delivery.",
                    position=random.choice(cls.positions),
                    summary=f"{full_name} has strong communication skills and consistently meets deadlines.",
                    experience_years=random.randint(1, 12),
                    education="Bachelor degree in Computer Science",
                    skills=random.choice(cls.skills),
                )

                Contact.objects.create(
                    team_member=member,
                    address=f"{random.randint(100, 9999)} {random.choice(cls.streets)}, {random.choice(cls.cities)}",
                    home_phone=f"{random.randint(1000000000, 9999999999)}",
                    mobile_phone=f"{random.randint(1000000000, 9999999999)}",
                    email=f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}@example.com",
                )
