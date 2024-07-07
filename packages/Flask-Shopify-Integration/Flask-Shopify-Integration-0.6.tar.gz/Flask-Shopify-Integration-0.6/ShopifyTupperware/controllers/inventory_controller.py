from flask import jsonify, request
from ShopifyTupperware import app
#from flask_jwt_simple import jwt_required
from flask_jwt_extended import jwt_required
from ShopifyTupperware.repositories.inventory_repository import InventoryRepository
from ShopifyTupperware.models import inventory_model, location_model

class InventoryController:

    
    @app.route('/location-inventory-level/<int:id>')
    @jwt_required()
    def get_inventory_location(id):
        repository = InventoryRepository()
        response = repository.get_inventory_level_location(id)
        if not response:
            return jsonify(Status = "Not Found", Code = 404), 404
        schema = inventory_model.InventoryLevelSchema(many= True)
        results = schema.dump(response)
        return jsonify(results), 200

    #'33331401883684,33331401916452,33332498169892'
    @app.route('/inventory-item')
    @jwt_required()
    def get_inventory_items():
        args = request.args
        if not args:
            return jsonify(Status = "Bad Request", Code = 400), 400
        ids = args['ids']
        repository = InventoryRepository()
        response = repository.get_inventory_items(ids)
        if not response:
            return jsonify(Status = "Not Found", Code = 404), 404
        schema = inventory_model.InventoryItemSchema(many= True)
        results = schema.dump(response)
        return jsonify(results), 200

    @app.route('/inventory-item/<int:id>')
    @jwt_required()
    def get_inventory_item(id):
        repository = InventoryRepository()
        response = repository.get_inventory_item(id)
        if not response:
            return jsonify(Status = "Not Found", Code = 404), 404
        schema = inventory_model.InventoryItemSchema()
        results = schema.dump(response)
        return jsonify(results), 200

    #connect location id with inventory item id
    @app.route('/inventory-level/connect', methods=['POST'])
    @jwt_required()
    def connect_inventory_level():
        data = request.get_json()
        if not data:
            return jsonify(Status = "Not Found", Code = 404), 404
        schema = inventory_model.InventoryLevelSchema()
        model = schema.dump(data)
        repository = InventoryRepository()
        repository.connect_inventory_level(model['location_id'], model['inventory_item_id'])
        return jsonify(Status = "OK", Code = 200), 200

    #adjust stock in location id and inventory item id
    @app.route('/inventory-level/adjust', methods=['POST'])
    @jwt_required()
    def adjust_inventory_level():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            schema = inventory_model.InventoryLevelSchema()
            model = schema.dump(data)
            repository = InventoryRepository()
            repository.adjust_inventory_level(model['location_id'], model['inventory_item_id'], model['available'])
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500
        

    #set stock in location id and inventory item id
    @app.route('/inventory-level/set', methods=['POST'])
    @jwt_required()
    def set_inventory_level():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            schema = inventory_model.InventoryLevelSchema()
            model = schema.dump(data)
            repository = InventoryRepository()
            repository.set_inventory_level(model['location_id'], model['inventory_item_id'], model['available'])
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500
       





