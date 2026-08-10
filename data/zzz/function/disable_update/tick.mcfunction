execute as @a if predicate bldp:mined_block run function zzz:disable_update/mined_block

    execute store result score #updates_remaining operator if data storage disable_update:versions enabled[]

title @a actionbar [{score:{name:"#updates_remaining",objective:operator},color:green},{text:" updates remaining "}]

data modify storage disable_update:temp all.disabled set from storage disable_update:versions disabled

function zzz:disable_update/disable_features/loop