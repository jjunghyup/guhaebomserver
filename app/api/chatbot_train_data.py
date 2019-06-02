from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.service import chatbot_train_data

api = Namespace('chatbotTrainData', description='Intent related operations')

model = api.model("chatbotTrainData", {
    "text": fields.String(description="Message", required=True),
    "intent": fields.String(description="Intent", required=True),
    "morphs": fields.List(fields.String, description="Morphs", required=True),
    "entity" : fields.List(fields.String, description="Entity", required=True),
})

upload_parser = api.parser()
upload_parser.add_argument('text', required=True, help='full text')

@api.route('/')
@api.response(404, 'entity not found')
class Intent(Resource):
    @api.expect(upload_parser)
    @api.doc('get_entity')
    def get(self):
        '''Fetch a intent given its identifier'''

        return jsonify(chatbot_train_data.get_one({'text': request.args['text']}, {'_id': False}))

    @api.expect(model)
    @api.doc('insert_entity')
    def post(self):
        '''Fetch a intent given its identifier'''
        json_data = request.json
        chatbot_train_data.insert_one(request.json)
        return jsonify({"result": "ok"})

    @api.expect(model)
    @api.doc('update_entity')
    def put(self):
        '''Fetch a intent given its identifier'''
        json_data = request.json
        chatbot_train_data.update_one(request.json)
        return jsonify({"result": "ok"})

    @api.doc('delete_entity')
    def delete(self):
        '''Fetch a intent given its identifier'''
        chatbot_train_data.delete_one(request.json)
        return jsonify({"result": "ok"})

