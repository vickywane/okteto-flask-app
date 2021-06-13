import pytest
import logging
from flask_app.routes.flaskr import create_app

log = logging.getLogger(__name__)


@pytest.fixture
def client():
    app = create_app()

    app.config['TESTING'] = True

    with app.test_client() as fclient:
        yield fclient


def test_handle_default_route(client):
    request = client.get('/')
    assert (request['status'] == "OK")
