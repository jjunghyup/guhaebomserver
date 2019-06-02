from flask_restplus import Api
from .ability import api as ability_api
from .account import api as account_api
from .chatbot import api as chatbot_api
from .conversation import api as conversation_api
from .job_category import api as job_api
from .predict import api as predict_api
from .intent import api as intent_api
from .entity import api as entity_api
from .morph import api as morphs_api
from .chatbot_train_data import api as chatbot_train_data_api

api = Api(
    title='Guhaebom API',
    version='1.0',
    description='A Guhaebom API',
)

api.add_namespace(ability_api)
api.add_namespace(account_api)
api.add_namespace(chatbot_api)
api.add_namespace(conversation_api)
api.add_namespace(job_api)
api.add_namespace(predict_api)
api.add_namespace(intent_api)
api.add_namespace(entity_api)
api.add_namespace(morphs_api)
api.add_namespace(chatbot_train_data_api)


