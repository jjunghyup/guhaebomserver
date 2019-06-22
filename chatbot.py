import pyrebase
from app.model.message import Message
from app.service.chatbot import ChatbotEngine
engine = ChatbotEngine()
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

# Log the user in
# user = auth.sign_in_with_email_and_password("firebase-adminsdk-eqwt2@guhaebom.iam.gserviceaccount.com", "tlfwkd5203!")

# Get a reference to the database service
db = firebase.database()


def ignore_first_call(fn):
    called = False

    def wrapper(*args, **kwargs):
        nonlocal called
        if called:
            return fn(*args, **kwargs)
        else:
            called = True
            return None

    return wrapper


@ignore_first_call
def job_stream_handler(message):
    print("-----------1 data--------------")
    print(message["data"])

    if message["data"] is None:
        return

    # isYou가 true인 경우에만 수행(사용자 인 경우)
    if message["data"]["isYou"] == "true":
        result, chat_type, add_process = engine.process(Message(message["data"]['sender'], message["data"]['message']))

        now = time.localtime()
        s = "%02d:%02d" % (now.tm_hour, now.tm_min)
        data = {
            "isYou": "false",
            "timestamp": s,
            "type": chat_type,
            "sender": "구해봇",
            "message": result
        }

        # Pass the user's idToken to the push method
        results = db.child("job").push(data)
        print("-----------push 결과--------------")
        print(results)

        if add_process:
            print("-----------worker에 확정메시지전달--------------")
            data = {
                "isYou": "false",
                "timestamp": s,
                "type": "1",
                "sender": "구해봇",
                "message": "[구인, 3] 3명의 지원자가 신청하였습니다."
            }
            results = db.child("worker").push(data)
            print("-----------push 결과--------------")
            print(results)

@ignore_first_call
def worker_stream_handler(message):
    print("-----------input2 data--------------")
    print(message["data"])
    if message["data"] is None:
        return

    if message["data"]["isYou"] == "true":
        result, chat_type, add_process = engine.process(Message(message["data"]['sender'], message["data"]['message']))

        now = time.localtime()
        s = "%02d:%02d" % (now.tm_hour, now.tm_min)
        data = {
            "isYou": "false",
            "timestamp": s,
            "type": chat_type,
            "sender": "구해봇",
            "message": result
        }

        # Pass the user's idToken to the push method
        results = db.child("worker").push(data)
        print("-----------push 결과--------------")
        print(results)

        if add_process:
            print("-----------job에 신청메시지 전달--------------")
            data = {
                "isYou": "false",
                "timestamp": s,
                "type": "1",
                "sender": "구해봇",
                "message": "신청하신 업무가 확정 완료 되었습니다. 감사합니다."
            }
            results = db.child("job").push(data)
            print("-----------push 결과--------------")
            print(results)


my_stream = db.child("job").stream(job_stream_handler)
my_stream2 = db.child("worker").stream(worker_stream_handler)


while True:
    data = input("[{}] Type exit to disconnect: ".format('?'))
    if data.strip().lower() == 'exit':
        print('Stop Stream Handler')
        if my_stream:
            my_stream.close()
        elif my_stream2:
            my_stream2.close()
        break
