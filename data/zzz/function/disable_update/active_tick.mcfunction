scoreboard players add #total_time operator 1

execute if score #game_timer operator matches 1.. run scoreboard players remove #game_timer operator 1

execute if score #game_timer operator matches ..0 run function zzz:disable_update/disable_random_update

execute as @a[scores={disable_update_died=1..}] run function zzz:disable_update/player_died

execute store result score #updates_remaining operator if data storage disable_update:versions enabled[]

function score_time:update {display_format:[minutes,seconds],player:"#game_timer",objective:operator}

execute store result storage disable_update:temp all.disable_update_time int 1 run scoreboard players get #disable_update_time operator
execute store result storage disable_update:temp all.timer int 1 run scoreboard players get #game_timer operator
function zzz:disable_update/update_timer with storage disable_update:temp all

title @a actionbar [{score:{name:"#updates_remaining",objective:operator},color:aqua},{text:" updates remaining "}]

data modify storage disable_update:temp all.disabled set from storage disable_update:versions disabled

function zzz:disable_update/disable_features/loop