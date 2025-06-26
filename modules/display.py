import time
from modules.utilities import *
from modules import WRITING_FPS

class Display:
    def __init__(self):
        self.last_generated = time.time()
        self.time_between_letters = 1/WRITING_FPS
        self.index = 0
        self.finished_writing = False
        self.header = ''
        self.options = ""
        self.footer = ''

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

