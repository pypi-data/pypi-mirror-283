from flask import jsonify, request
#from flask_jwt_simple import jwt_required
from flask_jwt_extended import jwt_required
from ShopifyTupperware.bloc.product_bloc import ProductBloc
from ShopifyTupperware import app
from ShopifyTupperware.helper import verify_webhook
from ShopifyTupperware.repositories.product_repository import ProductRepository
from ShopifyTupperware.models.product_model import ProductSchema, ProductSchema2
from ShopifyTupperware.models.image_model import ProductImageSchema, ImageSchema
from ShopifyTupperware.data.product_db import ProductDb
from ShopifyTupperware.bloc.collection_bloc import CollectionBloc
from ShopifyTupperware.models.collection_model import CollectionModel
import requests
import base64

class ProductController:


    @app.route('/product/page')
    @jwt_required()
    def get_product_page():
        try:
            repository = ProductRepository()
            response = repository.get_products_by_status('published')
            if not response:
                return jsonify(Status = "Not Found", Code = 404), 404
            schema = ProductSchema(many = True)
            results = schema.dump(response)
            for model in results:
                ProductBloc.add_update_product_list(model)
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500


    #get all product from shopify
    @app.route('/product')
    @jwt_required()
    def get_products():
        try:
            repository = ProductRepository()
            response = repository.get_products()
            if not response:
                return jsonify(Status = "Not Found Product", Code = 404), 404
            schema = ProductSchema(many = True)
            results = schema.dump(response)
            return jsonify(results), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500
        

    #get product by id from shopify
    @app.route('/product/<int:id>')
    @jwt_required()
    def get_product(id):
        try:
            repository = ProductRepository()
            response = repository.get_product(id)
            if not response:
                return jsonify(Status = "Not Found", Code = 404), 404
            schema = ProductSchema()
            results = schema.dump(response)
            return jsonify(results), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

       
    #save product to Shopify from api
    @app.route('/product', methods = ['POST'])
    @jwt_required()
    def save_product():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            if not data['key']:
                return jsonify(Status= "Bad Request", Code= 400, Desc= "Missing primary key 'key'"), 400

            schema = ProductSchema()
            repository = ProductRepository()
            product = schema.dump(data)
            model = repository.save_update_product(product)
            result = schema.dump(model)
            key = product['key']
            id = result['id']
            if ('collection_id' in data and data['collection_id'] is not None) and ('id' in result and result['id'] is not None):
                collection_id = (str)(data['collection_id'])
                if collection_id != '':
                    collection_ids = collection_id.split(',')
                    for col_id in collection_ids:
                        repository.add_product_to_collection(col_id, result['id'])
                  
            if 'images' not in result or len(result['images']) == 0:
                ProductBloc.update_product(key, result)
                return jsonify(Status = "OK", Code = 200), 200

            [new_img.update({'key': img['key']}) for img in product['images'] for new_img in result['images'] if img['alt'] == new_img['alt']]        
            ProductBloc.create_or_update_product_image(key, result, result['images'])
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500
        


    #save product to Shopify from database results
    @app.route('/product/save', methods = ['POST'])
    @jwt_required()
    def save_product_from_db():
        try:
            list_products = ProductDb.query.filter((ProductDb.is_sync == False) | (ProductDb.is_sync == None)).all()
            if not list_products:
                return jsonify(Status = "Not New Product Found", Code = 404), 404
            schema = ProductSchema(many= True)
            results = schema.dump(list_products)
             
            for product in results:
                key = product['key']
                repository = ProductRepository()
                model = repository.save_update_product(product)
                if model is not None:
                    new_schema = ProductSchema()
                    result = new_schema.dump(model)
                    ProductBloc.update_product(key, result)
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

    #delete product by id
    @app.route('/product/delete/<int:id>', methods= ['DELETE'])
    @jwt_required()
    def delete_product(id):
        try:
            if not id or id is None:
                return jsonify(Status = "Bad Request", Code = 400), 400

            repository = ProductRepository()
            response = repository.delete_product(id)
            if not response:
                return jsonify(Status = "Delete Error", Code = 500), 500
            return jsonify(Status= "DELETED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500 

    #update product price to shopify
    @app.route('/product/price', methods= ['POST'])
    @jwt_required()
    def update_price():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            repository = ProductRepository()
            response = repository.update_price(data)
            if not response:
                return jsonify(Status = "Update Error", Code = 500), 500
            return jsonify(Status= "UPDATED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500
      


    #published product
    @app.route('/product/publish', methods= ['POST'])
    @jwt_required()
    def update_published():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            repository = ProductRepository()
            response = repository.save_update_product(data)
            if not response:
                return jsonify(Status = "Update Error", Code = 500), 500
            return jsonify(Status= "UPDATED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500


    #update images
    @app.route('/product/images', methods= ['POST'])
    @jwt_required()
    def update_images():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            schema = ImageSchema()
            models = schema.dump(data, many= True)
            if not models or len(models) == 0:
                return jsonify(Status = "Bad Request", Code = 400), 400

            repository = ProductRepository()
            for model in models:
                attachment = base64.b64encode(requests.get(model['src']).content)
                product_id = model['product_id']
                image_id =  model['id'] if ('id' in model and model['id'] is not None) else None
                position = model['position'] if ('position' in model and model['position'] is not None) else None
                filename = model['src']
                res = repository.upload_product_image(product_id, image_id, filename, attachment, position)
                result = schema.dump(res) if res is not None else None
                if result is not None:
                    ProductBloc.update_image(model['key'], result['id'], result['product_id'])
            return jsonify(Status= "UPDATED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

    #delete images
    @app.route('/product/images/delete', methods= ['POST'])
    @jwt_required()
    def delete_images():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            schema = ImageSchema()
            models = schema.dump(data, many= True)
            if not models or len(models) == 0:
                return jsonify(Status = "Bad Request", Code = 400), 400
            repository = ProductRepository()
            for model in models:
                res = repository.delete_image(model['id'], model['product_id'])
                if res is not None:
                    ProductBloc.update_image(model['key'], None, model['product_id'])
            return jsonify(Status= "DELETED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500


    @app.route('/product/collect', methods= ['POST'])
    @jwt_required()
    def add_product_collect():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            repository = ProductRepository()
            if ('collection_id' in data and data['collection_id'] is not None) and ('product_id' in data and data['product_id'] is not None):
                collection_data= CollectionBloc.get_collection_list()
                if collection_data is not None:
                    for col_data in collection_data:
                        repository.remove_collection_from_product(col_data.id, data['product_id'])
                collection_id = (str)(data['collection_id'])
                collection_ids = collection_id.split(',')
                for col_id in collection_ids:
                    repository.add_product_to_collection(col_id, data['product_id'])
            return jsonify(Status= "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500



#WEBHOOK
    @app.route('/product/oncreated', methods = ['POST'])
    def on_created():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            schema = ProductSchema()
            model = schema.dump(data)
            ProductBloc.add_update_product_list(model)
            return jsonify(Status= "CREATED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

       
    @app.route('/product/onupdated', methods = ['POST'])
    def on_updated():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            schema = ProductSchema()
            model = schema.dump(data)
            response = ProductBloc.add_update_product_images(model)
            if not response:
                return jsonify(Status = "Update Error", Code = 500), 500
            return jsonify(Status= "UPDATED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

    @app.route("/product/ondeleted", methods=['POST'])
    def on_deleted():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            if 'id' not in data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            productDb = ProductDb()
            productDb.delete_product(data['id'])
            return jsonify(Status= "DELETED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

    @app.route('/product/collection/oncreate', methods = ['POST'])
    def collection_on_created():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            if 'id' not in data:
                return jsonify(Status = "Bad Request", Code = 400), 400

            schema = CollectionModel()
            model = schema.dump(data)
            CollectionBloc.add_new_bloc(model)
            return jsonify(Status= "CREATED", Code = 201), 201

        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

#ENDWEBHOOK   