from flask import Flask, request
import requests
import os

app = Flask(__name__)

KAKAOWORK_APP_KEY = os.environ.get(".06ded3de.73629468d2294c0e8d31627eec840131")
GEMINI_API_KEY = os.environ.get("AIzaSyB26IFyiIuAfPpEmPKgKrzgtDwTzVUh2cw")

def ask_ai(text):

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

    data = {
        "contents":[
            {
                "parts":[
                    {"text":text}
                ]
            }
        ]
    }

    r = requests.post(url,json=data)

    result=r.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]

def send_message(conversation_id,text):

    url="https://api.kakaowork.com/v1/messages.send"

    headers={
        "Authorization":"Bearer "+KAKAOWORK_APP_KEY,
        "Content-Type":"application/json"
    }

    data={
        "conversation_id":conversation_id,
        "text":text
    }

    requests.post(url,headers=headers,json=data)

@app.route("/webhook",methods=["POST"])
def webhook():

    data=request.json

    text=data.get("text")
    conversation_id=data.get("conversation_id")

    if text and text.startswith("/ask"):

        question=text.replace("/ask","")

        answer=ask_ai(question)

        send_message(conversation_id,answer)

    return "ok"

@app.route("/")
def home():
    return "bot running"

app.run(host="0.0.0.0",port=10000)