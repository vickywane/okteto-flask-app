import json
from requests import post


def test_handle_items_post():
    data = post('http://127.0.0.1:5050/api/customer',
                json={
                    'name': 'John Mike',
                    'occupation': 'Software Eng'
                }
                )

    print(data)


test_handle_items_post()
