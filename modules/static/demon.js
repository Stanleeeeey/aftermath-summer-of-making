
let deer_direction = 1
let deer_speed = 5
let deer_position = [window.innerWidth*0.9,window.innerHeight*0.5]

let player_position = [window.innerWidth*0.1,window.innerHeight*0.5]
let player_direction = 0
let player_speed = 6

let is_w_down = false
let is_s_down = false
let is_space_down = false


let lost = false

const fps = 60;
const time_between_attacks = 300;//ms
const time_between_shots = 400;

let demon_life = 20

let pentagrams = []
let bullets = []

window.addEventListener("keydown",
    (event) => {
        
        if (event.key === "Enter"){
            document.getElementById("portrait-div").innerHTML = ""
            fight();
            
        }
    }
)

function guide_deer(){

    let y_dir = 0

    if (player_position[1] > deer_position[1]){ y_dir = 1}
    else if(player_position[1] < deer_position[1]){y_dir = -1}

    return y_dir
}

window.addEventListener("keypress", (event) => {
    if (event.key === "w"){player_direction = -1; is_w_down = true;}
    else if (event.key === "s"){player_direction= 1; is_s_down = true}


    if (event.key === " "){
        
        is_space_down = true
    }

})


window.addEventListener("keyup", (event) => {
    if (event.key === "w" && !is_s_down){player_direction = 0; is_w_down = false}
    else if (event.key === "w" && is_s_down){player_direction = 1; is_w_down = false}
    else if (event.key === "s" && !is_w_down){player_direction = 0; is_s_down = false}
    else if (event.key === "s" && is_w_down){player_direction = -1; is_s_down = false}

    if (event.key === " "){
        is_space_down = false
    }


})

function check_death(){

    pentagrams.forEach((pentagram) => {
        let deer_corners = [pentagram, [pentagram[0], pentagram[1] + 30], [pentagram[0] + 30, pentagram[1]], [pentagram[0] + 30, pentagram[1] + 30]]
        let i = 0;
        deer_corners.forEach((corner) => {
            if (corner[0] >= player_position[0] && corner[0] <= player_position[0] + 20 && corner[1] >= player_position[1] && corner[1] <= player_position[1] + 20){
                
                pentagrams.splice(pentagrams.indexOf(pentagram), 1)
                lost = true
            }
            i++;
        })
    })

}

function check_collisions(){
    bullets.forEach((bullet) => {
        let bullet_corners = [bullet, [bullet[0], bullet[1] + 5], [bullet[0] + 30, bullet[1]], [bullet[0] + 30, bullet[1] + 5]]

        bullet_corners.forEach((corner) => {
            
            if (corner[0] >= deer_position[0] && corner[0] <= deer_position[0] + 40 && corner[1] >= deer_position[1] && corner[1] <= deer_position[1] + 40) {
                
                
                bullets.splice(bullets.indexOf(bullet), 1)
                    
                demon_life -= 1
                if (demon_life <= 0){
                    window.location= "/?move-to=17"
                }
                document.getElementById("life").innerHTML = demon_life
            }
            
        })
    })
}

async function fight(){
    console.log("fight");
    var canvas=document.getElementById("canvas");
    var ctx=canvas.getContext('2d');

    document.getElementById("life").innerHTML = demon_life
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    var image=new Image();
    var pentagram_img=new Image();
    pentagram_img.src = "/static/pentagram.png"
    pentagram_img.onload = await async function(){}
    image.src="/static/enemy.png";
    image.onload= await async function(){


        let start = performance.now()
        let last_pentagram = performance.now()
        let last_shot = performance.now()
        let end = performance.now()
        let time_between_frames = 1000 / fps;
        ctx.fillStyle = "rgb(200 200 200)";
        lost = false
        while(true){

            if(is_space_down && performance.now() - last_shot > time_between_shots){
                last_shot = performance.now()
                bullets.push(structuredClone(player_position))
                
            }

            if(lost){
                
                
                alert("You've been hit, you're exhausted, yet part of you keeps you fighting!")
                window.location = "/demon"
            }
            if (performance.now() - last_pentagram > time_between_attacks){
                last_pentagram = performance.now()
                pentagrams.push(structuredClone(deer_position))
            }
            if (time_between_frames > end - start){
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                pentagrams.forEach((pentagram) =>{
                    ctx.drawImage(pentagram_img,pentagram[0], pentagram[1],30, 30);

                    pentagram[0] -= 5
                    if (pentagram[0] < 0){
                        pentagrams = pentagrams.slice(1)
                    }
                })

                bullets.forEach((bullet) => {
                    ctx.fillRect(bullet[0], bullet[1],30, 5);

                    bullet[0] += 5
                    if (bullet[0] >  window.innerWidth){
                        bullets = bullets.slice(1)
                    }
                })
                if (deer_position[1] + deer_speed > canvas.height -40|| deer_position[1] + deer_speed < 0){
                    deer_speed*=-1
                }

                deer_position[1] += deer_direction* deer_speed

                ctx.drawImage(image,deer_position[0], deer_position[1],40, 40);


                if (player_position[1] + player_direction[1] * player_speed > canvas.height -20|| player_position[1] + player_direction[1] * player_speed < 0){
                    player_direction[1] = 0
                }


                player_position[1] += player_direction * player_speed
                
                ctx.fillRect(player_position[0], player_position[1], 20, 20)

                check_death()
                check_collisions()
            }

            await new Promise(r => setTimeout(r, start + time_between_frames - end));
        }
    };

    


}