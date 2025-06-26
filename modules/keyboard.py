import keyboard



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


