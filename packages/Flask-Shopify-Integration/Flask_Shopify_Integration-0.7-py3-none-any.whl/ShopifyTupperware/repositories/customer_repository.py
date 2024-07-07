from ShopifyTupperware.repositories.repository import Repository
from shopify import Customer, CustomerInvite, GiftCard, Metafield, GraphQL
import json
import http.client as client
import base64
import requests
from config import shopify_store_key, shopify_store_gql

class CustomerRepository(Repository):

    def findCustomer(self, id):
        customer = Customer()
        customer = customer.find(id_ = id)
        return customer

    def saveCustomer(self, data):
        customer = Customer()
        return customer.create(data)

    def updateCustomer(self, data):
        customer = Customer(data)
        return customer.save()

    def updateCustomerTags(self, id, tags):
       customer = Customer()
       customer = customer.find(id_ = id)
       if not customer:
           return None
       customer.tags = tags
       return customer.save()

    def getCustomerByEmail(self, email):
       customer = Customer()
       return customer.search(query = ('email:%s' %email))


    def inviteCustomer(self, id):
       customer = Customer()
       customer.id=id
       customer.send_invite()
       return customer
       

    def createGiftCardToCustomer(self, data):
        try:
           gift = GiftCard()
           return gift.create(data)
        except Exception as ex:
            raise ex

    def disableGiftCard(self, id):
        try:
           gift = GiftCard.find(id_ = id)
           if not gift:
               return None
           gift.disable()
           return True
        except Exception as ex:
            raise ex

    def getCustomerMetaById(self, id):
        try:
            response = GraphQL().execute('query customer($id: ID!){\
                                          customer(id: $id) {\
                                            id\
                                            firstName\
                                            lastName\
                                            email\
                                            phone\
                                            note\
                                            verifiedEmail\
                                            validEmailAddress\
                                            tags\
                                            metafield(namespace: "custom", key: "voucher") {\
                                                id\
                                                value\
                                                namespace\
                                            }\
                                          }\
                                        }', variables={"id": "gid://shopify/Customer/%d" %id}, operation_name= "customer")
            data = json.loads(response)
            if 'data' in data and data['data'] is not None:
                data = data['data']
                customer = data['customer'] if 'customer' in data else None
                if customer is not None:
                    metafield = customer['metafield']
                    if metafield is not None and 'id' in metafield :
                        return metafield['id'], metafield['value']
            return None,None
        except Exception as ex:
            return None,None

    def createCustomerMeta(self, customer_id, value):
        try:
            metafield = Metafield()
            metafield.owner_id = customer_id
            metafield.owner_resource = "customer"
            metafield.namespace = "custom"
            metafield.key = "voucher"
            metafield.value= "["+(",".join(value))+"]"
            metafield.type ="list.single_line_text_field"
            metafield.save()
            return metafield
        except Exception as ex:
            raise ex


    def sendCustomerRecoverPassword(self, email):
        try:
            host_url = str.format('%s' %(shopify_store_gql))
            headers = {'X-Shopify-Storefront-Access-Token': '%s'%(shopify_store_key),  'Content-Type': 'application/json'}
            
            data = ('mutation SendPasswordResetEmail {\
                                          customerRecover(email: "%s") {\
                                            customerUserErrors {\
                                              code\
                                              message\
                                            }\
                                            userErrors {\
                                              message\
                                            }\
                                          }\
                                        }' %(email))
            res  = requests.post(host_url, json= { "query": data }, headers= headers)
            return 0
        except Exception as ex:
            raise ex
