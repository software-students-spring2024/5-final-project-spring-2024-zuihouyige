import pytest
from unittest.mock import patch
from app.app import app as flask_app  # Adjust the import based on your project structure

@pytest.fixture
def client():
    # Patching MongoClient to prevent actual DB connection
    with patch('pymongo.MongoClient') as MockMongoClient:
        # Set up mock database and collections
        mock_db = MockMongoClient.return_value
        mock_db.__getitem__.return_value.recipes.find.return_value = [{"name": "Chocolate Cake"}]
        mock_db.__getitem__.return_value.recipes.find_one.return_value = {"name": "Chocolate Cake", "ingredients": "Chocolate, Eggs, Flour, Sugar", "steps": "Mix and bake"}
        
        # Flask provides a way to test your application by exposing the Werkzeug test Client
        # and handling the context locals for you.
        flask_app.config['TESTING'] = True
        with flask_app.test_client() as client:
            yield client

def test_home(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Chocolate Cake' in response.get_data(as_text=True)

def test_recipe_detail(client):
    """Test the recipe detail page."""
    response = client.get('/recipe/1')  # assuming '1' is the id used in the mocked find_one return
    assert response.status_code == 200
    assert 'Ingredients' in response.get_data(as_text=True)

def test_add_recipe(client):
    """Test the add recipe route."""
    with patch('app.app.db.recipes.insert_one') as mock_insert:
        response = client.post('/add', data={
            'name': 'Vanilla Cake',
            'ingredients': 'Vanilla, Eggs, Flour, Sugar',
            'steps': 'Mix and bake'
        }, follow_redirects=True)
        assert response.status_code == 200
        mock_insert.assert_called_once()

def test_edit_recipe(client):
    """Test the edit recipe route."""
    with patch('app.app.db.recipes.find_one') as mock_find_one, \
         patch('app.app.db.recipes.update_one') as mock_update_one:
        mock_find_one.return_value = {"_id": "1", "name": "Chocolate Cake", "ingredients": "Chocolate", "steps": "Mix and bake"}
        response = client.post('/edit/1', data={
            'name': 'Chocolate Cake Improved',
            'ingredients': 'Chocolate, More chocolate',
            'steps': 'Mix and bake slowly'
        }, follow_redirects=True)
        assert response.status_code == 200
        mock_update_one.assert_called_once()

def test_delete_recipe(client):
    """Test the delete recipe route."""
    with patch('app.app.db.recipes.delete_one') as mock_delete:
        response = client.post('/delete/1', follow_redirects=True)
        assert response.status_code == 200
        mock_delete.assert_called_once()

def test_search_recipes(client):
    """Test the search recipes route."""
    response = client.get('/search?query=cake')
    assert response.status_code == 200
    assert 'Chocolate Cake' in response.get_data(as_text=True)

def test_profile(client):
    """Test the profile page."""
    response = client.get('/profile')
    assert response.status_code == 200
