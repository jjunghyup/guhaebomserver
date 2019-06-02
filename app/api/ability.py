from flask import jsonify
from flask_restplus import Namespace, Resource
from app.service import ability

api = Namespace('ability', description='Ability related operations')


@api.route('/')
class AbilitiesList(Resource):
    @api.doc('list_ability')
    def get(self):
        '''List all abilities'''
        documents = [doc for doc in ability.find({}, {'_id': False})]
        return jsonify(documents)


@api.route('/<id>')
@api.param('id', 'The ability  identifier')
@api.response(404, 'ability not found')
class Ability(Resource):
    @api.doc('get_ability')
    def get(self, id):
        '''Fetch a ability given its identifier'''
        return ability.find_one({'id': id}, {'_id': False})
