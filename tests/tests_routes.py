import pytest
from app import create_app, db
from models import User


@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            yield test_client
        db.drop_all()



def test_homepage(test_client):
    """Test if the root URL returns a welcome message."""
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the User Management API! \n Add /users to the URL to display all the users." in response.data
