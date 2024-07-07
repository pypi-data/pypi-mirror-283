from flask import jsonify, request
from ShopifyTupperware.bloc.waranty_bloc import WarantyBloc
from ShopifyTupperware.models.waranty_model import LimitedWarantySchema
from ShopifyTupperware import app, jwt
import json

class WarantyController:

    @app.route('/waranty', methods= ['POST'])
    def postWaranty():
        try:
            form = request.form
            form_string = form['rawRequest']
            #print(form_string)
            data_json = json.loads(form_string)
            schema = LimitedWarantySchema()
            model = schema.dump(data_json)
            if not model:
                return jsonify(Status = "Not Found", Code = 404), 404
            response = WarantyBloc.add_limited_waranty(model)
            if(response == -1):
                return jsonify(Status = "Internal Server Error", Code = 500), 500
            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500



    #@app.route('/claim-waranty', methods= ['POST'])
    #def postClaimWaranty():
    #    try:
    #        form = request.form
    #        files = request.files
    #        data= json.loads(form['rawData'])
    #        results:dict = []
    #        for item in data:
    #            results.append({item['name'] : item['value']})

    #        now= datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    #        file_name_1= now
    #        file_name_2 = now
    #        if 'file1' in files: # image product
    #            file= files['file1']
    #            file_name_1 = file_name_1 + file.filename
    #            file.save(os.path.join(app.config['BASE_DIR'], app.config['UPLOAD_FOLDER'], file_name_1))
    #        if 'file2' in files: #image slip payment
    #            file= files['file2']
    #            file_name_2 = file_name_2 + file.filename
    #            file.save(os.path.join(app.config['BASE_DIR'], app.config['UPLOAD_FOLDER'], file_name_2))

    #        results.append({'photoProduct': app.config['UPLOAD_FOLDER'] + file_name_1})
    #        results.append({'photoSlip': app.config['UPLOAD_FOLDER'] + file_name_2})
    #        res= NewWarantyBloc.add_new_waranty(results)
    #        if res == -1:
    #            return jsonify(Status = "Bad Request", Code = 500), 500
    #        return jsonify(Status = "OK", Data= results, Code = 200), 200
    #    except Exception as ex:
    #        return jsonify(Status= "", Code= 500, Desc=ex.args), 500