from ShopifyTupperware.repositories.repository import Repository
from shopify import InventoryItem, InventoryLevel, Location

class InventoryRepository(Repository):

    def get_locations(self):
        try:
            location = Location()
            return location.find()
        except:
            return None
       

    def get_location(self, id):
        try:
            location = Location()
            return location.find(id_= id)
        except:
            return None

    def save_location(self, data):
        try:
            location = Location(data)
            location.save()
            return location
        except:
            return None
        

    def get_inventory_level_location(self, id):
        try:
            location = Location()
            response = location.find(id_= id)
            if not response:
                return None
            return response.inventory_levels()
        except:
            return None
       

    def get_inventory_items(self, ids):
        try:
            inventory_item = InventoryItem()
            return inventory_item.find(id_= None, from_= None, ids= ids)
        except:
            return None

        

    def get_inventory_item(self, id):
        try:
            inventory_item = InventoryItem()
            return inventory_item.find(id_= id)
        except:
            return None
       

    def update_inventory_item(self, id, sku):
        try:
            inventory_item = InventoryItem()
            inventory_item.id = id
            inventory_item.sku = sku
            return inventory_item.save()
        except:
            return None
        


    def get_inventory_level(self, inventory_item_id, location_id):
        try:
            inventory_level = InventoryLevel()
            return inventory_level.find(id_= None, from_= None, inventory_item_ids= inventory_item_id, location_ids= location_id)
        except:
            return None
       
    
    def connect_inventory_level(self, location_id, inventory_item_id):
        try:
            inventory_level = InventoryLevel()
            return inventory_level.connect(location_id= location_id, inventory_item_id= inventory_item_id)
        except:
            return None

        

    def adjust_inventory_level(self, location_id, inventory_item_id, available):
        try:
            inventory_level = InventoryLevel()
            return inventory_level.adjust(location_id= location_id, inventory_item_id= inventory_item_id, available_adjustment= available)
        except:
            return None
        

    def set_inventory_level(self, location_id, inventory_item_id, available):
        try:
            inventory_level = InventoryLevel()
            return inventory_level.set(location_id= location_id, inventory_item_id=inventory_item_id, available= available)
        except:
            return None
        


