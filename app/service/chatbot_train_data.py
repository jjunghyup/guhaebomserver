from app.service import get_collection

chatbotdata = get_collection('guhaebom', 'chatbotdata')


def get_all_names():
    output = []
    for s in chatbotdata.find():
        output.append({'text': s['text']})
    return output


def get_one(*args, **kwargs):
    data = chatbotdata.find_one(*args, **kwargs)
    return data


def insert_one(data):
    return chatbotdata.insert_one(data)


def delete_one(data):
    return chatbotdata.delete_one({'text': data['text']})


def update_one(data):
    delete_one(data)
    insert_one(data)

