from flask import Flask
from .routes.flaskr import create_app

app = Flask(__name__)
create_app(app)

if __name__ == "__main__":
    app.run()

# test = get(url="http://couchdb-admin:couchdb-password@database:5984/")
# print(test, "\n \n \n \n \n")