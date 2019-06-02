from app.service import get_collection

intent = get_collection('guhaebom', 'intent')


def get_all_intents():
    return [doc for doc in intent.find({}, {'_id': False})]


def get_one(*args, **kwargs):
    data = intent.find_one(*args, **kwargs)
    return data


def insert_one(data):
    return intent.insert_one(data)


def delete_one(data):
    return intent.delete_one({'id': data['id']})


def update_one(data):
    delete_one(data)
    insert_one(data)
