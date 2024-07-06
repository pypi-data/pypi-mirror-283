from flask import jsonify, request
from ShopifyTupperware.bloc.price_rule_bloc import PriceRuleBloc
from ShopifyTupperware.models.pricerule_model import PriceRuleSchema
from ShopifyTupperware.models.customer_model import CustomerSchema
from ShopifyTupperware.repositories.price_rule_repository import PriceRuleRepository
from ShopifyTupperware.repositories.customer_repository import CustomerRepository
#from flask_jwt_simple import jwt_required
from flask_jwt_extended import jwt_required
from ShopifyTupperware import app, jwt
from ShopifyTupperware.helper import verify_webhook
import re

class DiscountController:

    @app.route('/discount/pricerule', methods = ['POST'])
    @jwt_required()
    def create_price_rule():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            if not data['key']:
                return jsonify(Status= "Bad Request", Code= 400, Desc= "Missing key"), 400
            key = data['key']

            customer_ids = []
            if 'customer_selection' in data and data['customer_selection'] != 'all':
                if not data['email']:
                    return jsonify(Status= "Bad Request", Code= 400, Desc= "Missing email"), 400
                email = data['email']
                customer_repository = CustomerRepository()
                customers = customer_repository.getCustomerByEmail(email)
                if customers is not None:
                    customer_schema = CustomerSchema()
                    cust_models = customer_schema.dump(customers, many= True)
                    if cust_models is not None and len(cust_models) > 0:
                        customer_ids = [cust['id'] for cust in cust_models]
            schema = PriceRuleSchema()
            price_model = schema.dump(data)
            if customer_ids is not None and len(customer_ids) > 0:
                price_model['prerequisite_customer_ids'] = customer_ids
            else:
                price_model['customer_selection'] = 'all'

            if data['entitled_collection'] is not None:
                entitled_collection_ids = (str)(data['entitled_collection'])
                price_model['entitled_collection_ids'] = entitled_collection_ids.split(',')

            repository = PriceRuleRepository()
            price_rule = repository.create_price_rule(price_model)

            if not price_rule or price_rule.id is None:
                return jsonify(Status = "Not Found", Code = 404), 404

            code = data['discount_code']
            id = price_rule.id
            discount_result = repository.create_discount_price(code, id)
            #repository.update_discount_price_rule(id)
            if discount_result is not None and discount_result.id is not None:
                PriceRuleBloc.update_discount_id(key, id)
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500


    @app.route('/discount/create', methods = ['POST'])
    @jwt_required()
    def create_discount():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            if not data['key'] or not data['id'] or not data['code']:
                return jsonify(Status= "Bad Request", Code= 400, Desc= "Missing key or id or code"), 400
            repository = PriceRuleRepository()
            discount_result = repository.create_discount_price(data['code'], data['id'])
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500


    @app.route('/discount/update', methods = ['POST'])
    @jwt_required()
    def update_discount():
        try:
            data = request.get_json()
            code = data['code']
            key = data['key']
            id = data['id']
            price_repository = PriceRuleRepository()
            gid, discountCode = price_repository.get_discount_by_id(id)
            usageCount = discountCode['asyncUsageCount']
            price_repository.update_discount_limit(gid, usageCount, code)
            #sid = re.findall('\d+', gid)[0]
            #PriceRuleBloc.update_discount_id(key, id)
            return jsonify(Status= "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500
        

    @app.route('/discount/deactivate', methods = ['POST'])
    @jwt_required()
    def deactivate_discount():
        try:
            data = request.get_json()
            price_repository = PriceRuleRepository()
            id = data['id']
            key = data['key']
            price_repository.deactivate_discount(id)
            PriceRuleBloc.deactivated_discount(key)
            return jsonify(Status= "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500

#WEBHOOK
    @app.route('/discount/oncreated', methods = ['POST'])
    def discount_oncreated():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            if 'admin_graphql_api_id' in data and 'title' in data:
                gid = data['admin_graphql_api_id']
                title = data['title']
                id = re.findall('\d+', gid)[0]
                PriceRuleBloc.create_discount(id, title)
            return jsonify(Status= "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500
#/WEBHOOK
