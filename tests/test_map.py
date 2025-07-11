import pytest
from app import create_app, db

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

def test_get_map_entities_missing_params(client):
    # Aucun paramètre fourni
    response = client.get('/map/entities')
    assert response.status_code == 400
    assert 'center_lat' in response.json['error']
    # Un seul paramètre fourni
    response = client.get('/map/entities?center_lat=48.85')
    assert response.status_code == 400
    assert 'center_lat' in response.json['error'] 