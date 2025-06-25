import keyboard
from time import sleep
import sys

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

    return x

if __name__ == "__main__":
    
    print_slowly("Hi, here will be dragons and other rpg stuff, but for now it's nice and empty")
    print_slowly("You are about to enter main game loop, nice place, but first what's your character name?")
    
    flush_input()
    player_name = get_input()
    print_slowly(f"nice to meet you {player_name}!")

