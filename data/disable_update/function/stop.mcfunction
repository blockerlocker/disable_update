data modify storage disable_update:versions disabled set value []
data modify storage disable_update:versions enabled set from storage disable_update:versions all

data modify storage disable_update:state all.active set value false


tellraw @a {text:"Game stopped!",color:green}
execute as @a at @s run playsound ui.button.click ui @s
title @a actionbar ""
title @a subtitle ""