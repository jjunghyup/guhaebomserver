from app.service import get_collection

ability = get_collection('guhaebom', 'ability')


def insert(data):
    ability.insert(data)


def find(*args, **kwargs):
    return ability.find(*args, **kwargs)


def find_one(*args, **kwargs):
    return ability.find_one(*args, **kwargs)


def update(key, query, upsert=True, multiline=False):
    return ability.update(key, query, upsert, multiline)


def remove(query):
    return ability.remove(query)

