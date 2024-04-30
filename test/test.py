
import pytest
from app import app as flask_app, db
from bson.objectid import ObjectId
from pymongo import MongoClient
import io

@pytest.fixture
def app():
    # Setup for test app
    flask_app.config.update({
        "TESTING": True,
        "MONGO_URI": "mongodb://localhost:27017/test_database"
    })
    client = MongoClient(flask_app.config["MONGO_URI"])
    db = client.get_default_database()

    # Clear test database before each test
    db.recipes.delete_many({})

    yield flask_app

    # Teardown after tests
    db.recipes.delete_many({})
    client.close()

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.content_type

def test_recipe_detail(client, app):
    with app.app_context():
        # Insert a dummy recipe into the database
        recipe_id = db.recipes.insert_one({
            "name": "Test Recipe",
            "ingredients": "Test Ingredients",
            "steps": "Test Steps"
        }).inserted_id

    response = client.get(f'/recipe/{recipe_id}')
    assert response.status_code == 200
    assert 'Test Recipe' in response.get_data(as_text=True)

def test_add_recipe(client, app):
    response = client.post('/add', data={
        'name': 'New Test Recipe',
        'ingredients': 'Some Ingredients',
        'steps': 'Some Cooking Steps'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        assert db.recipes.find_one({"name": "New Test Recipe"})

def test_edit_recipe(client, app):
    with app.app_context():
        # Insert a dummy recipe into the database
        recipe_id = db.recipes.insert_one({
            "name": "Old Recipe",
            "ingredients": "Old Ingredients",
            "steps": "Old Steps"
        }).inserted_id

    response = client.post(f'/edit/{recipe_id}', data={
        'name': 'Updated Recipe',
        'ingredients': 'Updated Ingredients',
        'steps': 'Updated Steps'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        updated_recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})
        assert updated_recipe['name'] == 'Updated Recipe'

def test_delete_recipe(client, app):
    with app.app_context():
        # Insert a dummy recipe to delete later
        recipe_id = db.recipes.insert_one({
            "name": "Delete Me",
            "ingredients": "Some Ingredients",
            "steps": "Some Steps"
        }).inserted_id

    response = client.post(f'/delete/{recipe_id}', follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert db.recipes.find_one({"_id": ObjectId(recipe_id)}) is None

def test_search_recipes(client, app):
    with app.app_context():
        # Insert multiple recipes
        db.recipes.insert_many([
            {"name": "Soup", "ingredients": "Water", "steps": "Boil water"},
            {"name": "Salad", "ingredients": "Greens", "steps": "Mix greens"}
        ])

    response = client.get('/search?query=soup')
    assert response.status_code == 200
    assert 'Soup' in response.get_data(as_text=True)
    assert 'Salad' not in response.get_data(as_text=True)
