scoreboard players operation #hours score_time = #display_time score_time
scoreboard players set #72000 score_time 72000

execute store result storage score_time:temp all.format_number int 1 run scoreboard players operation #hours score_time /= #72000 score_time

function score_time:zzz/format_number
data modify storage score_time:temp all.final append from storage score_time:temp all.format_number

scoreboard players operation #subtract score_time = #hours score_time
scoreboard players operation #subtract score_time *= #72000 score_time
scoreboard players operation #display_time score_time -= #subtract score_time