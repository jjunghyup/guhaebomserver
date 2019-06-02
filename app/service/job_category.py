from app.service import get_collection

job_category = get_collection('guhaebom', 'job_category')


def insert(data):
    job_category.insert(data)


def find(*args, **kwargs):
    return job_category.find(*args, **kwargs)


def find_one(*args, **kwargs):
    return job_category.find_one(*args, **kwargs)


def update(key, query, upsert=True, multiline=False):
    return job_category.update(key, query, upsert, multiline)


def remove(query):
    return job_category.remove(query)

