Made for Minecraft 26.3

When the player breaks a block, a random update is disabled. This means any blocks, items, or mobs/entities that were added in that update will disappear when the player is nearby.

Can be reset with `/function disable_update:reset`

If you're curious about how this works, it utilizes the `update_tags` generator from my [personal data pack library, bldp](https://github.com/blockerlocker/bldp) to create Block, Item, and Entity Type tags for every single update.