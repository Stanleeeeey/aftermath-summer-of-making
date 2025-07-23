import time
from modules.utilities import *
from modules.dialogue import Dialogue
from modules import WRITING_FPS, STORY_URI, GAME_VARS
from flask import Flask, render_template, request
import webbrowser
import json 

dialogue = None
app = Flask(__name__)

@app.route("/")
def game():
        return render_template("index.html")

def load_text(id):
    global dialogue
    with open(STORY_URI) as f:
        d = json.load(f)
        dialogue = Dialogue(d[str(id)])
        return dialogue.get_json()

@app.route("/gameinfo/<id>", methods = ["POST"])
def gameinfo(id:int):

    try:
        GAME_VARS[dialogue.var_name] = request.data.decode("utf-8")
    except:
        pass
    return load_text(id)


@app.route("/deer", methods = ["GET"])
def deer():
    return render_template("deer.html")

class Server:
    def __init__(self):
        webbrowser.open("http://127.0.0.1:5000")
        

    
    def run(self):
        app.run(port = 5000)

