from flask import jsonify, request
from ShopifyTupperware.bloc.customer_bloc import CustomerBloc
from ShopifyTupperware.models.customer_model import CustomerSchema, Customer2Schema, GiftCardSchema
from ShopifyTupperware.repositories.customer_repository import CustomerRepository
#from flask_jwt_simple import jwt_required
from flask_jwt_extended import jwt_required
from ShopifyTupperware import app
from ShopifyTupperware.helper import verify_webhook
import json
import re

class CustomerController:

    @app.route('/customer/get/<string:email>')
    @jwt_required()
    def find_customer_by_email(email):
        try:
            repository = CustomerRepository()
            response = repository.getCustomerByEmail(email)
            if not response:
                return jsonify(Status = "Not Found", Code = 404), 404
            schema = Customer2Schema()
            customer = schema.dump(response, many= True)
            return jsonify(customer), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

    @app.route('/customer/find/<int:id>')
    @jwt_required()
    def find_customer_by_id(id):
        try:
            repository = CustomerRepository()
            response = repository.findCustomer(id)
            if not response:
                return jsonify(Status = "Not Found", Code = 404), 404
            schema = Customer2Schema()
            customer = schema.dump(response)
            return jsonify(customer), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500



    @app.route('/customer/new', methods = ['POST'])
    @jwt_required()
    def create_customer():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            if not data['key'] or not data['email'] or not data['first_name'] or not data['last_name']:
                return jsonify(Status= "Bad Request", Code= 400, Desc= "Missing key email or tags"), 400

            customer_key = data['key']
            #address_keys = [addr['key'] for addr in data['addresses']]

            if 'password' in data and data['password'] is not None:
                data['password_confirmation'] = data['password']

            schema = Customer2Schema()
            customer = schema.dump(data)
            repository = CustomerRepository()
            if customer['id'] is not None:
                temp = repository.updateCustomer(customer)
                CustomerBloc.update_status(customer_key)
                return jsonify(Status = "OK", Code = 200), 200
            model = repository.saveCustomer(customer)
            if model is not None:
                temp = schema.dump(model)
                if temp['id'] is None:
                    return jsonify(Status = "Bad Request", Code = 400), 400
                if temp['send_email_invite'] is not None and temp['send_email_invite'] == True:
                    repository.inviteCustomer(temp['id'])
                CustomerBloc.update_customer_id(customer_key, temp)
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

    @app.route('/customer/edit', methods = ['POST'])
    @jwt_required()
    def update_customer():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            if not data['id'] or not data['tags']:
                return jsonify(Status= "Bad Request", Code= 400, Desc= "Missing id or tags"), 400
            repository = CustomerRepository()
            model = repository.updateCustomerTags(id=data['id'], tags=data['tags'])
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500


    @app.route('/customer/metafield', methods = ['POST'])
    @jwt_required()
    def update_customer_metafield():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            if 'email' not in data:
                return jsonify(Status = "Bad Request", Code = 400), 400

            types=''
            if 'types' not in data:
                types='update'
            else:
                types = data['types']

            email = data['email']
            schema = Customer2Schema()
            customer: Customer2Schema = None
            repository = CustomerRepository()
            exist_customer = CustomerBloc.check_customer_by_email(email)
            if exist_customer is not None and  exist_customer.id is not None:
                customer = schema.dump(exist_customer)
            else:
                response = repository.getCustomerByEmail(email)
                if not response:
                    return jsonify(Status = "Not Found", Code = 404), 404
                customers = schema.dump(response, many= True)
                customer = customers[0]
            gid, current_values = repository.getCustomerMetaById(customer['id'])
            if current_values is None:
                current_values= '[]'
            current_values = current_values.replace('[', '').replace(']','')
            values =  current_values.split(',') if current_values != '' else []
            temp = "\"Kode Voucher: %s - %s Expired: %s\"" %(data['voucher_code'], data['voucher_amount'], data['voucher_expired'])
            if types == 'delete':
                if temp in values:
                    values.remove(temp)
            else:
                if temp not in values:
                    values.append(temp)
            repository.createCustomerMeta(customer['id'], values)
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

    @app.route('/customer/recover-password', methods = ['POST'])
    @jwt_required()
    def recovery_password():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            if 'email' not in data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            email = data['email']
            repository = CustomerRepository()
            response = repository.sendCustomerRecoverPassword(email)
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500


#WEBHOOK CUSTOMER
    #on created customer in shopify will trigger
    @app.route('/customer/oncreated', methods = ['POST'])
    def on_customer_created():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            schema = CustomerSchema()
            model = schema.dump(data)
            CustomerBloc.create(model)
            return jsonify(Status= "CREATED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500


    @app.route('/customer/ondeleted', methods = ['POST'])
    def on_customer_deleted():
        try:
            if not verify_webhook(request.get_data(), request.headers):
                return jsonify(Status= "UNAUTHORIZED", Code = 401), 401
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request", Code = 400), 400
            schema = CustomerSchema()
            model = schema.dump(data)
            CustomerBloc.delete_customer(model)
            return jsonify(Status= "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

#/WEBHOOK CUSTOMER

    @app.route('/customer/gift', methods=['POST'])
    def create_customer_gift():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Bad Request. Body request is required", Code = 400), 400
            if 'email' not in data or 'key' not in data:
                return jsonify(Status = "Bad Request. key and email must contain in body request", Code = 400), 400

            repository = CustomerRepository()
            customers = repository.getCustomerByEmail(data['email'])
            if not customers:
                return jsonify(Status = "Not Found", Code = 404), 404

            schema = CustomerSchema()
            models = schema.dump(customers, many= True)
            if not models or len(models) == 0:
                return jsonify(Status = "Not Found", Code = 404), 404

            customer = models[0]
            data['customer_id'] = customer['id']

            gift = repository.createGiftCardToCustomer(data)

            if not gift:
                return jsonify(Status = "Not Found", Code = 404), 404

            gift_schema = GiftCardSchema()
            gift_data = gift_schema.dump(gift)

            if not gift_data:
                return jsonify(Status = "Not Found", Code = 404), 404

            CustomerBloc.update_customer_gift(data['key'], gift_data)

            return jsonify(Status= "CREATED", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500
        
    @app.route('/customer/gift-disable', methods=['POST'])
    def customer_gift_disabled():
        try:
            data = request.get_json()
            if not data:
                return jsonify(Status = "Not Found", Code = 404), 404
            if 'id' not in data:
                return jsonify(Status = "Not Found", Code = 404), 404

            repository = CustomerRepository()
            repository.disableGiftCard(data['id'])
            return jsonify(Status= "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

