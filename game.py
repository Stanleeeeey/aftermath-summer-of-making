from enum import Enum
import time
from time import sleep
import os
import json
import keyboard

from utilities import *

STORY_URI = "data/story.json"
GAME_VARS = {}
FPS = 20
WRITING_FPS = 10


class GameStates(Enum):
    Writing = 0
    AwaitingInput = 1

class PlayerInputs(Enum):
    Continue = 0
    TextInput = 1
    MultipleChoice = 2

class Dialogue:
    def __init__(self, dialogue):
        self.load_text(dialogue["text"])
        self.next_dialogue = dialogue["moveto"]

        if dialogue["playerinput"] == "enter": self.player_input = PlayerInputs.Continue
        elif dialogue["playerinput"] == "textinput":
            self.player_input = PlayerInputs.TextInput
            self.var_name = dialogue["var"]
        elif dialogue["playerinput"] == "choice": self.player_input = PlayerInputs.MultipleChoice
        else: self.player_input = PlayerInputs.Continue
    
    def load_text(self, text):
        if "|" in text:
            spl = text.split("|")
            ans = ""

            for i in range(1, len(spl), 2):

                ans+= spl[i-1]
                ans += GAME_VARS[spl[i]]

            self.text = ans
        else: self.text = text

class Display:
    def __init__(self):
        self.last_generated = time.time()
        self.time_between_letters = 1/WRITING_FPS
        self.index = 0
        self.finished_writing = False

    def set_text(self, text):
        self.text = text
        self.index = 0
        self.finished_writing = False
    
    def frame_generation(self, header, footer):

        if not self.finished_writing:
            self.current_time = time.time()
            clear_terminal()
            columns, lines = os.get_terminal_size()

            #print top TUI
            print(header)

            #dialogue text

            print(self.text[:self.index])
            if self.current_time -self.last_generated > self.time_between_letters:

                self.index+=1
                if self.index == len(self.text): self.finished_writing = True
                self.last_generated = time.time()

            #print remaining lines
            print("\n"*(lines - (count_lines(self.text, self.index)) - 4))
            print(footer)

class Keyboard:
    def __init__(self,):
        self.is_pressed = False
        self.already_used = False

    def is_enter_just_pressed(self):
        if self.is_pressed and not self.already_used:
            self.already_used = True
            return True
        return False
    
    def update(self):
        if not keyboard.is_pressed("enter"):
            self.already_used = False
            self.is_pressed = False
        else:
            self.is_pressed = True



class Game:
    def __init__(self, location):
        self.location = location
        self.time = 1

        self.dialogue_id = 1

        self.state = GameStates.Writing

        self.display = Display()
        self.keyboard = Keyboard()


    def header(self):

        columns, lines = os.get_terminal_size()
        loc_len = len(self.location)
        time_len = len(str(self.time))

        return self.location + " " +"-"*(columns - loc_len - time_len - 2) +" "+ str(self.time)
    
    def footer(self):
        if self.current_dialogue.player_input == PlayerInputs.Continue or (self.current_dialogue.player_input == PlayerInputs.TextInput and self.state == GameStates.Writing):
            return f"press enter to continue " 
        return ""
    
    def load_text(self):
        with open(STORY_URI) as f:
            d = json.load(f)
            self.current_dialogue = Dialogue(d[str(self.dialogue_id)])


    def import_dialogue(self, id):

        self.dialogue_id = id
        self.load_text()
        self.state = GameStates.Writing
        self.display.set_text(self.current_dialogue.text)

    

    def run(self):
        clear_log()
        log("starting game")
        self.import_dialogue(1)
        
        time_between_frames = 1/FPS
        frame_start =  time.time()
        current_time = time.time()
        while True:

            
            
            if self.state == GameStates.AwaitingInput:
                self.display.frame_generation(self.header(), self.footer())
                while self.state == GameStates.AwaitingInput:
                    if self.current_dialogue.player_input == PlayerInputs.Continue  and self.keyboard.is_enter_just_pressed():
                        self.import_dialogue(self.current_dialogue.next_dialogue)
                        print(self.current_dialogue.text)

                    elif self.current_dialogue.player_input == PlayerInputs.TextInput:
                        GAME_VARS[self.current_dialogue.var_name] = get_input()
                        self.import_dialogue(self.current_dialogue.next_dialogue)
                    
                self.keyboard.update()
            if current_time - frame_start > time_between_frames:
                frame_start = time.time()
                self.display.frame_generation(self.header(), self.footer())

            if self.keyboard.is_enter_just_pressed():
                self.display.index = len(self.current_dialogue.text)
                self.state = GameStates.AwaitingInput
                
            if self.display.index == len(self.current_dialogue.text):
                self.state = GameStates.AwaitingInput
                    

            self.keyboard.update()
            current_time = time.time()



                
                
            

