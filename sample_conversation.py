import pyrebase
import time

config = {
  "apiKey": "apiKey",
  "authDomain": "guhaebom.firebaseapp.com",
  "databaseURL": "https://guhaebom.firebaseio.com",
  "storageBucket": "guhaebom.appspot.com",
  "serviceAccount": "guhaebom-firebase-admin.json",
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Get a reference to the database service
db = firebase.database()

def job_send_message(message):
    print("job input message : %s" % message)
    now = time.localtime()
    s = "%02d:%02d" % (now.tm_hour, now.tm_min)
    data = {
        "isYou": "true",
        "timestamp": s,
        "type": "1",
        "sender": "알바왕",
        "message":  message
    }
    db.child("job").push(data)
    time.sleep(2)

def worker_send_message(message):
    print("worker input message : %s" % message)
    now = time.localtime()
    s = "%02d:%02d" % (now.tm_hour, now.tm_min)
    data = {
        "isYou": "true",
        "timestamp": s,
        "type": "1",
        "sender": "카페꿈나무",
        "message":  message
    }
    db.child("worker").push(data)
    time.sleep(2)

def get_chatbot_last_message(collection):
    outputs = db.child(collection).get()
    message = outputs.pyres[len(outputs.pyres)-1].val()['message']
    print("%s output message : %s" % (collection, message))
    return message

# worker 시나리오
worker_send_message("newcat")
get_chatbot_last_message("worker")
worker_send_message("긴급하게 알바 구할 수 있을까?")
get_chatbot_last_message("worker")
worker_send_message("2019-06-21 ~ 2019-06-25")
get_chatbot_last_message("worker")
worker_send_message("응")
get_chatbot_last_message("worker")
worker_send_message("커피 제조, 서빙, 주방 보조")
get_chatbot_last_message("worker")

# job 시나리오
job_send_message("newcat")
get_chatbot_last_message("job")
job_send_message("카페 일자리 구해줘")
get_chatbot_last_message("job")
job_send_message("2019-06-21 ~ 2019-06-25")
get_chatbot_last_message("job")
job_send_message("응")
get_chatbot_last_message("job")
job_send_message("'업무' 신청할게")
get_chatbot_last_message("job")
get_chatbot_last_message("worker")

# worker 신청 수락
worker_send_message("'사람이름' 선택할게")
get_chatbot_last_message("worker")
get_chatbot_last_message("job")
