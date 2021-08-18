import os
import requests
from flask import request
from uuid import uuid4

COUCH_CUSTOMER_DB = '{}/customers'.format(os.environ.get('COUCHDB_URL'))


def create_app(app):
    @app.route('/')
    def handle_default_route():
        requests.put(COUCH_CUSTOMER_DB)
        return {'status': 'OK', 'description': 'REST API for performing CRUD operations against a Couch database'}

    @app.route('/api/customer', methods=['GET'])
    def handle_items_fetch():
        fetch_customers = requests.post(
            url='{}/_find'.format(COUCH_CUSTOMER_DB),
            json={
                "selector": {"type": "paid_customer"}
            },
            headers={
                'Content-Type': 'application/json'
            }
        )

        customers = fetch_customers.json()

        if fetch_customers.status_code == 200:
            return {"status": "OK", 'customers': customers['docs']}
        else:
            return {'status': "ERROR CREATING USER"}, fetch_customers.status_code

    @app.route('/api/customer', methods=['POST'])
    def handle_items_post():
        data = request.get_json()

        doc = {
            "docs": [
                {
                    '_id': 'customer:{}'.format(uuid4().hex), 'subscription': 'PREMIUM', 'type': 'paid_customer',
                    'name': data['name'], 'occupation': data['occupation']
                }
            ]
        }

        insert_doc = requests.post(
            url='{}/_bulk_docs'.format(COUCH_CUSTOMER_DB),
            json=doc,
            headers={
                'Content-Type': 'application/json'
            }
        )
        print(insert_doc.status_code, insert_doc, '{}/_bulk_docs'.format(COUCH_CUSTOMER_DB))
        if insert_doc.status_code == 201:
            return {'status': 'USER CREATED'}
        else:
            return {'status': "ERROR CREATING USER"}, insert_doc.status_code

    @app.route('/api/customer', methods=['DELETE'])
    def handle_items_delete():
        data = request.get_json()

        delete_doc = requests.head(url="{0}/{1}".format(COUCH_CUSTOMER_DB, data['id']))

        if delete_doc.status_code == 200:
            return {"status": "DOCUMENT DELETED"}
        else:
            return {"status": "ERROR DELETING DOCUMENT"}, delete_doc.status_code
