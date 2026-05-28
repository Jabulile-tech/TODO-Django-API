"""
Apps configuration for todos app.
"""
from django.apps import AppConfig


class TodosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todos'
    verbose_name = 'Todo Items'
