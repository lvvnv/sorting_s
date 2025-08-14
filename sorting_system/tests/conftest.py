# tests/conftest.py
import pytest
import os
import django
from django.conf import settings
from django.test.utils import setup_test_environment

# Configure Django settings for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sorting_system.settings')
django.setup()
setup_test_environment()


@pytest.fixture
def api_client():
    """A Django test client instance."""
    from django.test import Client
    return Client()


@pytest.fixture
def authenticated_user(db):
    """Create and return an authenticated user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    return user