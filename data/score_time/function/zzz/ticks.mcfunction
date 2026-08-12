execute store result storage score_time:temp all.format_number int 1 run scoreboard players get #display_time score_time

function score_time:zzz/format_number
data modify storage score_time:temp all.final append from storage score_time:temp all.format_number