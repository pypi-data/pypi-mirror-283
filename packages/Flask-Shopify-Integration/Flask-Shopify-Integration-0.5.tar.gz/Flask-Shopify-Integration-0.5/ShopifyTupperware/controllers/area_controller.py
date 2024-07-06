from flask import jsonify, request
from ShopifyTupperware import app, jwt
import json
from ShopifyTupperware.data.area_db import AreaDb

class AreaController:
    
    @app.route('/provinsi', methods= ['POST'])
    def get_provinsi():
        area_db = AreaDb()
        models= area_db.get_provinsi()
        return jsonify(models), 200

    @app.route('/kabupaten', methods= ['POST'])
    def get_kabupaten():
        data = request.get_json()
        if not('code' in data):
            return jsonify(Status= "Bad Request", Code= 400), 400
        code = data['code']
        area_db = AreaDb()
        models= area_db.get_city(code)
        return jsonify(models), 200



    @app.route('/kecamatan', methods= ['POST'])
    def get_kecamatan():
        data = request.get_json()
        if not('code' in data):
            return jsonify(Status= "Bad Request", Code= 400), 400
        code = data['code']
        area_db = AreaDb()
        models= area_db.get_kecamatan(code)
        return jsonify(models), 200

    @app.route('/kelurahan', methods= ['POST'])
    def get_kelurahan():
        data = request.get_json()
        if not('code' in data):
            return jsonify(Status= "Bad Request", Code= 400), 400
        code = data['code']
        area_db = AreaDb()
        models= area_db.get_kelurahan(code)
        return jsonify(models), 200





