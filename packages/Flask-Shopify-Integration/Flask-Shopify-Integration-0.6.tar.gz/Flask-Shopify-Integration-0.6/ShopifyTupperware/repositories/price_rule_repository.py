from ShopifyTupperware.repositories.repository import Repository
from shopify import PriceRule, DiscountCode, GraphQL
import json

class PriceRuleRepository(Repository):

    def create_price_rule(self, data):
        price_rule = PriceRule(data)
        price_rule.save()
        return price_rule

    def create_discount_price(self, code, price_id):
        discount_code = DiscountCode({"price_rule_id": price_id})
        discount_code.code= code
        discount_code.save()
        return discount_code

    def update_discount_price_rule(self, id):
        try:
            GraphQL().execute('mutation discountCodeBasicUpdate($basicCodeDiscount: DiscountCodeBasicInput!, $id: ID!) {\
                                  discountCodeBasicUpdate(basicCodeDiscount: $basicCodeDiscount, id: $id) {\
                                    codeDiscountNode {\
                                      id\
                                    }\
                                    userErrors {\
                                      field\
                                      message\
                                    }\
                                  }\
                                }', 
                              variables= {"basicCodeDiscount": {
                                                "combinesWith": {
                                                  "orderDiscounts": True,
                                                  "productDiscounts": True,
                                                  "shippingDiscounts": False
                                                }
                                              },
                                              "id": "gid://shopify/DiscountCodeNode/%d" %(id)}, 
                              operation_name= 'discountCodeBasicUpdate')
            return 0
        except Exception as ex:
            raise ex


        
    def get_discount_by_code(self, code):
        try:
            response = GraphQL().execute('query codeDiscountNodeByCode($code: String!) {\
                                          codeDiscountNodeByCode(code: $code) {\
                                            codeDiscount {\
                                              ... on DiscountCodeBasic {\
                                                title\
                                                asyncUsageCount\
                                                codeCount\
                                              }\
                                            }\
                                            id\
                                          }\
                                        }', 
                                        variables={"code": str(code)}, 
                                        operation_name="codeDiscountNodeByCode")
            data = json.loads(response)
            data = data['data']['codeDiscountNodeByCode']
            id = data['id']
            codeDiscount = data['codeDiscount']
            return id, codeDiscount
        except Exception as ex:
            return None

    def get_discount_by_id(self, id):
        try:
            response = GraphQL().execute('query codeDiscountNode($id: ID!) {\
                                            codeDiscountNode(id: $id) {\
                                                id\
                                                codeDiscount {\
                                                    ... on DiscountCodeBasic {\
                                                        title\
                                                        summary\
                                                        asyncUsageCount\
                                                        codeCount\
                                                    }\
                                                }\
                                            }\
                                        }',
                                        variables={"id": "gid://shopify/DiscountCodeNode/%d" %id}, 
                                        operation_name="codeDiscountNode")
            data = json.loads(response)
            data = data['data']['codeDiscountNode']
            id = data['id']
            codeDiscount = data['codeDiscount']
            return id, codeDiscount
        except Exception as ex:
            return None

    def update_discount_limit(self, id, limit, code):
        try:
            response = GraphQL().execute('mutation discountCodeBasicUpdate(\
                                          $id: ID!\
                                          $basicCodeDiscount: DiscountCodeBasicInput!\
                                ) {\
                                    discountCodeBasicUpdate(id: $id, basicCodeDiscount: $basicCodeDiscount) {\
                                    codeDiscountNode {\
                                        codeDiscount {\
                                        ... on DiscountCodeBasic {\
                                            title\
                                            codes(first: 10) {\
                                            nodes {\
                                                code\
                                            }\
                                            }\
                                            startsAt\
                                            endsAt\
                                            appliesOncePerCustomer\
                                        }\
                                        }\
                                    }\
                                    userErrors {\
                                        field\
                                        code\
                                        message\
                                    }\
                                    }\
                                }', 
                              variables={"id": id, 
                                         "basicCodeDiscount":{
                                             "code": code,
                                             "appliesOncePerCustomer": True,
                                             "usageLimit": int(limit)+1
                                          }
                                        }, 
                              operation_name="discountCodeBasicUpdate")
            return response
        except Exception as ex:
            return None

    def deactivate_discount(self, id):
        try:
            response = GraphQL().execute('mutation discountCodeDeactivate($id: ID!) {\
                                  discountCodeDeactivate(id: $id) {\
                                    codeDiscountNode {\
                                      codeDiscount {\
                                        ... on DiscountCodeBasic {\
                                          title\
                                          status\
                                          startsAt\
                                          endsAt\
                                        }\
                                      }\
                                    }\
                                    userErrors {\
                                      field\
                                      code\
                                      message\
                                    }\
                                  }\
                                }', 
                                variables={"id": "gid://shopify/DiscountCodeNode/%d" %id},
                                operation_name="discountCodeDeactivate")
            return response
        except Exception as ex:
            return None