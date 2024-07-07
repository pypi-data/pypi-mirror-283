from ShopifyTupperware.data import db


class AreaDb():

    def __init__(self):
        self.engine = db.engine

    def get_provinsi(self):
        conn = self.engine.raw_connection()
        cursor = conn.cursor()
        try:
             cursor.execute('exec getProvinsi')
             results = cursor.fetchall()
             items = [dict(zip([key[0] for key in cursor.description], row)) for row in results]
             return items
        except :
            pass
        finally:
            cursor.close()
            conn.close()

    def get_city(self, code):
        conn = self.engine.raw_connection()
        cursor = conn.cursor()
        try:
             cursor.execute('exec getCity ?', [code])
             results = cursor.fetchall()
             items = [dict(zip([key[0] for key in cursor.description], row)) for row in results]
             return items
        except :
            pass
        finally:
            cursor.close()
            conn.close()

    def get_kecamatan(self, code):
        conn = self.engine.raw_connection()
        cursor = conn.cursor()
        try:
             cursor.execute('exec getKecamatan ?', [code])
             results = cursor.fetchall()
             items = [dict(zip([key[0] for key in cursor.description], row)) for row in results]
             return items
        except :
            pass
        finally:
            cursor.close()
            conn.close()

    def get_kelurahan(self, code):
        conn = self.engine.raw_connection()
        cursor = conn.cursor()
        try:
             cursor.execute('exec getKelurahan ?', [code])
             results = cursor.fetchall()
             items = [dict(zip([key[0] for key in cursor.description], row)) for row in results]
             return items
        except :
            pass
        finally:
            cursor.close()
            conn.close()
