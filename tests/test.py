import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.app import app as flask_app  # Import your Flask app

@pytest.fixture
def client():
    with patch('pymongo.MongoClient') as MockMongoClient:
        mock_db = MockMongoClient.return_value.__getitem__.return_value
        with flask_app.test_client() as client:
            yield client, mock_db

def test_home_page(client):
    client, mock_db = client
    mock_db.recipes.find.return_value = [
        {"name": "Chocolate Cake", "ingredients": "Chocolate", "steps": "Bake"}
    ]
    response = client.get('/')
    assert response.status_code == 200
    assert 'Chocolate Cake' in response.get_data(as_text=True)

def test_recipe_detail(client):
    client, mock_db = client
    mock_db.recipes.find_one.return_value = {
        "_id": "1",
        "name": "Chocolate Cake",
        "ingredients": "Chocolate",
        "steps": "Bake"
    }
    response = client.get('/recipe/1')
    assert response.status_code == 200
    assert 'Chocolate Cake' in response.get_data(as_text=True)

def test_add_recipe(client):
    client, mock_db = client
    response = client.post('/add', data={
        'name': 'Lemon Cake',
        'ingredients': 'Lemon',
        'steps': 'Bake'
    }, follow_redirects=True)
    assert response.status_code == 200
    mock_db.recipes.insert_one.assert_called_once()

def test_edit_recipe(client):
    client, mock_db = client
    mock_db.recipes.find_one.return_value = {
        "_id": "1",
        "name": "Chocolate Cake",
        "ingredients": "Chocolate",
        "steps": "Bake"
    }
    response = client.post('/edit/1', data={
        'name': 'Vanilla Cake',
        'ingredients': 'Vanilla',
        'steps': 'Bake'
    }, follow_redirects=True)
    assert response.status_code == 200
    mock_db.recipes.update_one.assert_called_once()

def test_delete_recipe(client):
    client, mock_db = client
    response = client.post('/delete/1', follow_redirects=True)
    assert response.status_code == 200
    mock_db.recipes.delete_one.assert_called_once()

def test_search_recipes(client):
    client, mock_db = client
    mock_db.recipes.find.return_value = [
        {"name": "Chocolate Cake", "ingredients": "Chocolate", "steps": "Bake"}
    ]
    response = client.get('/search?query=chocolate')
    assert response.status_code == 200
    assert 'Chocolate Cake' in response.get_data(as_text=True)

def test_profile(client):
    client, _ = client
    response = client.get('/profile')
    assert response.status_code == 200
