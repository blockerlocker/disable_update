$scoreboard players set #disable_update_time operator $(ticks)

$tellraw @a {text:"Set time between update removals to $(ticks) ticks!",color:green}
execute as @a at @s run playsound ui.button.click ui @s