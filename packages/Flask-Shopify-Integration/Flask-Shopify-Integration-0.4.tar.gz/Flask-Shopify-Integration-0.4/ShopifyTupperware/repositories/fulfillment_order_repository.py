from ShopifyTupperware.repositories.repository import Repository
from shopify import FulfillmentOrders
from config import shopify_admin, shopify_key, shopify_pwd
import http.client as client
import base64
import requests
import json

class FulfillmentOrderRepository(Repository):

    def get_fulfillment_order(self, order_id):
        fulfillment_orders = FulfillmentOrders()
        return fulfillment_orders.find(order_id=order_id)


    @staticmethod
    def submit_order_fulfillment(fulfillment_order_id):
        try:
            host_url = str.format('%s/fulfillment_orders/%d/fulfillment_request.json' %(shopify_admin,fulfillment_order_id))
            connection = client.HTTPSConnection(host_url, 443)
            key = str.format('%s:%s' %(shopify_key, shopify_pwd))
            token_enc = base64.b64encode(key.encode()).decode('utf-8')
            auth_schema = 'Basic %s' %token_enc
            #headers = {'X-Shopify-Access-Token': shopify_pwd, 'Content-Type': 'application/json'}
            headers = {'Authorization': auth_schema}
            #connection.request('POST', '', body= None, headers= headers)
            #res = connection.getresponse()

            res  = requests.post(host_url, headers= headers)
            #data = res.read()
            print(res)
        except Exception as ex:
            raise ex


    @staticmethod
    def accept_order_fulfillment(fulfillment_order_id):
        try:
            host_url = str.format('%s/fulfillment_orders/%d/fulfillment_request/accept.json' %(shopify_admin,fulfillment_order_id))
            connection = client.HTTPSConnection(host_url, 443)
            key = str.format('%s:%s' %(shopify_key, shopify_pwd))
            token_enc = base64.b64encode(key.encode()).decode('utf-8')
            auth_schema = 'Basic %s' %token_enc
            #headers = {'X-Shopify-Access-Token': shopify_pwd, 'Content-Type': 'application/json'}
            headers = {'Authorization': auth_schema}
            #connection.request('POST', '', body= None, headers= headers)
            #res = connection.getresponse()

            res  = requests.post(host_url, headers= headers)
            #data = res.read()
            print(res)
        except Exception as ex:
            raise ex


    @staticmethod
    def open_order_fulfillment(fulfillment_order_id):
        try:
            host_url = str.format('%s/fulfillment_orders/%d/open.json' %(shopify_admin,fulfillment_order_id))
            #connection = client.HTTPSConnection(host_url, 443)
            key = str.format('%s:%s' %(shopify_key, shopify_pwd))
            token_enc = base64.b64encode(key.encode()).decode('utf-8')
            auth_schema = 'Basic %s' %token_enc
            #headers = {'X-Shopify-Access-Token': shopify_pwd, 'Content-Type': 'application/json'}
            headers = {'Authorization': auth_schema}
            #connection.request('POST', '', body= None, headers= headers)
            #res = connection.getresponse()

            res  = requests.post(host_url, headers= headers)
            if not res.ok:
                raise Exception('Failed to fulfill.')
            return res.json()
        except Exception as ex:
            raise ex


    @staticmethod
    def move_fulfillment_orders(fulfillment_order_id, new_location_id):
        try:
            host_url = str.format('%s/fulfillment_orders/%d/move.json' %(shopify_admin, fulfillment_order_id))
            key = str.format('%s:%s' %(shopify_key, shopify_pwd))
            token_enc = base64.b64encode(key.encode()).decode('utf-8')
            auth_schema = 'Basic %s' %token_enc
            headers = {'Authorization': auth_schema}
            body = {"fulfillment_order": {"new_location_id": new_location_id}}#"fulfillment_order_line_items": []
            res  = requests.post(host_url, json= body, headers= headers)
            if not res.ok:
                raise Exception('Failed to fulfill.')
            return res.json()
        except Exception as ex:
            raise ex


    @staticmethod
    def approve_order_fulfillment(obj):
        try:
            host_url = str.format('%s/fulfillments.json' %(shopify_admin))
            #connection = client.HTTPSConnection(host_url, 443)
            key = str.format('%s:%s' %(shopify_key, shopify_pwd))
            token_enc = base64.b64encode(key.encode()).decode('utf-8')
            auth_schema = 'Basic %s' %token_enc
            headers = {'Authorization': auth_schema }
            body = {"fulfillment" : obj }
            res  = requests.post(host_url, json= body, headers= headers)
            #print(res.content)
            #print(res.json())
            if not res.ok:
                raise Exception('Failed to fulfill.')
            return res.json()

        except Exception as ex:
            raise ex


    
    def get_fulfillment_orders_by_orderid(self, order_id):
        try:
            fulfillment_order = FulfillmentOrders.find(order_id= order_id)
            return fulfillment_order
        except Exception as ex:
            return None

