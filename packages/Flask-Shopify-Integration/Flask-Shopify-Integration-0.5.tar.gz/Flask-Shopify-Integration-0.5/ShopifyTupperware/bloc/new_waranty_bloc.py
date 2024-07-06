from ShopifyTupperware import helper
from ShopifyTupperware.data.new_waranty_db import NewWarantyDb,NewWarantyAttachDb
import datetime

class NewWarantyBloc:

    @staticmethod
    def add_new_waranty(model: dict):
        try:
            new_model= NewWarantyDb()
            for data in model:
                for key, value in data.items():
                    if hasattr(new_model, key) & (helper.is_dictionary(data[key]) != True):
                        setattr(new_model, key, value)
                        pass
                    pass
                if 'photoProduct' in data:
                    photo1 = NewWarantyAttachDb()
                    photo1.image_url= data['photoProduct']
                    new_model.attachments.append(photo1)
                    pass
                if 'photoSlip' in data:
                    photo2 = NewWarantyAttachDb()
                    photo2.image_url= data['photoSlip']
                    new_model.attachments.append(photo2)
                    pass
                pass
            new_model.created_by = new_model.email
            new_model.created_at = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            NewWarantyDb.create_or_update(new_model)
            return 1
        except Exception as ex:
            return -1


