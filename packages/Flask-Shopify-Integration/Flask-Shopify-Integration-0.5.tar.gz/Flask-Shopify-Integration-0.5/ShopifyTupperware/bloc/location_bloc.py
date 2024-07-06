from ShopifyTupperware.data.inventory_db import LocationDb
from ShopifyTupperware import helper

class LocationBloc:


    @staticmethod
    def create_location(data):
        location_db = LocationDb()
        for key, value in data.items():
            if hasattr(location_db, key) & (helper.is_dictionary(data[key]) != True):
                setattr(location_db, key, value)
        return LocationDb.create_location(location_db)


    @staticmethod
    def update_location(data):
        if LocationDb.location_exists(data['id']):
            return LocationDb.update_location_by_id(data['id'], data['name'], data['address1'])
        location_db = LocationDb()
        for key, value in data.items():
            if hasattr(location_db, key) & (helper.is_dictionary(data[key]) != True):
                setattr(location_db, key, value)
        return LocationDb.create_location(location_db)
