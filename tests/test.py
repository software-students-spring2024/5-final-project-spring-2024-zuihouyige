import pytest
from app import app as flask_app  # Ensure this import matches your project structure
from bson.objectid import ObjectId

@pytest.fixture(scope="module")
def client():
    # Set the app to testing mode
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(scope="module")
def test_recipe_id():
    return ObjectId()  # Generate a sample ObjectId for testing

def test_home(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200

def test_recipe_detail(client, test_recipe_id):
    """Test the recipe detail page."""
    response = client.get(f'/recipe/{test_recipe_id}')
    assert response.status_code == 200

def test_add_recipe(client):
    """Test adding a new recipe."""
    response = client.post('/add', data={
        'name': 'Test Recipe',
        'ingredients': 'Test Ingredients',
        'steps': 'Test Steps'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_edit_recipe(client, test_recipe_id):
    """Test editing an existing recipe."""
    response = client.post(f'/edit/{test_recipe_id}', data={
        'name': 'Updated Test Recipe',
        'ingredients': 'Updated Ingredients',
        'steps': 'Updated Steps'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_delete_recipe(client, test_recipe_id):
    """Test deleting a recipe."""
    response = client.post(f'/delete/{test_recipe_id}', follow_redirects=True)
    assert response.status_code == 200

def test_search_recipes(client):
    """Test the search functionality."""
    response = client.get('/search?query=test')
    assert response.status_code == 200

def test_profile(client):
    """Test the profile page."""
    response = client.get('/profile')
    assert response.status_code == 200
