from app.service import get_collection

account = get_collection('guhaebom', 'account')


def get_all_accounts():
    return account.find({'_id': False})


def get_one(*args, **kwargs):
    data = account.find_one(*args, **kwargs)
    return data


def insert_one(data):
    return account.insert_one(data)


def delete_one(data):
    return account.delete_one({'id': data['id']})


def update_one(data):
    delete_one(data)
    insert_one(data)
