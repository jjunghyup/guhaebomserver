import pymongo

conn = pymongo.MongoClient('ip', 27017, username='chacha', password='test!@34')


def get_database(database):
    return conn.get_database(database)


def get_collection(database, collection):
    return conn.get_database(database).get_collection(collection)
