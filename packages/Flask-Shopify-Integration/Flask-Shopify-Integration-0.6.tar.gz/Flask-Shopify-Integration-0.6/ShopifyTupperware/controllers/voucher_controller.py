from flask import jsonify, request, render_template
from ShopifyTupperware import app, jwt
import json
from datetime import datetime

class VoucherController:

    @app.route("/my-voucher")
    def voucher_index():
        try:
            return render_template(
                'voucher.html',
                title='Voucher Page',
                year=datetime.now().year,
            )
        except Exception as ex:
            raise ex

    @app.route('/add-voucher', methods= ['POST'])
    def add_voucher():
        try:
            data = request.get_json()
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

