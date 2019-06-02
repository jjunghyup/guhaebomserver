from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.service import entity

api = Namespace('entity', description='Intent related operations')

model = api.model("entity", {
    "entity": fields.List(fields.String, description="entity", required=False),
})


@api.route('/<intent_id>')
@api.param('intent_id', 'The entity  identifier')
@api.response(404, 'entity not found')
class Intent(Resource):
    @api.doc('get_entity')
    def get(self, intent_id):
        '''Fetch a intent given its identifier'''
        return jsonify(entity.get_one({'intent': intent_id}, {'_id': False}))

    @api.expect(model)
    @api.doc('insert_entity')
    def post(self, intent_id):
        '''Fetch a intent given its identifier'''
        json_data = request.json
        entity.insert_one({'intent': intent_id, 'entity': json_data['entity']})
        return jsonify({"result": "ok"})

    @api.expect(model)
    @api.doc('update_entity')
    def put(self, intent_id):
        '''Fetch a intent given its identifier'''
        json_data = request.json
        entity.update_one({'intent': intent_id, 'entity': json_data['entity']})
        return jsonify({"result": "ok"})

    @api.doc('delete_entity')
    def delete(self, intent_id):
        '''Fetch a intent given its identifier'''
        entity.delete_one({'intent': intent_id})
        return jsonify({"result": "ok"})

