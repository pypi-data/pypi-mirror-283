from ShopifyTupperware.data import db

class ProductClaimDb:

    def __init__(self):
        self.engine = db.engine

    def getProductSeries(self):
        conn = self.engine.raw_connection()
        cursor = conn.cursor()
        try:
             cursor.execute('exec getProductSeries')
             results = cursor.fetchall()
             items = [dict(zip([key[0] for key in cursor.description], row)) for row in results]
             return items
        except :
            pass
        finally:
            cursor.close()
            conn.close()
    def getProductCollection(self, id):
        conn = self.engine.raw_connection()
        cursor = conn.cursor()
        try:
             cursor.execute('exec getProductCollection ?', [id])
             results = cursor.fetchall()
             items = [dict(zip([key[0] for key in cursor.description], row)) for row in results]
             return items
        except :
            pass
        finally:
            cursor.close()
            conn.close()

    def getProductParts(self, id):
        conn = self.engine.raw_connection()
        cursor = conn.cursor()
        try:
             cursor.execute('exec getProductParts ?', [id])
             results = cursor.fetchall()
             items = [dict(zip([key[0] for key in cursor.description], row)) for row in results]
             return items
        except :
            pass
        finally:
            cursor.close()
            conn.close()



