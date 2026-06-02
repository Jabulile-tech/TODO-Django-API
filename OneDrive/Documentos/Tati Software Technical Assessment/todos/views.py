"""
API views for Todo CRUD operations.
"""
import logging
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer

# Get logger for this module
logger = logging.getLogger(__name__)


class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Todo CRUD operations.

    Provides:
    - List all todos: GET /api/todos/
    - Create todo: POST /api/todos/
    - Retrieve todo: GET /api/todos/{id}/
    - Update todo: PUT /api/todos/{id}/
    - Partial update: PATCH /api/todos/{id}/
    - Delete todo: DELETE /api/todos/{id}/
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new Todo item with logging.
        """
        logger.info(f"Creating new todo with data: {request.data}")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            todo_id = serializer.data['id']
            logger.info(f"Successfully created todo with ID: {todo_id}")
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            logger.warning(
                f"Failed to create todo due to validation errors: "
                f"{serializer.errors}"
            )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        """
        Save the todo instance.
        """
        serializer.save()

    def list(self, request, *args, **kwargs):
        """
        List all Todo items with logging.
        """
        logger.debug("Fetching list of all todos")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single Todo item with logging.
        """
        todo_id = kwargs.get('pk')
        logger.debug(f"Retrieving todo with ID: {todo_id}")
        try:
            return super().retrieve(request, *args, **kwargs)
        except Todo.DoesNotExist:
            logger.warning(f"Todo with ID {todo_id} not found")
            return Response(
                {"detail": "Todo not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        """
        Update a Todo item with logging.
        """
        todo_id = kwargs.get('pk')
        logger.info(
            f"Updating todo ID {todo_id} with data: {request.data}"
        )

        try:
            response = super().update(request, *args, **kwargs)
            logger.info(f"Successfully updated todo ID {todo_id}")
            return response
        except Todo.DoesNotExist:
            logger.warning(
                f"Todo with ID {todo_id} not found for update"
            )
            return Response(
                {"detail": "Todo not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a Todo item with logging.
        """
        todo_id = kwargs.get('pk')
        logger.info(
            f"Partially updating todo ID {todo_id} "
            f"with data: {request.data}"
        )

        try:
            response = super().partial_update(request, *args, **kwargs)
            logger.info(
                f"Successfully partially updated todo ID {todo_id}"
            )
            return response
        except Todo.DoesNotExist:
            logger.warning(
                f"Todo with ID {todo_id} not found for partial update"
            )
            return Response(
                {"detail": "Todo not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a Todo item with logging.
        """
        todo_id = kwargs.get('pk')
        logger.info(f"Deleting todo with ID: {todo_id}")

        try:
            instance = get_object_or_404(Todo, pk=todo_id)
            instance.delete()
            logger.info(f"Successfully deleted todo ID {todo_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            logger.warning(f"Todo with ID {todo_id} not found for delete")
            return Response(
                {"detail": "Todo not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Get all completed todos.
        GET /api/todos/completed/
        """
        logger.debug("Fetching all completed todos")
        completed_todos = Todo.objects.filter(is_completed=True)
        serializer = self.get_serializer(completed_todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Get all pending (incomplete) todos.
        GET /api/todos/pending/
        """
        logger.debug("Fetching all pending todos")
        pending_todos = Todo.objects.filter(is_completed=False)
        serializer = self.get_serializer(pending_todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
