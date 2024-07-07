from flask import jsonify, request
from ShopifyTupperware.models.fullfilment_model import FullfilmentSchema, FulfillmentOrderSchema, FulfillmentV2Schema
from ShopifyTupperware.models.transaction_model import TransactionSchema
#from flask_jwt_simple import jwt_required
from flask_jwt_extended import jwt_required
from ShopifyTupperware import app
from ShopifyTupperware.repositories.order_repository import OrderRepository
from ShopifyTupperware.repositories.fulfillment_order_repository import FulfillmentOrderRepository
from ShopifyTupperware.repositories.fulfillment_repository import FulfillmentRepository
from ShopifyTupperware.repositories.price_rule_repository import PriceRuleRepository
from ShopifyTupperware.models.order_model import OrderSchema
from ShopifyTupperware.bloc.order_bloc import OrderBloc
from ShopifyTupperware.data.order_db import OrderDb
from ShopifyTupperware.bloc.price_rule_bloc import PriceRuleBloc
from ShopifyTupperware.helper import verify_webhook
from config import shopify_admin, shopify_key, shopify_pwd
import http.client as client
import base64
import requests
import json

class OrderController:

    @app.route('/order/updatelocation', methods= ['POST'])
    @jwt_required()
    def update_location_id():
        try:
            data = request.get_json()
            if not data and 'id' not in data and data['id'] is None:
                return jsonify(Status= "Bad Request", Code = 400), 400 
            key = data['key']
            fulfillment_repository = FulfillmentOrderRepository()
            results = fulfillment_repository.get_fulfillment_orders_by_orderid(data['id'])
            if results is not None:
                fulfillment_order_schema = FulfillmentOrderSchema()
                fulfillment_orders = fulfillment_order_schema.dump(results, many= True)
                location_id = fulfillment_orders[0]['assigned_location_id']
                OrderBloc.update_order_locationid(key, location_id)
                #return jsonify(Status= "OK", Code = 200, LocationId=location_id), 200
            return jsonify(Status= "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500


    #get order list from shopify
    @app.route('/order')
    @jwt_required()
    def get_orders():
        order_repository = OrderRepository()
        response = order_repository.get_orders()
        if not response:
            return jsonify(Status= "NOT FOUND", Code = 404), 404
        schema = OrderSchema(many = True)
        results = schema.dump(response)
        return jsonify(results), 200



    #get order by id from shopify
    @app.route('/order/<int:id>')
    #@jwt_required
    def get_order(id):
        order_repository = OrderRepository()
        response = order_repository.get_order(id)
        if not response:
            return jsonify(Status= "NOT FOUND", Code = 404), 404
        schema = OrderSchema()
        results = schema.dump(response)
        #if OrderBloc.order_exist(results['id']) is None:
        #    OrderBloc.save_order(results)
        return jsonify(results), 200


    @app.route('/order/paid', methods= ['GET'])
    @jwt_required()
    def get_order_list_paid():
        try:
            order_repository = OrderRepository()
            results = order_repository.get_order_paid()
            if not results:
                return jsonify(Status= "NOT FOUND", Code = 404), 404
            schema = OrderSchema(many=True)
            models = schema.dump(results)
            for model in models:
                OrderDb.update_checkoutid(model['id'], model['checkout_id'])
            return jsonify(models), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500



    #get order list pagination
    @app.route('/order/list' ,methods= ['POST'])
    @jwt_required()
    def get_orders_page():
        try:
            data = request.get_json()
            if not data or 'date_start' not in data or 'date_end' not in data:
                return jsonify(Status= "BAD REQUEST", Code = 400), 400
            date_start = data['date_start']
            date_end = data['date_end']
            order_repository = OrderRepository()
            response = order_repository.get_order_page(date_start, date_end) #"2020-02-01T00:00:00"
            if not response:
                return jsonify(Status= "NOT FOUND", Code = 404), 404
            schema = OrderSchema(many = True)
            results = schema.dump(response)
            order_length = len(results)
            for order in results:
                if OrderBloc.order_exist(order['id']) is None:
                    OrderBloc.save_order(order)
            return jsonify(Status= "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500



    @app.route('/order/transaction/<int:id>')
    @jwt_required()
    def get_order_transactions(id):
        try:
            orderRepostory = OrderRepository()
            transaction = orderRepostory.get_transaction_by_orderid(id)
            transSchema = TransactionSchema(many = True)
            results = transSchema.dump(transaction)
            return jsonify(results), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500


    #update order
    @app.route('/order/update', methods= ['POST'])
    @jwt_required()
    def update_status():
        data = request.get_json()
        if not data:
            return jsonify(Status= "BAD REQUEST", Code = 400), 400

        schema = OrderSchema()
        order = schema.dump(data)
        order_repository = OrderRepository()
        response = order_repository.update_order(order)
        if not response:
            return jsonify(Status= "NOT FOUND", Code = 404), 404
        return jsonify(Status= "OK", Code= 200), 200


    #paid order by payment gateway
    @app.route('/order/paid', methods= ['POST'])
    @jwt_required()
    def order_paid():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status= "BAD REQUEST", Code = 400), 400
            schema = TransactionSchema()
            transaction = schema.dump(data)
            order_repository = OrderRepository()
            response = order_repository.paid_order(transaction)
            if not response:
                return jsonify(Status= "NOT FOUND", Code = 404), 404
            return jsonify(Status= "OK", Code= 200), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500


    
    #fulfillment order
    @staticmethod
    def approve_order_fulfillment(obj):
        try:
            host_url = str.format('%s/fulfillments.json' %(shopify_admin))
            key = str.format('%s:%s' %(shopify_key, shopify_pwd))
            token_enc = base64.b64encode(key.encode()).decode('utf-8')
            auth_schema = 'Basic %s' %token_enc
            headers = {'Authorization': auth_schema }
            body = {"fulfillment" : obj }
            res  = requests.post(host_url, json= body, headers= headers)
            if not res.ok:
                raise Exception('Failed to fulfill.')
            return res.json()
        except Exception as ex:
            raise ex

    @app.route('/order/shipped', methods= ['POST'])
    @jwt_required()
    def order_fulfilled():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status= "BAD REQUEST", Code = 400), 400
            schema = FullfilmentSchema()
            fulfillment = schema.dump(data)

            fulfillment_order_repo = FulfillmentOrderRepository()
            temp = fulfillment_order_repo.get_fulfillment_order(fulfillment['order_id'])
            root_schema = FulfillmentOrderSchema(many= True)
            fulfillment_order = root_schema.dump(temp)

            if fulfillment_order is None or len(fulfillment_order) == 0:
                return jsonify(Status= "Not Found", Code = 404), 404

            if fulfillment_order[0]['line_items'] is None or len(fulfillment_order[0]['line_items']) == 0:
                return jsonify(Status= "Not Found", Code = 404), 404

            for item in fulfillment_order:
                if item['assigned_location_id'] == data['location_id']:
                    continue
                FulfillmentOrderRepository.move_fulfillment_orders(item['id'], fulfillment['location_id'])

            #temps = []
            #temps2 = []
            #for item in fulfillment_order:
            #    for item2 in item['line_items']:
            #        temps2.append({"id": item2['id'], "quantity": item2['quantity']})
            #    temps.append({"fulfillment_order_id": item['id'], "fulfillment_order_line_items": temps2})
            #    temps2=[]

            temps = [
                {
                    "fulfillment_order_id": item['id'],
                    "fulfillment_order_line_items": [
                        {"id": item2['id'], "quantity": item2['quantity']}
                        for item2 in item['line_items']
                    ]
                }
                for item in fulfillment_order
            ]

            obj = {
                "message": str.format("Order number %d already fulfill by %s" %(fulfillment['order_id'], fulfillment['tracking_company'])),
                "line_items_by_fulfillment_order": temps,
                "notify_customer": fulfillment['notify_customer'],
                "tracking_info": {
                    "company" : fulfillment['tracking_company'],
                    "number" : fulfillment['tracking_number'],
                    "url" : fulfillment['tracking_url']
                    },
                }

            result = FulfillmentOrderRepository.approve_order_fulfillment(obj)

            return jsonify(result), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500

    @app.route('/order/completed', methods= ['POST'])
    @jwt_required()
    def order_fulfillment_completed():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status= "BAD REQUEST", Code = 400), 400

            if ('id' not in data) or ('order_id' not in data):
                return jsonify(Status= "BAD REQUEST", Code = 400), 400

            order_repository = OrderRepository()
            response = order_repository.completed_order(data['id'], data['order_id'])
            if not response:
                return jsonify(Status= "NOT FOUND", Code = 404), 404
            return jsonify(Status= "OK", Code= 200), 200

        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500

       

    #cancel order in shopify if order expired or canceled by system
    @app.route('/order/cancel/<int:id>', methods = ['PUT'])
    @jwt_required()
    def cancel_order(id):
        order_repository = OrderRepository()
        response = order_repository.cancel_order(id)
        if not response:
            return jsonify(Status= "NOT FOUND", Code = 404), 404
        return jsonify(Status= "OK", Code= 200), 200

#WEBHOOK

    #order created by shopify, setting order created on shopify in paid or unpaid
    @app.route('/order/oncreated', methods = ['POST'])
    def save_order():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            #print(data)
            schema = OrderSchema()
            order = schema.dump(data)
            if OrderBloc.order_exist(order['id']) is None:
                OrderBloc.save_order(order)
                return jsonify(Status= "CREATED", Code = 201), 201
            return jsonify(Status= "CREATED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500

        
    #order paid from shopify will trigger here
    @app.route('/order/onpaid', methods = ['POST'])
    def edit_order():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            #print(data)
            schema = OrderSchema()
            order = schema.dump(data)
            if OrderBloc.order_exist(order['id']) is not None:
                return jsonify(Status= "CREATED", Code = 200), 200
            OrderBloc.save_order(order)
            return jsonify(Status= "CREATED", Code = 201), 201
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500

        

    #order deleted from shopify
    @app.route('/order/ondeleted', methods = ['POST'])
    def remove_order():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            schema = OrderSchema()
            order = schema.dump(data)
            return jsonify(Status= "DELETED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500

    #order cancel or expired from shopify
    @app.route('/order/oncanceled', methods = ['POST'])
    def canceled_order():
        try:
            #if not verify_webhook(request.get_data(), request.headers):
            #    return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            schema = OrderSchema()
            order = schema.dump(data)

            if 'discount_applications' in order and order['discount_applications'] is not None and len(order['discount_applications']) > 0:
                voucher_codes = []
                for voucher in order['discount_applications']:
                    codes=''
                    amount = voucher['value']
                    disc_type = voucher['value_type']
                    if 'code' in voucher and voucher['code'] is not None:
                        codes = voucher['code']
                    elif 'title' in voucher and voucher['title'] is not None:
                        codes = voucher['title']
                    code = str(codes).split('|')
                    for c in code:
                        c = str(c).strip()
                        if c in voucher_codes:
                            continue
                        voucher_codes.append(c)
                        PriceRuleBloc.insert_update_discount(order['id'], c, amount, disc_type)

            #if 'discount_codes' in order and order['discount_codes'] is not None and len(order['discount_codes']) > 0:
            #    for voucher in order['discount_codes']:
            #        code = voucher['code']
            #        amount = voucher['amount']
            #        disc_type = voucher['type']
            #        PriceRuleBloc.insert_update_discount(order['id'], code, amount, disc_type)
            return jsonify(Status= "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status= "ERROR", Code = 500, Desc = ex.args), 500

#/WEBHOOK