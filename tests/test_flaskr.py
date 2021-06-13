import json

from flask import Flask
import pytest
import logging
from ..routes.flaskr import create_app

log = logging.getLogger(__name__)

app = Flask(__name__)
client = create_app(app)


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as fclient:
        yield fclient


def test_handle_default_route(client):
    request = client.get('/')
    data = json.loads(request.data)
    assert (data['status'] == "OK")
