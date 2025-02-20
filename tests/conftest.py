import pytest
from app import app, db
from models import User

@pytest.fixture(scope='module')
def test_client():
    """Set up test client and in-memory database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory test DB
    client = app.test_client()

    with app.app_context():
        db.create_all()

        # Create an admin user for authentication
        admin_user = User(username="admin", password="admin123")
        db.session.add(admin_user)
        db.session.commit()

    yield client  # Provide the test client

    with app.app_context():
        db.session.remove()
        db.drop_all()
