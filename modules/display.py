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

class Display:
    def __init__(self):
        self.last_generated = time.time()
        self.time_between_letters = 1/WRITING_FPS
        self.index = 0
        self.finished_writing = False
        self.header = ''
        self.options = ""
        self.footer = ''

        
        webbrowser.open("http://127.0.0.1:5000")
        app.run()

    

    def set_text(self, text, options = ""):
        self.text = text
        self.index = 0
        self.finished_writing = False
        self.add_options(options)

    def add_options(self, options):
        self.options = ""
        for i in range(len(options)):
            self.options += f"{i+1}. {options[i]}\n"


    def set_header(self, left, right = ''):
        columns, _ = os.get_terminal_size()
        self.header = left + " " +"-"*(columns - len(left) - len(right) - 2) +" "+ str(right)

    def set_footer(self, left, right = ''):
        columns, _ = os.get_terminal_size()
        self.footer = left + " " +"-"*(columns - len(left) - len(right) - 2) +" "+ str(right)
    
    def frame_generation(self):

        if not self.finished_writing:
            self.current_time = time.time()
            clear_terminal()
            columns, lines = os.get_terminal_size()

            top_lines = count_lines(self.header, len(self.header)) + count_lines(self.text, self.index)

            
            #print top TUI
            if self.header: print(self.header)
            #dialogue text
            print(self.text[:self.index])
            if self.current_time -self.last_generated > self.time_between_letters:

                self.index+=1
                if self.index == len(self.text): self.finished_writing = True
                self.last_generated = time.time()

            

            bottom_lines = count_lines(self.options, len(self.options)) + count_lines(self.footer, len(self.footer)) + 1

            #print remaining lines
            print("\n"*(lines - (top_lines+bottom_lines)))
            if self.options: print(self.options)
            print(self.footer)

