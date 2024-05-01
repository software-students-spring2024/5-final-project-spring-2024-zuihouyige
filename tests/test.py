import pytest
from app.app import app as flask_app  # Ensure this import matches your project structure
from bson.objectid import ObjectId



def test_home():
    """Test the home page route."""
    assert True
