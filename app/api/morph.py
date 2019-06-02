from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.util.lexical_analyze import morphs, error_keyword_fix

api = Namespace('morph', description='morph related operations')

model = api.model("morph", {
    "query": fields.String(description="query string", required=True),
})


@api.route('/')
class Intent(Resource):

    @api.expect(model)
    @api.doc('morph analyze')
    def post(self):
        '''Fetch a intent given its identifier'''
        json_data = request.json
        query = error_keyword_fix(json_data['query'])
        return jsonify(morphs(query))

