data modify storage disable_update:versions disabled set value []
data modify storage disable_update:versions enabled set from storage disable_update:versions all

scoreboard players reset @a disable_update_died

function zzz:disable_update/add_bossbar

data modify storage disable_update:state all.active set value true

function zzz:disable_update/reset_timer

tellraw @a [{text:"Game started! Next update disabled in ",color:green},{score:{name:"#disable_update_time",objective:operator}}," ticks!"]
execute as @a at @s run playsound ui.button.click ui @s