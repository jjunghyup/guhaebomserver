from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.service import account

api = Namespace('account', description='account related operations')

company = api.model('Company', {
    'name': fields.String,
    'category': fields.String
})

career = api.model('Career', {
    'category': fields.String,
    'experience': fields.String,
    'reputation': fields.String
})

model = api.model("account", {
    "name": fields.String(description="account name", required=True),
    "sex": fields.String(description="sex", required=True),
    "desiredSalary": fields.String(description="desiredSalary", required=True),
    "birthDate": fields.String(description="birthDate", required=True),
    "Location": fields.String(description="Location", required=True),
    "company": fields.Nested(company, description="company info", required=False),
    "career": fields.List(fields.Nested(career), description="career info", required=False),
})


@api.route('/')
class AccountList(Resource):
    @api.doc('list_accounts')
    def get(self):
        '''List all abilities'''
        return jsonify(account.get_all_accounts())


@api.route('/<id>')
@api.param('id', 'The account  identifier')
@api.response(404, 'account not found')
class Account(Resource):
    @api.doc('get_account')
    def get(self, id):
        '''Fetch a account given its identifier'''
        return account.get_one({'id': id}, {'_id': False})

    @api.expect(model)
    @api.doc('insert_account')
    def post(self, id):
        '''Fetch a account given its identifier'''
        json_data = request.json
        json_data['id'] = id
        account.insert_one(json_data)
        return jsonify({"result": "ok"})

    @api.expect(model)
    @api.doc('update_account')
    def put(self, id):
        '''Fetch a account given its identifier'''
        json_data = request.json
        json_data['id'] = id
        account.insert_one(json_data)
        return jsonify({"result": "ok"})

    @api.doc('insert_account')
    def delete(self, id):
        '''Fetch a account given its identifier'''
        account.delete_one({'id': id})
        return jsonify({"result": "ok"})
