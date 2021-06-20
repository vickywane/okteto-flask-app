import json
import os
from flask import Flask
import pytest
import logging
import httpretty
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


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_handle_items_fetch(client):
    mockResponse = '{"docs":[{"_id":"customer:123456789","_rev":"1-123456789","subscription":"PREMIUM",' \
                   '"type":"paid_customer","name":"John Mike","occupation":"Software Eng"}],' \
                   '"bookmark":"g1123123424211233221"} '
    httpretty.register_uri(
        httpretty.POST,
        '{}/customers/_find'.format(os.environ.get("COUCHDB_URL")),
        body=mockResponse
    )

    request = client.get('/api/customer')
    data = json.loads(request.data)
    assert (data['status'] == 'OK')
    assert 'customers' in data
    assert '_id' in data['customers'][0]


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_handle_items_post(client):
    httpretty.register_uri(
        httpretty.POST,
        '{}/customers/_bulk_docs'.format(os.environ.get("COUCHDB_URL")),
        status=201
    )

    request = client.post('/api/customer', json={
        'name': 'John Mike',
        'occupation': 'Software Eng'
    })

    responseData = json.loads(request.data)
    assert responseData['status'] == "USER CREATED"


@httpretty.activate(verbose=True, allow_net_connect=False)
def test_handle_items_delete(client):
    mockCustomerID = 'customer:123456789'

    httpretty.register_uri(
        httpretty.HEAD,
        '{0}/customers/{1}'.format(os.environ.get("COUCHDB_URL"), mockCustomerID),
    )

    request = client.delete('/api/customer', json={
        'id': mockCustomerID,
    })

    responseData = json.loads(request.data)
    assert request.status_code == 200
    assert responseData['status'] == "DOCUMENT DELETED"
