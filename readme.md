# Aftermath
or something, don't know yet

## What is it?

Aftermath is an old school rpg, inspired by classics such as Zork, yet having its own more modern, unique twist. 

## How to play

simply run `main.py`

## How does the story work

`story.json` consists of series of dialogues interlinked with each other.

There are three basic types 

### 1. Player input
```json
    "1": {
            "text":"What's your name",
            "playerinput":"textinput",
            "moveto":2,
            "var":"playername"
    },
```

- "1" is an id of a dialogue 
- "text" is what will be displayed to the player
- "playerinput" specifies what kind of reaction we excpect from the player, in this case a text inpit - their name.
- "moveto" specifies which dialogue will be displayed after to the player, in our case it's a dialogue number 2
- "var" a name of a variable where answer will be stored

### 2. Continue
```json
    "2": {
            "text":"nice to meet you |playername|!",
            "playerinput":"enter",
            "moveto":3
    },
```
another type of player input is `"enter"` where player simply clicks enter to move onto the next dialogue

Additionally `||` is used to display variable

### 3. Multiplechoice

```json
    "3": {
        "text":"what's your favourite cupcake?",
        "playerinput":"choice",
        "choices":["chocolate", "raspberry"],
        "moveto":[4, 5]
    },

```

- "choices" - what player will see
- "moveto" is now an array. If player chooses "choclate" it moves to dialogue 4, if they choose "rapberry" game moves to dialogue 5 
