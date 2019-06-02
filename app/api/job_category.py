from flask import jsonify
from flask_restplus import Namespace, Resource
from app.service import job_category

api = Namespace('jobCategories', description='Jobs related operations')


@api.route('/')
class JobCategoryList(Resource):
    @api.doc('list_job_categories')
    def get(self):
        '''List all job categories'''
        documents = [doc for doc in job_category.find({}, {'_id': False})]
        return jsonify(documents)


@api.route('/<id>')
@api.param('id', 'The job category identifier')
@api.response(404, 'Job not found')
class JobCategory(Resource):
    @api.doc('get_job')
    def get(self, id):
        '''Fetch a job given its identifier'''
        return job_category.find_one({'id': id}, {'_id': False})
