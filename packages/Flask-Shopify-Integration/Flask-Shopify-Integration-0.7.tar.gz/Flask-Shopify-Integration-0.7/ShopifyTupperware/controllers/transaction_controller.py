from flask import jsonify, request
#from flask_jwt_simple import jwt_required
from flask_jwt_extended import jwt_required
from ShopifyTupperware import app
from ShopifyTupperware.repositories.transaction_repository import TransactionRepository
from ShopifyTupperware.models.transaction_model import TransactionSchema


class TransactionController:

    @app.route('/transaction/order/<int:id>')
    @jwt_required()
    def get_transaction(id):
        schema = TransactionSchema(many= True)
        repository = TransactionRepository()
        response = repository.get_transactions(id)
        results = schema.dump(response)
        return jsonify(results), 200

