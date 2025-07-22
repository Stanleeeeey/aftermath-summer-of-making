from enum import Enum
import time
from time import sleep
import os
import json

from modules.keyboard import Keyboard
from modules.utilities import *
from modules.server import Server
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

        self.server = Server()

    #this code prapares game for running
    def initialize_game(self,):
        clear_log()
        log("starting game")
        

    def run(self):

        self.initialize_game()
        self.server.run()



                
                
            

