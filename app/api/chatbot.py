from flask import jsonify, request
from flask_restplus import Namespace, Resource
from flask_restplus import fields
from app.model.message import Message
from app.service.chatbot import ChatbotEngine
engine = ChatbotEngine()

api = Namespace('chatbot', description='predict related chatbot')

model = api.model("chatbot", {
    "message": fields.String(description="Chat Message to Chatbot", required=True),
    "sender": fields.String(description="Sender ID", required=True),
})


@api.route('/process')
class ChatbotProcess(Resource):

    @api.expect(model)
    @api.doc('predict_job_categories')
    def post(self):
        json_data = request.json
        result = engine.process(Message(json_data['sender'],json_data['message']))
        return jsonify(result)


