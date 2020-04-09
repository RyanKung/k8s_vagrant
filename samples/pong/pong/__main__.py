import os
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def pong():
    return "pong"

app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8000))
