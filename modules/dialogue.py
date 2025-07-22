from enum import Enum
from modules import GAME_VARS

class PlayerInputs(Enum):
    Continue = 0
    TextInput = 1
    MultipleChoice = 2

class Dialogue:
    def __init__(self, dialogue):
        self.load_text(dialogue["text"])
        self.next_dialogue = dialogue["moveto"]

        if dialogue["playerinput"] == "enter":
            self.player_input = PlayerInputs.Continue

        elif dialogue["playerinput"] == "textinput":
            self.player_input = PlayerInputs.TextInput
            self.var_name = dialogue["var"]
        elif dialogue["playerinput"] == "choice":
            self.player_input = PlayerInputs.MultipleChoice
            self.options = dialogue["choices"]
            self.next_dialogue = [[self.options[i], self.next_dialogue[i]] for i in range(len(self.options))]
        else: self.player_input = PlayerInputs.Continue

        dialogue["text"] = self.text
        self.dialogue = dialogue
    
    def load_text(self, text):
        if "|" in text:
            spl = text.split("|")
            ans = ""
            i=1
            while i <= len(spl):

                ans+= spl[i-1]
                try:
                    ans += GAME_VARS[spl[i]]
                except:
                    pass
                i+=2

            self.text = ans
            print(self.text, spl)
        else: self.text = text
       

    def get_json(self):
        return self.dialogue