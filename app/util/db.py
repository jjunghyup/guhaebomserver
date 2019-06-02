from pymongo import MongoClient
mongo = MongoClient('localhost', 27017, username='chacha', password='test!@34')


def get_intent_test_data():
    td = mongo.guhaebom.chatbotdata
    output = {}
    encode = []
    decode = []

    for s in td.find():
        encode.append(s['text'])
        decode.append(s['intent'])

    output['encode'] = encode
    output['decode'] = decode

    print(encode)
    print(decode)
    return output


def get_intent_data():
    td = mongo.guhaebom.intent
    output = {}

    for s in td.find():
        output[s['id']] = s['name']

    return output


def get_entity_test_data(intent):
    td = mongo.guhaebom.chatbotdata
    encode = []
    decode = []

    for s in td.find():
        if s['intent'] == intent:
            encode.append(s['morphs'])
            decode.append(s['entity'])
    print(encode)
    print(decode)
    return encode, decode




# def get_one(query):
#     usr = mongo.db.user
#     data = usr.find_one(query)
#     return data
#
# def insert_one(data):
#     usr = mongo.chatbot.user
#     return usr.insert_one(data)
#
#
# def delete_one(data):
#     usr = mongo.chatbot.user
#     return usr.delete_one({'user_id': data['user_id']})
#
# def update_one(data):
#     usr = mongo.chatbot.user
#     delete_one(data)
#     insert_one(data)
#
# if __name__ == '__main__':
#     id = 'idid'
#     print(id)
#     print(get_one({'user_id': 'sw.hyeon'})['user_id'])
#
