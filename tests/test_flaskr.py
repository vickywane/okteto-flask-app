import json
import os
from flask import Flask
import pytest
import logging
import requests
from ..routes.flaskr import create_app
from unittest.mock import Mock, patch

log = logging.getLogger(__name__)

app = Flask(__name__)
client = create_app(app)


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as fclient:
        yield fclient

#
# def test_handle_default_route(client):
#     request = client.get('/')
#     data = json.loads(request.data)
#     assert (data['status'] == "OK")


# @pytest.mark.server(url='/customers/_bulk_docs'.format(os.environ.get("COUCHDB_URL")), response={
#     "customers": [
#         {
#             "_id": "customer:5a7c1823c04f44de9f70f44af2902dc2",
#             "_rev": "1-04667a03c0aed3ab27c45513a2f83587",
#             "name": "John Doe",
#             "occupation": "Software Tester",
#             "subscription": "PREMIUM",
#             "type": "paid_customer"
#         }
#     ],
#     "status": "OK"
# })
# @pytest.mark.server(url='/v1/books', response=[{'id': 1}], method='GET')

def test_handler_responses(client):
    mock_patcher = patch("routes.flaskr.requests.post")
    mock = mock_patcher.start()

    mock.return_value.json.return_value = {}
    log.info('MOCK RESPONSE')
    log.info(mock)

    request = client.post('/api/customer', json={
        'name': 'John Mike',
        'occupation': 'Software Eng'
    })

    mock_patcher.stop()


    # responseData = json.loads(request.data)
    # log.info("RESPONSE HERE")
    # log.info(responseData)