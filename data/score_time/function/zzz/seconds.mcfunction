scoreboard players operation #seconds score_time = #display_time score_time
scoreboard players set #20 score_time 20

execute store result storage score_time:temp all.format_number int 1 run scoreboard players operation #seconds score_time /= #20 score_time

function score_time:zzz/format_number
data modify storage score_time:temp all.final append from storage score_time:temp all.format_number

scoreboard players operation #subtract score_time = #seconds score_time
scoreboard players operation #subtract score_time *= #20 score_time
scoreboard players operation #display_time score_time -= #subtract score_time