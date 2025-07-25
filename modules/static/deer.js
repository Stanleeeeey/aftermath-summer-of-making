

let deer_speed = 5
let deer_position = [0,0]

let player_position = [window.innerWidth/2,window.innerHeight/2]
let player_direction = [0,0]
let player_speed = 6

let is_w_down = false
let is_s_down = false
let is_a_down = false
let is_d_down = false

let lost = false

const fps = 60;

window.addEventListener("keydown",
    (event) => {
        
        if (event.key === "Enter"){
            document.getElementById("portrait-div").innerHTML = ""
            fight();
            
        }
    }
)

window.addEventListener("resize" , () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
})

function guide_deer(){
    let x_dir = 0
    let y_dir = 0
    if (player_position[0] > deer_position[0]){ x_dir = 1}
    else if(player_position[0] < deer_position[0]){x_dir = -1}

    if (player_position[1] > deer_position[1]){ y_dir = 1}
    else if(player_position[1] < deer_position[1]){y_dir = -1}

    return [x_dir, y_dir]
}

window.addEventListener("keypress", (event) => {
    if (event.key === "w"){player_direction[1] = -1; is_w_down = true;}
    else if (event.key === "s"){player_direction[1] = 1; is_s_down = true}
    else if (event.key === "a"){player_direction[0] = -1; is_a_down = true}
    else if (event.key === "d"){player_direction[0] = 1; is_d_down = true}
})


window.addEventListener("keyup", (event) => {
    if (event.key === "w" && !is_s_down){player_direction[1] = 0; is_w_down = false}
    else if (event.key === "w" && is_s_down){player_direction[1] = 1; is_w_down = false}
    else if (event.key === "s" && !is_w_down){player_direction[1] = 0; is_s_down = false}
    else if (event.key === "s" && is_w_down){player_direction[1] = -1; is_s_down = false}
    else if (event.key === "a" && !is_d_down){player_direction[0] = 0; is_a_down = false}
    else if (event.key === "a" && is_d_down){player_direction[0] = 1; is_a_down = false}
    else if (event.key === "d" && !is_a_down){player_direction[0] = 0; is_d_down = false}
    else if (event.key === "d" && is_a_down){player_direction[0] = -1; is_d_down = false}

})

function check_collision(){
    let deer_corners = [deer_position, [deer_position[0], deer_position[1] + 40], [deer_position[0] + 40, deer_position[1]], [deer_position[0] + 40, deer_position[1] + 40]]

    deer_corners.forEach((corner) => {
        if (corner[0] >= player_position[0] && corner[0] <= player_position[0] + 20 && corner[1] >= player_position[1] && corner[1] <= player_position[1] + 20){
            

            lost = true
        }
    })

}


async function fight(){
    console.log("fight");
    var canvas=document.getElementById("canvas");
    var ctx=canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    var image=new Image();
    image.src="/static/enemy.png";
    image.onload= await async function(){


        let start = performance.now()
        let end = performance.now()
        let time_between_frames = 1000 / fps;
        ctx.fillStyle = "rgb(200 200 200)";
        lost = false
        while(true){

            if(lost){
                alert("deer got you!")
                window.location = "/?move-to=15";
            }
            if (time_between_frames > end - start){
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                

                if (deer_position[0] + deer_speed[0] > canvas.width - 40 || deer_position[0] + deer_speed[0] < 0){
                    deer_speed[0]*=-1
                }
                if (deer_position[1] + deer_speed[1] > canvas.height -40|| deer_position[1] + deer_speed[1] < 0){
                    deer_speed[1]*=-1
                }
                
                
                deer_position[0] += guide_deer()[0]* deer_speed
                deer_position[1] += guide_deer()[1]* deer_speed

                ctx.drawImage(image,deer_position[0], deer_position[1],40, 40);

                if (player_position[0] + player_direction[0] * player_speed > canvas.width - 20 || player_position[0] + player_direction[0] * player_speed < 0){
                    player_direction[0] = 0
                }
                if (player_position[1] + player_direction[1] * player_speed > canvas.height -20|| player_position[1] + player_direction[1] * player_speed < 0){
                    player_direction[1] = 0
                }

                player_position[0] += player_direction[0] * player_speed
                player_position[1] += player_direction[1] * player_speed
                
                ctx.fillRect(player_position[0], player_position[1], 20, 20)

                check_collision()
            }

            await new Promise(r => setTimeout(r, start + time_between_frames - end));
        }
    };

    


}