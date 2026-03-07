from django.apps import AppConfig

class TeamConfig(AppConfig):
    name = 'team'

    def ready(self):
        import team.signals