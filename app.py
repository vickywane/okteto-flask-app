from flask import Flask, request
from flask_app.routes.flaskr import create_app

app = Flask(__name__)
create_app(app)

if __name__ == "__main__":
    app.run()
