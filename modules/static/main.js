let id = 1

const server_url = "http://127.0.0.1:5000/gameinfo"
let is_enter_pressed = false;
let gameState = "loading"
let player_response = ""
let dialog = undefined

function enable_loading(){
    let loading = document.getElementById("loading")
    loading.classList.remove("loading-hidden")
    loading.classList.add("loading-visible")


}

function disable_loading(){
    let loading = document.getElementById("loading")
    loading.classList.remove("loading-visible")
    loading.classList.add("loading-hidden")
}

async function request_dialog(dialog_id, args = ""){
    const response = await fetch(server_url + "/" +  dialog_id,{
        method: 'POST',
        headers: {
            Accept: 'application/json',
        },
        body: args
    });
    
    const text =  await response.text()
    const ans = JSON.parse(text)
    dialog = ans
    return  ans
    
}

function prepare_choices(choices){

    let ans = ""
    choices.forEach((element, index) => {
        ans += (1+index) + ". "+element + "<br>"
    });
    return ans
}

async function write(dialog){
    gameState = "writing"
    let text = dialog.text
    document.getElementById("text").innerHTML = ""
    for (let i = 0; i < text.length; i++) {
        document.getElementById("text").innerHTML = document.getElementById("text").innerHTML + text[i]
        await new Promise(r => setTimeout(r, 30));

        if (is_enter_pressed === true){
            document.getElementById("text").innerHTML = text
            break;
        }
    };

    if(dialog.playerinput === "textinput"){
        document.getElementById("options").innerHTML = "type your response"
        gameState = "awaitingtextinput"
    }
    else if (dialog.playerinput === "enter"){
        document.getElementById("options").innerHTML = "press enter to continue"
        gameState = "awaitinginput"
    }
    else if (dialog.playerinput === "choice"){
        document.getElementById("options").innerHTML = "type your option"
        choices = prepare_choices(dialog["choices"])
        document.getElementById("choices").innerHTML = choices
        gameState = "awaitingtextinput"
    }
   
    
}

async function wrtie_title(dialog){
    gameState = "writing"
    let text = dialog.text
    document.getElementById("title").innerHTML = ""
    for (let i = 0; i < text.length; i++) {
        document.getElementById("title").innerHTML = document.getElementById("title").innerHTML + text[i]
        await new Promise(r => setTimeout(r, 30));

        if (is_enter_pressed === true){
            document.getElementById("title").innerHTML = text
            break;
        }
    };
    gameState = "awaitinginput"
}

function display_dialog(dialog, ){
    console.log(dialog)
    disable_loading()
    console.log(dialog.type)
    if (dialog.type === undefined || dialog.type === "text"){
        write(dialog)
    } else if(dialog.type === "title"){
        wrtie_title(dialog)
    }
    

}

async function handle_scene(){
    document.getElementById("text").innerHTML = ""
    document.getElementById("title").innerHTML = ""
    document.getElementById("options").innerHTML = ""

    
    if (gameState === "awaitinginput" ){
        dialog = await request_dialog(dialog.moveto)
    }
    else if (gameState === "awaitingtextinput" && dialog.playerinput === "choice"){
        console.log(dialog.moveto, Number(player_response) - 1, player_response)

        dialog = await request_dialog(dialog.moveto[Number(player_response) - 1], player_response)
        document.getElementById("choices").innerHTML = ""
    }
    else if (gameState === "awaitingtextinput"){
        console.log(dialog.moveto[dialog.playerinput])
        dialog = await request_dialog(dialog.moveto, player_response)
    }
    player_response = ""
    document.getElementById("player-response").innerHTML = ""
    document.getElementById("options").innerHTML = "press enter to continue"

    

    display_dialog(dialog )


}

window.addEventListener("load", async function(){
    enable_loading()
    let dialog = await request_dialog(1)

    display_dialog(dialog)
})

window.addEventListener("keydown", async (event) =>{

    if(event.key === "Enter" && gameState !== "awaitingtextinput" && gameState !== "awaitinginput"){
        is_enter_pressed = true;
        await new Promise(r => setTimeout(r, 40));
        is_enter_pressed = false;
    }
    else if(gameState === "awaitingtextinput" && event.key.length === 1){
        player_response += event.key
        document.getElementById("player-response").innerHTML = player_response
    }
    else if(gameState === "awaitingtextinput" && event.key === "Backspace"){
        player_response = player_response.substring(0, player_response.length - 1)
        document.getElementById("player-response").innerHTML = player_response

    }
    else if(event.key === "Enter"){
        handle_scene()
    }



})

