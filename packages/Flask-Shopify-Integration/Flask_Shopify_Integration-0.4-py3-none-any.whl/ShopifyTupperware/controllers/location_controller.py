from flask import jsonify, request
from ShopifyTupperware import app
#from flask_jwt_simple import jwt_required
from flask_jwt_extended import jwt_required
from ShopifyTupperware.repositories.inventory_repository import InventoryRepository
from ShopifyTupperware.models import inventory_model, location_model
from ShopifyTupperware.data.inventory_db import LocationDb
from ShopifyTupperware.bloc.location_bloc import LocationBloc
from ShopifyTupperware.models.location_model import LocationSchema
import http.client as client
import base64
from config import shopify_admin, shopify_key, shopify_pwd
from ShopifyTupperware.helper import verify_webhook

class LocationController:

    @app.route('/location')
    @jwt_required()
    def get_locations():
        repository = InventoryRepository()
        response = repository.get_locations()
        if not response:
            return jsonify(Status = "Not Found", Code = 404), 404
        schema = location_model.LocationSchema(many= True)
        results = schema.dump(response)
        return jsonify(results), 200


    @app.route('/location/<int:id>')
    @jwt_required()
    def get_location(id):
        repository = InventoryRepository()
        response = repository.get_location(id)
        if not response:
            return jsonify(Status = "Not Found", Code = 404), 404
        schema = location_model.LocationSchema()
        results = schema.dump(response)
        return jsonify(results), 200


    @app.route('/location', methods= ['POST'])
    @jwt_required()
    def save_location():
        try:
            data = request.get_json()
            if not data or not data['key']:
                return jsonify(Status = "Not Found", Code = 404), 404
            schema = location_model.LocationSchema()
            location = schema.dump(data)
            repository = InventoryRepository()
            response = repository.save_location(location)
            if not response:
                return jsonify(Status = "Not Found", Code = 404), 404
            location = schema.dump(response)
            if location['id'] is not None:
                LocationDb.update_location(data['key'], location['id'])
            return jsonify(location), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500


    @app.route('/location/order/<int:id>')
    @jwt_required()
    def get_location_order(id):
        try:
            host_url = str.format('%s/orders/%d/fulfillment_orders.json' %(shopify_admin, id))
            connection = client.HTTPSConnection(host_url, 443)
            key = str.format('%s:%s' %(shopify_key, shopify_pwd))
            token_enc = base64.b64encode(key.encode()).decode()
            auth_schema = 'Basic %s' %token_enc
            #url = str.format('orders/%d/fulfillment_orders.json' %id)
            connection.request('GET', '', None, {'Authorization': auth_schema, 'Accept': 'application/json','Content-Type': 'application/json'})
            res = connection.getresponse()
            data = res.read()
            print(data)
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

#WEBHOOK


    @app.route('/location/oncreate', methods= ['POST'])
    def location_oncreate():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            schema = LocationSchema()
            location = schema.dump(data)
            LocationBloc.create_location(location)
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

    @app.route('/location/onupdate', methods= ['POST'])
    def location_onupdate():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            schema = LocationSchema()
            location = schema.dump(data)
            LocationBloc.update_location(location)
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

#END WEBHOOK