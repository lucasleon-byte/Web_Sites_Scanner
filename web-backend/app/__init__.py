from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    CORS(app) 

    
    client = MongoClient('mongodb+srv://leonvunic:Nogomet123@clusterdiplomski.rqewm.mongodb.net/?retryWrites=true&w=majority&ssl=true')
    app.db = client.get_database('scan')

    from .routes import main
    app.register_blueprint(main)

    return app
 



