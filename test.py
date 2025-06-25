import keyboard
from time import sleep
import sys
import os

from models.player import Player

clear_terminal = lambda : os.system('cls' if os.name == 'nt' else 'clear')

def print_slowly(text):
    for i, letter in enumerate(text):

        print(letter, end = "")
        sys.stdout.flush()
        sleep(0.1)
        if keyboard.is_pressed("enter"):
            print(text[i:])
            return
    print()

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def get_input():
    x = input(">> ")
    while x =="":
        print("You're shy, I get it, but it's important")
        x = input(">> ")
    return x

def count_lines(text, text_index):
    return text.count("\n") + 1

class Game:
    def __init__(self, location):
        self.location = location
        self.time = 1
        self.current_text = "Hi, here will be dragons and other rpg stuff, but for now it's nice and empty\nYou are about to enter main game loop, nice place, but first what's your character name?"
        self.current_text_index = 0
        self.footer_type = "continue"

    def get_header(self):

        columns, lines = os.get_terminal_size()
        loc_len = len(self.location)
        time_len = len(str(self.time))

        return self.location + " " +"-"*(columns - loc_len - time_len - 2) +" "+ str(self.time)
    
    def footer(self):
        if self.footer_type == "input":
            return get_input()
        return "press enter to continue"

    def frame_generation(self):
        clear_terminal()
        columns, lines = os.get_terminal_size()

        print(self.get_header())
        print(self.current_text[:self.current_text_index])
        self.current_text_index+=1
        print("\n"*(lines - (count_lines(self.current_text, self.current_text_index)) - 4))
        print(self.footer())
        sleep(0.1)
        if keyboard.is_pressed("enter"):
            self.current_text_index = len(self.current_text)

if __name__ == "__main__":
    clear_terminal()


    game = Game("home")
    while True:
        game.frame_generation()

