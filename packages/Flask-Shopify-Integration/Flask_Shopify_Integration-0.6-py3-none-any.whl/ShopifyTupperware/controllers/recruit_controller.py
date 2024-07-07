from flask import jsonify, request
#from ShopifyTupperware.bloc.new_recruit_bloc import NewRecruitBloc
from ShopifyTupperware.bloc.recruit_bloc import RecruitBloc
from ShopifyTupperware.models.recruit_model import RecruitSchema
from ShopifyTupperware import app, jwt
#from logging.config import dictConfig
import json
import os
import datetime

class RecruitController:

    @app.route('/recruits', methods= ['POST'])
    def recruit():
        try:
            form = request.form
            form_string = form['rawRequest']
            #print(form_string)
            #app.logger.info(form_string)
            data_json = json.loads(form_string)
            schema = RecruitSchema()
            model = schema.dump(data_json)
            if not model:
                return jsonify(Status = "Not Found", Code = 404), 404

            res = RecruitBloc.add_recruit(model)
            if res == -1:
                return jsonify(Status = "Internal Server Error", Code = 500), 500

            return jsonify(Status = "OK", Code = 200), 200
        except Exception as ex:
            return jsonify(Status = "Internal Server Error", Code = 500, Desc = ex.args), 500

    #@app.route('/recruits2', methods= ['POST'])
    #@app.route('/register-salesforce', methods= ['POST'])
    #def postRecruit2():
    #    try:
    #        form = request.form
    #        files = request.files
    #        data= json.loads(form['rawData'])
    #        results:dict = []
    #        noKtp= ""
    #        for item in data:
    #            if item['name'] == 'noKtp':
    #                noKtp=item['value']
    #            results.append({item['name'] : item['value']})

    #        now= datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    #        file_name= noKtp + now + '.png'
    #        if 'file' in files:
    #            file= files['file']
    #            file.save(os.path.join(app.config['BASE_DIR'], app.config['UPLOAD_FOLDER'], file_name))

    #        results.append({'photoKtp': app.config['UPLOAD_FOLDER'] + file_name})
    #        res= NewRecruitBloc.add_new_recruit(results)
    #        if res == -1:
    #            return jsonify(Status = "Bad Request", Code = 500), 500
    #        return jsonify(Status = "OK", Data= results, Code = 200), 200
    #    except Exception as ex:
    #        return jsonify(Status= "", Code= 500, Desc=ex.args), 500

    