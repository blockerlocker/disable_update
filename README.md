Made for Minecraft 26.3

Every 30 seconds, a random update is removed from the game, and all blocks, items, and entities from that update are removed from the world and the player's inventory.

| Command | Description |
| --- | --- |
| `/function disable_update:start` | Start the game. |
| `/function disable_update:stop` | End the game. |
| `/function disable_update:set_time {ticks:<time>}` | Customize the time between update removals to be something other than 30 seconds. |

If you're curious about how this works, it utilizes the `update_tags` generator from my [personal data pack library, bldp](https://github.com/blockerlocker/bldp) to create Block, Item, and Entity Type tags for every single update. As for the timer, it's just a basic scoreboard that ticks up and get's reformatted into a time code using [my data pack library score_time](https://github.com/blockerlocker/score_time).