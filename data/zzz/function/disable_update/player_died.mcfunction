scoreboard players reset @s disable_update_died

gamemode spectator @s

data modify storage disable_update:versions disabled set value []
data modify storage disable_update:versions enabled set from storage disable_update:versions all

data modify storage disable_update:state all.active set value false

bossbar remove disable_update:timer

function score_time:update {display_format:[minutes,seconds],player:"#total_time",objective:operator}

title @s times 0.1s 6s 1s
title @s title ""
title @s subtitle [{text:"You survived for ",color:yellow},{score:{name:"#total_time",objective:operator},color:aqua},{text:"!"}]

execute as @a at @s run playsound block.beacon.deactivate ui @s