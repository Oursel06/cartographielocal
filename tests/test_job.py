import pytest
from app import create_app, db
import uuid

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_jobs_empty(client):
    response = client.get('/jobs')
    assert response.status_code == 200
    assert response.json == []

def test_get_job_by_id_not_found(client):
    random_id = uuid.uuid4()
    response = client.get(f'/jobs/{random_id}')
    assert response.status_code == 404 