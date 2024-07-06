from ShopifyTupperware.data import order_db, customer_db, address_db, fulfillment_db
from ShopifyTupperware import helper
from ShopifyTupperware.data.line_item_db import LineItemDb
from ShopifyTupperware.data.discount_allocation_db import DiscountAllocationDb

class LineItemBloc:

   @staticmethod
   def add_discount_allocation(new_line_item, discount_allocations):
       for model in discount_allocations:
           db = DiscountAllocationDb()
           for key, value in model.items():
                if hasattr(db, key) & (helper.is_dictionary(model[key]) != True):
                    setattr(db, key, value)
           new_line_item.discount_allocations.append(db)

   @staticmethod
   def add(new_order, line_items):
       for line_item in line_items:
           new_line_item = LineItemDb()
           if 'discount_allocations' in line_item:
               if(line_item['discount_allocations'] is not None) and (len(line_item['discount_allocations']) > 0):
                   LineItemBloc.add_discount_allocation(new_line_item, line_item['discount_allocations'])
           for key, value in line_item.items():
                if hasattr(new_line_item, key) & (helper.is_dictionary(line_item[key]) != True):
                    setattr(new_line_item, key, value)
           new_line_item.order_id = new_order.id
           new_order.line_items.append(new_line_item)
       return new_order



