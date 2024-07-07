from flask import jsonify, request
from ShopifyTupperware import app
from ShopifyTupperware.data.product_claim_db import ProductClaimDb
import json

class ProductClaimController:

    @app.route("/product-claim/series", methods= ['POST'])
    def getProductSeries():
        db = ProductClaimDb()
        models= db.getProductSeries()
        return jsonify(models), 200

    @app.route("/product-claim/collection", methods= ['POST'])
    def getProductCollection():
        data = request.get_json()
        if not('code' in data):
            return jsonify(Status= "Bad Request", Code= 400), 400
        code = data['code']
        db = ProductClaimDb()
        models= db.getProductCollection(code)
        return jsonify(models), 200

    @app.route("/product-claim/part", methods= ['POST'])
    def getProductParts():
        data = request.get_json()
        if not('code' in data):
            return jsonify(Status= "Bad Request", Code= 400), 400
        code = data['code']
        db = ProductClaimDb()
        models= db.getProductParts(code)
        return jsonify(models), 200



