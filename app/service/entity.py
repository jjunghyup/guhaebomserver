from app.service import get_collection

entity = get_collection('guhaebom', 'entity')


def get_one(*args, **kwargs):
    data = entity.find_one(*args, **kwargs)
    return data


def insert_one(data):
    return entity.insert_one(data)


def delete_one(data):
    return entity.delete_one({'intent': data['intent']})


def update_one(data):
    delete_one(data)
    insert_one(data)
