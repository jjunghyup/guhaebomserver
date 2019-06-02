from app.service import get_collection

conversation = get_collection('guhaebom', 'conversation')


def get_one(query):
    data = conversation.find_one(query)
    return data


def insert_one(data):
    return conversation.insert_one(data)


def delete_one(data):
    return conversation.delete_one({'sender': data['sender']})


def update_one(data):
    if '_id' in data:
        data.pop('_id')
    conversation.update_one({'sender': data['sender']}, {"$set": data}, upsert=False)
