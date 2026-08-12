execute unless data storage disable_update:versions enabled[0] run return run function zzz:disable_update/no_more_updates

data modify storage bldp:array_random in set from storage disable_update:versions enabled
function bldp:func/array/random/init

function zzz:disable_update/disable_update with storage bldp:array_random out

function zzz:disable_update/reset_timer

title @a times 0.1s 1.5s 1s
title @a title ""
title @a subtitle [{text:"Disabled ",color:yellow},{storage:"bldp:array_random",nbt:"out.id",interpret:true,color:aqua}]

execute as @a at @s run playsound minecraft:block.vault.break ui @s ~ ~ ~ 2 2