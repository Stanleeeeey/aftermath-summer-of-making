let id = 1

const server_url = "http://127.0.0.1:5000/gameinfo"

let current_json = ""

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

async function request_dialog(){
    const response = await fetch(server_url + "/" +  id,{
        method: 'POST',
        headers: {
            Accept: 'application/json',
        },
    });
    
    const text = await response.text()

    current_json = JSON.parse(text)


    
}

window.addEventListener("load", function(){
    enable_loading()
    request_dialog()
   
})