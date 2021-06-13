from flask import request
from requests import get
from uuid import uuid4
from couchdb import Server, ResourceConflict, ResourceNotFound

couch = Server(url="http://couchdb-admin:couchdb-password@localhost:5984")
# print(couch, "\n \n \n \n \n")
# test = get(url="http://couchdb-admin:couchdb-password@host.docker.internal:5984/")
# print(test, "\n \n \n \n \n")
database = couch['customers']

def create_app(app):
    @app.route('/')
    def handle_default_route():
        return {'status': 'OK', 'description': 'REST API for performing CRUD operations against a Couch database'}

    @app.route('/api/customer', methods=['GET'])
    def handle_items_fetch():
        mango_query = {
            'selector': {'type': 'paid_customer'},
        }

        items = []

        for data in database.find(mango_query):
            items.append(data)

        return {"status": "OK", 'customers': items}

    @app.route('/api/customer', methods=['POST'])
    def handle_items_post():
        data = request.get_json()
        database.save(
            {'_id': 'customer:{}'.format(uuid4().hex), 'subscription': 'PREMIUM', 'type': 'paid_customer',
             'name': data['name'], 'occupation': data['occupation']})
        return {'status': 'OK', 'method': 'post'}

    @app.route('/api/customer', methods=['DELETE'])
    def handle_items_delete():
        data = request.get_json()
        doc = dict(_id=data['id'], _rev=data['rev'])

        try:
            database.delete(doc)
            return {'status': 'OK', 'message': 'Deleted record for: {}'.format(data['id'])}
        except ResourceConflict:
            return {'error': 'conflict found for document:{}'.format(data[id])}, 500
        except ResourceNotFound:
            return {'error': "document not found"}, 404

