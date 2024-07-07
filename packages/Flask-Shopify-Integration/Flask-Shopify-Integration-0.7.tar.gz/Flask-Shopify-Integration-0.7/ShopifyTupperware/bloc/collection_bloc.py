from ShopifyTupperware.data.collection_db import CollectionDb
from ShopifyTupperware import helper

class CollectionBloc:

    @staticmethod
    def get_collection_list():
        return CollectionDb.get_collections()

    @staticmethod
    def add_new_bloc(model):
        if CollectionDb.collection_exists(model['id']) is not None:
            return CollectionBloc.update_collection(model)
        new_collection = CollectionDb()
        for key, value in model.items():
            if hasattr(new_collection, key) & (helper.is_dictionary(model[key]) != True):
                setattr(new_collection, key, value)
                pass
            pass
        return CollectionDb.create_or_update(new_collection)

    @staticmethod
    def update_collection(model):
        image_src = ''
        image = model['image'] if 'image' in model and model['image'] is not None else None
        if image is not None:
            image_src = image['src'] if 'src' in image and image['src'] is not None else None
        return CollectionDb.update_collection(model['id'], model['title'], image_src, model['body_html'], True, model['handle'])



