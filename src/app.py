import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db
from routes import api

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
CORS(app)

@app.route('/')
def main():
    return jsonify({ "status": "App Running Successfully!"}), 200

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run()