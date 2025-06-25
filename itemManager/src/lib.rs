
pub enum Modifier{
    Strength(u32),
    Dexterity(u32),
    Constitution(u32),
    Inteligence(u32),
    Charisma(u32),
}


pub struct Inventory{
    items: Vec<Item>

}

pub struct Effect{
    modifier: Modifier,
    name: String,
}

pub struct Item{
    id: u32,
    name:String,
    description: String,
    effects: Vec<Effect>,
    
}

impl Inventory{

    pub fn new() -> Self{
        Inventory{
            items: vec![]
        }
    }

    pub fn add_item(&mut self, item: Item){
        self.items.push(item);
    }

    pub fn remove_item_by_id(&mut self, id: u32){
        let mut index = 0;
        for item in &self.items{
            if item.id == id{
                self.items.remove(index);
                break;
            }
            index+=1;
        }
    }

    pub fn get_items(&self) -> &Vec<Item>{
        &self.items
    }
}

impl Item{
    pub fn new(id: u32, name: String, description: String, effects: Vec<Effect>)-> Self{
        Item{
            id: id,
            name: name,
            description: description,
            effects: effects
        }
    }
}

