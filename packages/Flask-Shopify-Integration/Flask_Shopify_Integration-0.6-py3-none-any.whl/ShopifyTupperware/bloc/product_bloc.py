from ShopifyTupperware.data.product_db import ProductDb
from ShopifyTupperware import helper
from ShopifyTupperware.data.image_db import ImageDb
from ShopifyTupperware.data.variant_db import VariantDb
from ShopifyTupperware.data.inventory_db import LocationDb, InventoryLevelDb

class ProductBloc:

    @staticmethod
    def update_product(key, model):
        if model['variants'] is not None:
            variant = model['variants'][0]
            location = LocationDb.query.filter(LocationDb.actived == True and LocationDb.is_default == True).first()
            inventory_level= InventoryLevelDb()
            inventory_level.inventory_item_id= variant['inventory_item_id']
            inventory_level.location_id= location.id
            inventory_level.available= variant['inventory_quantity']
            inventory_level.status = 1
            inventory_level.is_sync = True
            InventoryLevelDb.add_or_update(inventory_level)
            VariantDb.update_inventory_item_id(product_key= key, product_id= model['id'], inventory_item_id= variant['inventory_item_id'], id= variant['id'])
            ProductDb.update_id(key= key, id= model['id'])
        return 0

    @staticmethod
    def create_or_update_product_image(key, model, images):
        try:
            location = LocationDb.query.filter(LocationDb.is_default == True and LocationDb.actived == True).first()

            if model['variants'] is not None:
                for variant in model['variants']:
                    inventory_level= InventoryLevelDb()
                    inventory_level.inventory_item_id= variant['inventory_item_id']
                    inventory_level.location_id= location.id
                    inventory_level.available= variant['inventory_quantity']
                    inventory_level.status = 1
                    inventory_level.is_sync = True
                    InventoryLevelDb.add_or_update(inventory_level)
                    VariantDb.update_inventory_item_id(product_key= key, product_id= model['id'], inventory_item_id= variant['inventory_item_id'], id= variant['id'])
                    ProductDb.update_id(key= key, id= model['id'])
                    pass
                pass
            if not images:
                return
            if model['images'] is not None:
                for image in model['images']:
                    for img in images:
                        if img['alt'] == image['alt']:
                            ImageDb.update_product_image_id(img['key'], image['id'], model['id'])
                    pass
                pass

        except Exception as ex:
            raise ex
        return 0

    @staticmethod
    def create_or_update_product(product):
        current_product = ProductDb.query.filter(ProductDb.id == model['id']).first()
        if not current_product:
            new_product = ProductDb()
            for key, value in product.items():
                if hasattr(new_product, key) & (helper.is_dictionary(product[key]) != True):
                    setattr(new_product, key, value)
                    pass
                pass
            pass
        pass


    @staticmethod
    def add_update_product_list(model):
        existing = ProductDb.query.filter(ProductDb.id == model['id']).first()
        if existing is not None:
            ProductBloc.add_update_product_images(model)
            return False
        #initial new product
        new_product = ProductDb()
        for key, value in model.items():
            if hasattr(new_product, key) & (helper.is_dictionary(model[key]) != True):
                setattr(new_product, key, value)
        #add variants of product
        if model['variants'] is not None:
            for variant in model['variants']:
                new_variant_db = VariantDb()
                for key, value in variant.items():
                    if hasattr(new_variant_db, key) & (helper.is_dictionary(variant[key]) != True):
                        setattr(new_variant_db, key, value)
                        pass
                    pass
                new_product.variants.append(new_variant_db)
                pass
            pass

        #add images of product
        if model['images'] is not None:
            for image in model['images']:
                new_image_db = ImageDb()
                for key, value in image.items():
                    if hasattr(new_image_db, key) & (helper.is_dictionary(image[key]) != True):
                        setattr(new_image_db, key, value)
                        pass
                    pass
                new_product.images.append(new_image_db)
                pass
            pass
        new_product.status = 3
        new_product = ProductDb.create_or_update(new_product)
        return new_product

    @staticmethod
    def add_product_inventory_level(model):
        if model['variants'] is not None:
            variants = model['variants']
            location = LocationDb.query.filter(LocationDb.actived == True and LocationDb.is_default == True).first()
            for variant in variants:
                inventory_level= InventoryLevelDb()
                inventory_level.inventory_item_id= variant['inventory_item_id']
                inventory_level.location_id= location.id
                inventory_level.available= variant['inventory_quantity']
                inventory_level.status = 1
                inventory_level.is_sync = True
                InventoryLevelDb.add_or_update(inventory_level)
        return 0


    @staticmethod
    def add_update_product_images(model):
        if model['images'] is not None:
            images = model['images']
            current_product = ProductDb.query.filter(ProductDb.id == model['id']).first()
            if not current_product:
                return None
            ProductDb.update_published(model['id'], model)
            current_images = ImageDb.query.filter(ImageDb.product_id == model['id']).delete()
            new_images = []
            for image in images:
                product_image = ImageDb()
                product_image.product_id = model['id']
                product_image.product_key = current_product.key
                product_image.id = image['id']
                product_image.src = image['src']
                product_image.alt = image['alt']
                product_image.width = image['width']
                product_image.height = image['height']
                new_images.append(product_image)
            return ImageDb.create_or_update(new_images)
        else:
            return None

    @staticmethod
    def add_update_product_with_images(product_key, product_id, images):
        new_images = []
        for image in images:
            product_image = ImageDb()
            product_image.product_id = product_id
            product_image.product_key = product_key
            product_image.id = image['id']
            product_image.src = image['src']
            product_image.alt = image['alt']
            product_image.width = image['width']
            product_image.height = image['height']
            new_images.append(product_image)
        return ImageDb.create_or_update(new_images)

    @staticmethod
    def update_image(image_key, image_id, product_id):
        return ImageDb.update_product_image_id(image_key, image_id, product_id)

