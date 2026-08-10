$execute as @e[type=#bldp:update/$(version),type=!item] run data merge entity @s {Health:0,DeathTime:20}
$kill @e[type=#bldp:update/$(version),type=!item]
