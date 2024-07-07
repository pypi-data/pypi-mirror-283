import datetime
from flask import Flask
from flask_cors import CORS
#from flask_jwt_simple import JWTManager
from flask_jwt_extended import JWTManager
from config import jwt_key_secret
from config import path_to_upload
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = jwt_key_secret
app.config['JWT_EXPIRES'] = datetime.timedelta(minutes= 5) 
app.config['UPLOAD_FOLDER'] = path_to_upload
app.config['BASE_DIR'] = basedir
JWTManager(app)


class ShopifyInitClass:

    @staticmethod
    def getCurrentApp():
        return app

        #for enable cors
        #cors = CORS(app)

#import ShopifyTupperware.views
import ShopifyTupperware.controllers
