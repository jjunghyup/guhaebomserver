from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.util.job_category_predict import predict_job_category

api = Namespace('predict', description='predict related operations')

job_category_model = api.model("Insert_user_data", {
     "query":
         fields.String(description="Query ex)<keyword1>,<keyword2>,<keyword3>", required=True),
     # "item_count":
     #     fields.Integer(description="Show Recommend Item Count ex) 10", required=False)
})


@api.route('/predictJobCategory')
class PredictJobCategory(Resource):

    @api.expect(job_category_model)
    @api.doc('predict_job_categories')
    def post(self):
        '''List all job categories'''
        json_data = request.json
        # result = predict_job_category(json_data['query'], json_data['item_count'])
        result = predict_job_category(json_data['query'])
        return jsonify(result)

