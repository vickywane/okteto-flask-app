import os
from requests import get, post

STAGING_API_ENDPOINT = os.environ.get("STAGING_COUCHDB_URL")


def test_handle_default_route():
    request = get(STAGING_API_ENDPOINT)
    response = request.json()
    assert (response['status'] == "OK")
    assert 'description' in response


def test_handle_items_post():
    request = post('{}/api/customer'.format(STAGING_API_ENDPOINT),
                   json={
                       'name': 'John Mike',
                       'occupation': 'Software Eng'
                   })

    responseData = request.json()
    assert responseData['status'] == "USER CREATED"


def test_handle_items_fetch():
    request = get('{}/api/customer'.format(STAGING_API_ENDPOINT))
    data = request.json()
    assert (data['status'] == 'OK')
    assert 'customers' in data
    assert '_id' in data['customers'][0]
