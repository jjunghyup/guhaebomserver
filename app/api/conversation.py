from flask import jsonify
from flask_restplus import Namespace, Resource
from app.service import conversation

api = Namespace('converstaion', description='Jobs related operations')


@api.route('/<id>')
@api.param('id', 'The job category identifier')
@api.response(404, 'Job not found')
class JobCategory(Resource):
    @api.doc('get_job')
    def delete(self, id):
        '''Fetch a job given its identifier'''
        conversation.delete_one({'sender':id})
        return jsonify({"result": "ok"})
