from enum import Enum
import time
from time import sleep
import os
import json

from modules.keyboard import Keyboard
from modules.utilities import *
from modules.display import Display
from modules.dialogue import Dialogue, PlayerInputs
from modules import STORY_URI, FPS, GAME_VARS


class GameStates(Enum):
    Writing = 0
    AwaitingInput = 1
    Combat = 2




class Game:
    def __init__(self, location):
        self.location = location
        self.time = 1

        self.dialogue_id = 1

        self.state = GameStates.Writing

        self.display = Display()
        self.keyboard = Keyboard()



    
    def generate_footer(self):
        if self.current_dialogue.player_input == PlayerInputs.Continue or (self.current_dialogue.player_input == PlayerInputs.TextInput and self.state == GameStates.Writing):
            return f"press enter to continue " 
        if self.current_dialogue.player_input == PlayerInputs.MultipleChoice:
            return f"choose" 
        return ""
    
    def load_text(self):
        with open(STORY_URI) as f:
            d = json.load(f)
            self.current_dialogue = Dialogue(d[str(self.dialogue_id)])


    def import_dialogue(self, id):

        self.dialogue_id = id
        self.load_text()
        self.state = GameStates.Writing
        if self.current_dialogue.player_input == PlayerInputs.MultipleChoice:
            
            self.display.set_text(self.current_dialogue.text, self.current_dialogue.options)
        else:
            self.display.set_text(self.current_dialogue.text)
        
        self.display.set_footer(self.generate_footer(), "press q to do something")


    #this code prapares game for running
    def initialize_game(self,):
        clear_log()
        log("starting game")
        self.import_dialogue(1)

    def await_input(self):
        self.display.frame_generation()
        while self.state == GameStates.AwaitingInput:
                    
            if self.current_dialogue.player_input == PlayerInputs.Continue and self.keyboard.is_enter_just_pressed():
                self.import_dialogue(self.current_dialogue.next_dialogue)      

            elif self.current_dialogue.player_input == PlayerInputs.TextInput:
                GAME_VARS[self.current_dialogue.var_name] = get_input()
                self.import_dialogue(self.current_dialogue.next_dialogue)

            elif self.current_dialogue.player_input == PlayerInputs.MultipleChoice:
                picked = int(get_input())
                self.import_dialogue(self.current_dialogue.next_dialogue[picked-1][1])

            self.keyboard.update()


    def check_dialogue_status(self):
        if self.keyboard.is_enter_just_pressed():
            self.display.index = len(self.current_dialogue.text)
            self.state = GameStates.AwaitingInput
                
        if self.display.index == len(self.current_dialogue.text):
            self.state = GameStates.AwaitingInput

    def run(self):

        self.initialize_game()
        
        time_between_frames = 1/FPS
        frame_start =  time.time()
        current_time = time.time()
        
        #main game loop
        while True:
            
            if self.state == GameStates.AwaitingInput: self.await_input()

            if current_time - frame_start > time_between_frames:
                frame_start = time.time()
                self.display.frame_generation()

            self.check_dialogue_status()
                    

            self.keyboard.update()
            current_time = time.time()



                
                
            

