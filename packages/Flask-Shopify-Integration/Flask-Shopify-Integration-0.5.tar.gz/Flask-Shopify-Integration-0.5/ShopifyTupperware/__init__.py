import datetime
from flask import Flask
from flask_cors import CORS
#from flask_jwt_simple import JWTManager
from flask_jwt_extended import JWTManager
from config import jwt_key_secret
from config import path_to_upload
import os
#import logging
#add to protect from ip address
from flask import abort, request

basedir = os.path.abspath(os.path.dirname(__file__))


app: Flask = None  #Flask(__name__)


class ShopifyInitClass:

    def __init__(self, custom_app: Flask) -> None:
        app = custom_app

        #for enable cors
        #cors = CORS(app)

        app.config['JWT_SECRET_KEY'] = jwt_key_secret
        app.config['JWT_EXPIRES'] = datetime.timedelta(minutes= 5) 
        app.config['UPLOAD_FOLDER'] = path_to_upload
        app.config['BASE_DIR'] = basedir
        JWTManager(app)

    #@app.before_request
    #def limit_remote_addr():
    #    pass
        #if request.remote_addr != '10.20.30.40':
        #    abort(403)  # Forbidden


    #@app.before_first_request
    #def before_first_request():
    #    log_level = logging.INFO
    
    #    for handler in app.logger.handlers:
    #        app.logger.removeHandler(handler)
    
    #    root = os.path.dirname(os.path.abspath(__file__))
    #    logdir = os.path.join(root, 'logs')
    #    if not os.path.exists(logdir):
    #        os.mkdir(logdir)
    #    log_file = os.path.join(logdir, 'app.log')
    #    handler = logging.FileHandler(log_file)
    #    handler.setLevel(log_level)
    #    app.logger.addHandler(handler)
    
    #    app.logger.setLevel(log_level)



#import ShopifyTupperware.views
#import ShopifyTupperware.controllers

