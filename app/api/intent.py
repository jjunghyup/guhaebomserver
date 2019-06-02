from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.service import intent

api = Namespace('intent', description='Intent related operations')

model = api.model("intent", {
    "name": fields.String(description="intent name", required=True),
})


@api.route('/')
class IntentList(Resource):
    @api.doc('list_intents')
    def get(self):
        '''List all abilities'''
        return jsonify(intent.get_all_intents())


@api.route('/<id>')
@api.param('id', 'The intent  identifier')
@api.response(404, 'intent not found')
class Intent(Resource):
    @api.doc('get_intent')
    def get(self, id):
        '''Fetch a intent given its identifier'''
        return intent.get_one({'id': id}, {'_id': False})

    @api.expect(model)
    @api.doc('insert_intent')
    def post(self, id):
        '''Fetch a intent given its identifier'''
        json_data = request.json
        intent.insert_one({'id': id, 'name': json_data['name']})
        return jsonify({"result": "ok"})

    @api.expect(model)
    @api.doc('update_intent')
    def put(self, id):
        '''Fetch a intent given its identifier'''
        json_data = request.json
        intent.update_one({'id': id, 'name': json_data['name']})
        return jsonify({"result": "ok"})

    @api.doc('insert_intent')
    def delete(self, id):
        '''Fetch a intent given its identifier'''
        intent.delete_one({'id': id})
        return jsonify({"result": "ok"})


