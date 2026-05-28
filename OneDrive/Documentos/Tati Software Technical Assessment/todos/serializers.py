"""
Serializers for Todo model validation and representation.
"""
from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """
    Serializer for Todo model.
    Handles validation and automatic timestamp handling.
    """

    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'description',
            'is_completed',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """
        Validate title is not empty and has reasonable length.
        """
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Title cannot be empty."
            )
        if len(value.strip()) > 200:
            raise serializers.ValidationError(
                "Title cannot exceed 200 characters."
            )
        return value.strip()

    def validate(self, data):
        """
        Additional validation at the object level.
        """
        if 'description' in data and data['description']:
            if len(str(data['description']).strip()) == 0:
                data['description'] = None
        return data
