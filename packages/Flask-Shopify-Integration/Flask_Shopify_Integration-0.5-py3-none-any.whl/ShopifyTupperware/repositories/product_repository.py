from ShopifyTupperware.repositories.repository import Repository
from shopify import Product, Collect, SmartCollection, Variant, Image, CustomCollection, GraphQL
import math
from urllib.parse import urlparse
import os

class ProductRepository(Repository):

    def get_products_by_status(self, status):
        try:
            count = Product.count(published_status= status)
            limit = 50
            total_page = math.ceil(count / limit)
            list_products = list()
            for page in range(total_page):
                product = Product.find(limit= limit, page= page + 1, published_status= status)
                list_products.extend(product)
            return list_products
        except:
            return None

    def get_products(self):
        try:
            product = Product()
            return product.find()
        except:
            return None
        

    def get_product(self, id):
        try:
            product = Product()
            return product.find(id_ = id)
        except:
            return None
        

    def save_update_product(self, data):
        try:
            product = Product(data)
            product.save()
            return product
        except Exception as ex:
            return None

    def update_price(self, data):
        variant = Variant(data)
        return variant.save()

    def delete_product(self, id):
        try:
            product = Product()
            product = product.find(id_= id)
            product.destroy()
            return product
        except:
            return None

    def create_new_image(self, product_id, data):
        try:
            image = Image(data)
            image.save()
            return image
        except Exception as ex:
            raise ex

    def upload_product_image(self, product_id, image_id, filename, attachment, position):
        try:
            filename = urlparse(filename)
            filename = os.path.basename(filename.path)
            image = Image()
            if image_id is not None:
                image.id = image_id
            if position is not None:
                image.position = position
            image.product_id=product_id
            image.attachment = attachment.decode()
            image.filename = filename
            image.save()
            return image
        except Exception as ex:
            raise ex

    def delete_image(self, image_id, product_id):
        try:
            image = Image()
            image = image.find(id_= image_id, product_id= product_id)
            image.destroy()
            return image
        except Exception as ex:
            return None

    def append_image_to_product(self, id, images):
        try:
            imgs = [{"altText": m['alt'], "src": m['src']} for m in images]
            response = GraphQL().execute('mutation productAppendImages($input: ProductAppendImagesInput!) {\
                                   productAppendImages(input: $input) {\
                                     newImages {\
                                       id\
                                       altText\
                                     }\
                                     product {\
                                       id\
                                     }\
                                     userErrors {\
                                       field\
                                       message\
                                     }\
                                   }\
                                 }',
                                variables={
                                  "input": {
                                    "id": "gid://shopify/Product/%d"%id,
                                    "images": imgs
                                  }
                                },
                              operation_name='productAppendImages')
            if response is not None:
                pass
        except Exception as ex:
            return None


    def add_product_to_collection(self, collection_id, product_id):
        try:
            collect = Collect()
            collect.collection_id = collection_id
            collect.product_id= product_id
            collect.save()
            return collect
        except Exception as ex:
            return None

    def remove_collection_from_product(self, collection_id, product_id):
        try:
            GraphQL().execute('mutation collectionRemoveProducts($id: ID!, $productIds: [ID!]!) {\
                                   collectionRemoveProducts(id: $id, productIds: $productIds) {\
                                     job {\
                                         done\
                                         id\
                                     }\
                                     userErrors {\
                                       field\
                                       message\
                                     }\
                                   }\
                                 }', 
                              variables={
                                  "id": "gid://shopify/Collection/%d" %collection_id,
                                  "productIds": [
                                    "gid://shopify/Product/%d" %product_id
                                  ]
                               },
                              operation_name='collectionRemoveProducts')
            return 0
        except Exception as ex:
            raise ex
        
    def publish_schedule_product(self, publish_id, product_id, publish_at):
        try:
            GraphQL().execute('mutation publishablePublish($id: ID!, $input: [PublicationInput!]!) {\
                                   publishablePublish(id: $id, input: $input) {\
                                     publishable {\
                                       availablePublicationsCount {\
                                         count\
                                       }\
                                       resourcePublicationsCount {\
                                         count\
                                       }\
                                     }\
                                     shop {\
                                       publicationCount\
                                     }\
                                     userErrors {\
                                       field\
                                       message\
                                     }\
                                   }\
                                 }', 
                              variables={
                                  "id": "gid://shopify/Product/%d" %product_id,
                                  "input": [{
                                    "publicationId": "gid://shopify/Publication/%d" %publish_id,
                                    "publishDate": publish_at
                                  }]
                               },
                              operation_name='publishablePublish')
            return 0
        except Exception as ex:
            raise ex

    def unpublish_schedule_product(self, publish_id, product_id, publish_at):
        try:
            GraphQL().execute('mutation publishableUnpublish($id: ID!, $input: [PublicationInput!]!) {\
                                   publishablePublish(id: $id, input: $input) {\
                                     publishable {\
                                       availablePublicationsCount {\
                                         count\
                                       }\
                                       resourcePublicationsCount {\
                                         count\
                                       }\
                                     }\
                                     shop {\
                                       publicationCount\
                                     }\
                                     userErrors {\
                                       field\
                                       message\
                                     }\
                                   }\
                                 }',
                              variables={
                                  "id": "gid://shopify/Product/%d" %product_id,
                                  "input": [{
                                    "publicationId": "gid://shopify/Publication/%d" %publish_id,
                                    "publishDate": publish_at
                                  }]
                               },
                              operation_name='publishableUnpublish')
            return 0
        except Exception as ex:
            raise ex

