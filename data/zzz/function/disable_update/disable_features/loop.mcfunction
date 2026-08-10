execute unless data storage disable_update:temp all.disabled[0] run return fail

data modify storage disable_update:temp all.version set from storage disable_update:temp all.disabled[0].id

function zzz:disable_update/disable_features/entity with storage disable_update:temp all
execute as @a at @s run function zzz:disable_update/disable_features/block with storage disable_update:temp all
function zzz:disable_update/disable_features/item with storage disable_update:temp all

data remove storage disable_update:temp all.disabled[0]

function zzz:disable_update/disable_features/loop