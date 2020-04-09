import os
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def ping():
    return requests.get(os.getenv("PONG_SVC")).data

app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8000))
