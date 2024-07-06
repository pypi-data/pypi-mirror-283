from ShopifyTupperware import helper
from ShopifyTupperware.data.new_recruit_db import NewRecruitDb

class NewRecruitBloc:

    @staticmethod
    def add_new_recruit(model: dict):
        try:
            new_recruit= NewRecruitDb()
            for data in model:
                for key, value in data.items():
                    if hasattr(new_recruit, key) & (helper.is_dictionary(data[key]) != True):
                        setattr(new_recruit, key, value)
            NewRecruitDb.create_or_update(new_recruit)
            return 1
        except Exception as ex:
            return -1