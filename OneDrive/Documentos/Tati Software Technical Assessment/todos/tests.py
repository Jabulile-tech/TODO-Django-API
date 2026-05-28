"""
Comprehensive unit tests for Todo API endpoints.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Todo


class TodoModelTest(TestCase):
    """Test cases for Todo model."""

    def setUp(self):
        """Set up test todo instances."""
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            is_completed=False
        )

    def test_todo_creation(self):
        """Test that a todo can be created successfully."""
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertFalse(self.todo.is_completed)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)

    def test_todo_string_representation(self):
        """Test todo string representation."""
        self.assertEqual(str(self.todo), "Test Todo")

    def test_todo_default_completion_status(self):
        """Test that default completion status is False."""
        new_todo = Todo.objects.create(title="Another Todo")
        self.assertFalse(new_todo.is_completed)

    def test_todo_optional_description(self):
        """Test that description is optional."""
        todo_without_desc = Todo.objects.create(
            title="No Description Todo"
        )
        self.assertIsNone(todo_without_desc.description)


class TodoAPITest(TestCase):
    """Test cases for Todo API endpoints."""

    def setUp(self):
        """Set up test client and sample todos."""
        self.client = APIClient()
        self.list_url = reverse('todo-list')

        # Create sample todos
        self.todo1 = Todo.objects.create(
            title="Buy Groceries",
            description="Milk, eggs, bread",
            is_completed=False
        )
        self.todo2 = Todo.objects.create(
            title="Finish Project",
            description="Complete Django REST API",
            is_completed=True
        )

    def test_create_todo_valid(self):
        """Test creating a todo with valid data."""
        data = {
            "title": "New Task",
            "description": "This is a new task",
            "is_completed": False
        }
        response = self.client.post(
            self.list_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(response.data['title'], "New Task")
        self.assertEqual(
            response.data['description'],
            "This is a new task"
        )
        self.assertFalse(response.data['is_completed'])

    def test_create_todo_missing_title(self):
        """Test creating a todo without title should fail."""
        data = {
            "description": "Task without title",
        }
        response = self.client.post(
            self.list_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn('title', response.data)

    def test_create_todo_empty_title(self):
        """Test creating a todo with empty title should fail."""
        data = {
            "title": "",
            "description": "Task with empty title",
        }
        response = self.client.post(
            self.list_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn('title', response.data)

    def test_list_all_todos(self):
        """Test listing all todos."""
        response = self.client.get(self.list_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_todo(self):
        """Test retrieving a single todo."""
        url = reverse('todo-detail', kwargs={'pk': self.todo1.id})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response.data['title'], "Buy Groceries")
        self.assertEqual(response.data['id'], self.todo1.id)

    def test_retrieve_nonexistent_todo(self):
        """Test retrieving a non-existent todo returns 404."""
        url = reverse('todo-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_update_todo_full(self):
        """Test fully updating a todo with PUT."""
        url = reverse('todo-detail', kwargs={'pk': self.todo1.id})
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "is_completed": True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response.data['title'], "Updated Task")
        self.assertEqual(
            response.data['description'],
            "Updated description"
        )
        self.assertTrue(response.data['is_completed'])

    def test_update_todo_partial(self):
        """Test partially updating a todo with PATCH."""
        url = reverse('todo-detail', kwargs={'pk': self.todo1.id})
        data = {
            "is_completed": True
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Unchanged field
        self.assertEqual(response.data['title'], "Buy Groceries")
        # Changed field
        self.assertTrue(response.data['is_completed'])

    def test_update_nonexistent_todo(self):
        """Test updating a non-existent todo returns 404."""
        url = reverse('todo-detail', kwargs={'pk': 99999})
        data = {
            "title": "Updated Task",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_delete_todo(self):
        """Test deleting a todo."""
        url = reverse('todo-detail', kwargs={'pk': self.todo1.id})
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        # Verify it's deleted
        self.assertFalse(
            Todo.objects.filter(id=self.todo1.id).exists()
        )

    def test_delete_nonexistent_todo(self):
        """Test deleting a non-existent todo returns 404."""
        url = reverse('todo-detail', kwargs={'pk': 99999})
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_completed_todos_endpoint(self):
        """Test retrieving only completed todos."""
        url = reverse('todo-completed')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.todo2.id)

    def test_pending_todos_endpoint(self):
        """Test retrieving only pending todos."""
        url = reverse('todo-pending')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.todo1.id)

    def test_todo_timestamps(self):
        """Test that created_at and updated_at are set correctly."""
        url = reverse('todo-detail', kwargs={'pk': self.todo1.id})
        response = self.client.get(url)
        self.assertIsNotNone(response.data['created_at'])
        self.assertIsNotNone(response.data['updated_at'])

    def test_create_todo_title_whitespace_stripped(self):
        """Test that title whitespace is stripped."""
        data = {
            "title": "  Task with spaces  ",
        }
        response = self.client.post(
            self.list_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(response.data['title'], "Task with spaces")


class TodoSerializerTest(TestCase):
    """Test cases for TodoSerializer validation."""

    def test_serializer_with_valid_data(self):
        """Test serializer with valid data."""
        from .serializers import TodoSerializer

        data = {
            "title": "Valid Task",
            "description": "Valid Description",
            "is_completed": False
        }
        serializer = TodoSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_empty_description(self):
        """Test serializer handles empty description gracefully."""
        from .serializers import TodoSerializer

        data = {
            "title": "Task",
            "description": "",
        }
        serializer = TodoSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_title_validation(self):
        """Test serializer title validation."""
        from .serializers import TodoSerializer

        # Test empty title
        data = {"title": ""}
        serializer = TodoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
