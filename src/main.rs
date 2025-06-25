use itemmanager::Inventory;
use std::io::{stdin, stdout};
use std::{thread};
use std::time::Duration;

pub struct Game{
    //TODO:
}

pub struct Player{
    pub name: String,
    inventory: Inventory
}

impl Player{
    pub fn new(name: String) -> Player{
        Player{
            name: name,
            inventory: Inventory::new()
        }
    }
}

pub fn get_text_from_user() -> String{
    let mut text = String::new();

    stdin().read_line(&mut text).unwrap();
    text.replace(&['\r', '\n'], "")
}

fn clear_terminal(){
    print!("\x1B[2J\x1B[1;1H");
}

pub fn main(){
    clear_terminal();

    println!("Hi, here will be dragons and other rpg stuff, but for now it's nice and empty");
    println!("You are about to enter main game loop, nice place, but first what's your character name?");
    
    let player_name=get_text_from_user();
    let mut player = Player::new(player_name);

    println!("hi, {}! your story begins now", player.name);
    thread::sleep(Duration::new(1, 0));
    
    clear_terminal();
    while true{
        
    }
}