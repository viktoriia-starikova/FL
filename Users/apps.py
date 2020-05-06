from django.apps import AppConfig

## Сигнал создания профиля пользователя, когда создан юзер
class UsersConfig(AppConfig):
    name = 'Users'
    def ready(self):
        import Users.signals
