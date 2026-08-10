data modify storage disable_update:versions disabled set value []
data modify storage disable_update:versions enabled set from storage disable_update:versions all

tellraw @a {text:"All versions have been re-enabled",color:green}
execute as @a at @s run playsound ui.button.click ui @s