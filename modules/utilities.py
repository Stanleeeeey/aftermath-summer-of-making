import os 
from datetime import datetime 
from modules import LOG_URI


def clear_terminal():
    flush_input()
    os.system('cls' if os.name == 'nt' else 'clear')

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def get_input():
    flush_input()
    x = input(">> ")
    while x =="":
        print("You're shy, I get it, but it's important")
        x = input(">> ")
    return x

def count_lines(text, index):
    current_text = text[:index].split("\n")
    columns, _ = os.get_terminal_size()

    return sum([len(i) // columns + 1 for i in current_text])
    
def log(text: str):
    with open(LOG_URI, "a") as f:
        f.write(f"[{datetime.now().time()}] {text}\n")

def clear_log():
    with open(LOG_URI, "w") as f:
        f.write(f"[{datetime.now().time()}] cleared log\n")