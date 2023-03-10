from django.apps import AppConfig


class BaseTodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_todo'
