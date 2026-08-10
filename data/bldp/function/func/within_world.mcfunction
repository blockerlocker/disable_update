execute store success storage bldp:within_world out byte 1 run clone ~ ~ ~ ~ ~ ~ ~ ~ ~ strict replace force
execute if data storage bldp:within_world {out:true} run return run data remove storage bldp:within_world out
data remove storage bldp:within_world out
return fail