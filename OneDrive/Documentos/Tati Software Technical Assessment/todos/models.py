"""
Todo model definition.
"""
from django.db import models


class Todo(models.Model):
    """
    Todo model with fields for title, description, completion status.

    Includes automatic timestamp tracking for created and updated times.
    """

    title = models.CharField(
        max_length=200,
        help_text="The title of the todo item"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the todo item"
    )
    is_completed = models.BooleanField(
        default=False,
        help_text="Whether the todo item is completed"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the todo was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the todo was last updated"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Todo'
        verbose_name_plural = 'Todos'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_completed']),
        ]

    def __str__(self):
        return self.title
