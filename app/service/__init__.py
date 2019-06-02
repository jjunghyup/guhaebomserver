import pymongo

conn = pymongo.MongoClient('ip', 27017, username='id', password='pass')


def get_database(database):
    return conn.get_database(database)


def get_collection(database, collection):
    return conn.get_database(database).get_collection(collection)
