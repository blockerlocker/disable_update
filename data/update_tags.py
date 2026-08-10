import os, urllib.request, json, requests, re
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

print("--Grabbing version manifest")
version_manifest = json.load(urllib.request.urlopen("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"))

latest_snapshot = version_manifest["latest"]["snapshot"]
version_dict = version_manifest["versions"]

version_dict.sort(key=lambda version: version["releaseTime"],reverse=True)

print("--Filtering by release versions and latest snapshot")
all_versions = [{"id":version["id"]} for version in version_dict if version["type"] == "release" or version["id"] == "1.5"]
if not {"id": latest_snapshot} in all_versions:
    all_versions.insert(0, {"id": latest_snapshot})

def get_registry_content_list(version,registry):
    version_response = requests.get(f"https://raw.githubusercontent.com/misode/mcmeta/{version}-registries/{registry}/data.json")
    if version_response.status_code == 200:
        item_list = version_response.json()
        item_list = [modernize_id(item,registry) for item in item_list if modernize_id(item,registry) != None]
        return item_list
    else:
        return None

def modernize_id(item,registry):
    if item == "chain":
        return "iron_chain"
    elif item == "grass":
        return "short_grass"
    elif "pottery_shard_" in item:
        return re.sub(r"pottery_shard_(.*)", r"\1_pottery_sherd", item)
    elif item == "scute":
        return "turtle_scute"
    elif item == "zombie_pigman_spawn_egg":
        return "zombified_piglin_spawn_egg"
    elif item == "zombie_pigman":
        return "zombified_piglin"
    elif item == "grass_path":
        return "dirt_path"
    elif item == "rose":
        return "poppy"
    elif item == "boat":
        return "oak_boat"
    elif item == "chest_boat":
        return "oak_chest_boat"
    elif registry == "entity_type" and item == "potion":
        return "splash_potion"
    elif item == "creaking_transient":
        return None
    else:
        return(item)

print("--Grabbing and modernizing lists for each version")
for version in all_versions:
    version["item_list"] = get_registry_content_list(version["id"],"item")
    version["block_list"] = get_registry_content_list(version["id"],"block")
    version["entity_type_list"] = get_registry_content_list(version["id"],"entity_type")

def filter_lists_chronologically(list):
    for version in all_versions:
        if not version == all_versions[-1] and (version[list] and all_versions[all_versions.index(version) + 1][list]) != None:
            current_list = version[list]
            previous_list = all_versions[all_versions.index(version) + 1][list]
            
            test_current_list = current_list.copy()

            for item in test_current_list:
                if item in previous_list:
                    current_list.remove(item)

            all_versions[all_versions.index(version)][list] = current_list

print("--Filtering item lists by newly added items")
filter_lists_chronologically("item_list")
filter_lists_chronologically("block_list")
filter_lists_chronologically("entity_type_list")

def scan_for_version(id):
    return all_versions.index(next((version for version in all_versions if version["id"] == id), None))

def transfer_items(tag_list,source,target,filter):
    test_list = all_versions[scan_for_version(source)][tag_list].copy()
    for item in test_list:
        if re.search(filter,item):
            all_versions[scan_for_version(target)][tag_list].append(item)
            all_versions[scan_for_version(source)][tag_list].remove(item)
    if len(all_versions[scan_for_version(source)][tag_list]) == 0:
        all_versions[scan_for_version(source)][tag_list] = None

print("--Fixing experimental items")
transfer_items("item_list","1.17","1.21.2","bundle")
transfer_items("item_list","1.19.3","1.20","^(?!(ender_dragon|iron_golem|snow_golem|wither)).*")
transfer_items("item_list","1.19.4","1.20",".")
transfer_items("item_list","1.20.3","1.21",".")
transfer_items("item_list","1.20.5","1.21","^(?!(armadillo|wolf_armor)).*")
transfer_items("item_list","1.21.2","1.21.4","pale_oak_|creaking_|pale_moss_|pale_hanging_moss")

print("--Fixing experimental entities")
transfer_items("entity_type_list","1.19.3","1.20",".")
transfer_items("entity_type_list","1.19.4","1.20","sniffer")
transfer_items("entity_type_list","1.20.3","1.21",".")
transfer_items("entity_type_list","1.20.5","1.21","^(?!(armadillo)).*")
transfer_items("entity_type_list","1.21.2","1.21.4","pale_oak_|creaking")

print("--Creating manual item lists for preclassic through 1.14")
all_versions[scan_for_version("1.14")]["item_list"] = ["bamboo", "cornflower", "lily_of_the_valley", "wither_rose", "spruce_sign", "birch_sign", "acacia_sign", "jungle_sign", "dark_oak_sign", "stone_slab", "stone_stairs", "andesite_slab", "andesite_stairs", "andesite_wall", "polished_andesite_slab", "polished_andesite_stairs", "diorite_slab", "diorite_stairs", "diorite_wall", "polished_diorite_slab", "polished_diorite_stairs", "granite_slab", "granite_stairs", "granite_wall", "polished_granite_slab", "polished_granite_stairs", "mossy_stone_brick_slab", "mossy_stone_brick_stairs", "mossy_stone_brick_wall", "mossy_cobblestone_slab", "mossy_cobblestone_stairs", "smooth_sandstone_slab", "smooth_sandstone_stairs", "sandstone_wall", "cut_sandstone_slab", "smooth_red_sandstone_slab", "smooth_red_sandstone_stairs", "red_sandstone_wall", "cut_red_sandstone_slab", "smooth_quartz_slab", "smooth_quartz_stairs", "nether_brick_wall", "red_nether_brick_slab", "red_nether_brick_stairs", "red_nether_brick_wall", "end_stone_brick_slab", "end_stone_brick_stairs", "end_stone_brick_wall", "stone_brick_wall", "brick_wall", "prismarine_wall", "loom", "flower_banner_pattern", "creeper_banner_pattern", "skull_banner_pattern", "mojang_banner_pattern", "globe_banner_pattern", "white_dye", "black_dye", "brown_dye", "blue_dye", "suspicious_stew", "crossbow", "panda_spawn_egg", "pillager_spawn_egg", "ravager_spawn_egg", "bell", "barrel", "cartography_table", "fletching_table", "grindstone", "lectern", "smithing_table", "stonecutter", "blast_furnace", "smoker", "cat_spawn_egg", "scaffolding", "jigsaw", "lantern", "sweet_berries", "campfire", "composter", "wandering_trader_spawn_egg", "trader_llama_spawn_egg", "fox_spawn_egg", "leather_horse_armor"]
all_versions[scan_for_version("1.13.1")]["item_list"] = ["dead_tube_coral", "dead_brain_coral", "dead_bubble_coral", "dead_fire_coral", "dead_horn_coral"]
all_versions[scan_for_version("1.13")]["item_list"] = ["pumpkin", "debug_stick", "spruce_button", "spruce_pressure_plate", "spruce_trapdoor", "stripped_spruce_log", "stripped_spruce_wood", "birch_button", "birch_pressure_plate", "birch_trapdoor", "stripped_birch_log", "stripped_birch_wood", "acacia_button", "acacia_pressure_plate", "acacia_trapdoor", "stripped_acacia_log", "stripped_acacia_wood", "dark_oak_button", "dark_oak_pressure_plate", "dark_oak_trapdoor", "stripped_dark_oak_log", "stripped_dark_oak_wood", "kelp", "dried_kelp", "dried_kelp_block", "seagrass", "prismarine_stairs", "prismarine_slab", "prismarine_brick_stairs", "prismarine_brick_slab", "dark_prismarine_stairs", "dark_prismarine_slab", "trident", "turtle_egg", "turtle_scute", "turtle_helmet", "turtle_spawn_egg", "phantom_spawn_egg", "cod_bucket", "salmon_bucket", "pufferfish_bucket", "tropical_fish_bucket", "cod_spawn_egg", "salmon_spawn_egg", "pufferfish_spawn_egg", "tropical_fish_spawn_egg", "tube_coral", "tube_coral_block", "dead_tube_coral_block", "tube_coral_fan", "dead_tube_coral_fan", "brain_coral", "brain_coral_block", "dead_brain_coral_block", "brain_coral_fan", "dead_brain_coral_fan", "bubble_coral", "bubble_coral_block", "dead_bubble_coral_block", "bubble_coral_fan", "dead_bubble_coral_fan", "fire_coral", "fire_coral_block", "dead_fire_coral_block", "fire_coral_fan", "dead_fire_coral_fan", "horn_coral", "horn_coral_block", "dead_horn_coral_block", "horn_coral_fan", "dead_horn_coral_fan", "shulker_box", "drowned_spawn_egg", "phantom_membrane", "sea_pickle", "blue_ice", "nautilus_shell", "heart_of_the_sea", "conduit", "dolphin_spawn_egg"]
all_versions[scan_for_version("1.12")]["item_list"] = ["white_concrete", "white_concrete_powder", "white_glazed_terracotta", "white_bed", "light_gray_concrete", "light_gray_concrete_powder", "light_gray_glazed_terracotta", "light_gray_bed", "gray_concrete", "gray_concrete_powder", "gray_glazed_terracotta", "gray_bed", "black_concrete", "black_concrete_powder", "black_glazed_terracotta", "black_bed", "brown_concrete", "brown_concrete_powder", "brown_glazed_terracotta", "brown_bed", "red_concrete", "red_concrete_powder", "red_glazed_terracotta", "orange_concrete", "orange_concrete_powder", "orange_glazed_terracotta", "orange_bed", "yellow_concrete", "yellow_concrete_powder", "yellow_glazed_terracotta", "yellow_bed", "lime_concrete", "lime_concrete_powder", "lime_glazed_terracotta", "lime_bed", "green_concrete", "green_concrete_powder", "green_glazed_terracotta", "green_bed", "cyan_concrete", "cyan_concrete_powder", "cyan_glazed_terracotta", "cyan_bed", "light_blue_concrete", "light_blue_concrete_powder", "light_blue_glazed_terracotta", "light_blue_bed", "blue_concrete", "blue_concrete_powder", "blue_glazed_terracotta", "blue_bed", "purple_concrete", "purple_concrete_powder", "purple_glazed_terracotta", "purple_bed", "magenta_concrete", "magenta_concrete_powder", "magenta_glazed_terracotta", "magenta_bed", "pink_concrete", "pink_concrete_powder", "pink_glazed_terracotta", "pink_bed", "knowledge_book", "parrot_spawn_egg"]
all_versions[scan_for_version("1.11.1")]["item_list"] = ["iron_nugget"]
all_versions[scan_for_version("1.11")]["item_list"] = ["wither_skeleton_spawn_egg", "stray_spawn_egg", "husk_spawn_egg", "elder_guardian_spawn_egg", "donkey_spawn_egg", "mule_spawn_egg", "skeleton_horse_spawn_egg", "zombie_horse_spawn_egg", "zombie_villager_spawn_egg", "observer", "white_shulker_box", "light_gray_shulker_box", "gray_shulker_box", "black_shulker_box", "brown_shulker_box", "red_shulker_box", "orange_shulker_box", "yellow_shulker_box", "lime_shulker_box", "green_shulker_box", "cyan_shulker_box", "light_blue_shulker_box", "blue_shulker_box", "purple_shulker_box", "magenta_shulker_box", "pink_shulker_box", "shulker_shell", "totem_of_undying", "evoker_spawn_egg", "vex_spawn_egg", "vindicator_spawn_egg", "llama_spawn_egg"]
all_versions[scan_for_version("1.10")]["item_list"] = ["bone_block", "magma_block", "nether_wart_block", "red_nether_bricks", "structure_void", "polar_bear_spawn_egg"]
all_versions[scan_for_version("1.9")]["item_list"] = ["dirt_path", "structure_block", "spectral_arrow", "tipped_arrow", "beetroot", "beetroot_seeds", "beetroot_soup", "dragon_head", "end_rod", "end_stone_bricks", "purpur_block", "purpur_pillar", "purpur_slab", "purpur_stairs", "chorus_plant", "chorus_flower", "chorus_fruit", "popped_chorus_fruit", "shulker_spawn_egg", "dragon_breath", "lingering_potion", "shield", "chain_command_block", "repeating_command_block", "elytra", "spruce_boat", "birch_boat", "jungle_boat", "acacia_boat", "dark_oak_boat", "end_crystal"]
all_versions[scan_for_version("1.8")]["item_list"] = ["granite", "polished_granite", "diorite", "polished_diorite", "andesite", "polished_andesite", "slime_block", "barrier", "iron_trapdoor", "endermite_spawn_egg", "coarse_dirt", "prismarine_crystals", "prismarine_shard", "prismarine", "prismarine_bricks", "dark_prismarine", "sea_lantern", "wet_sponge", "guardian_spawn_egg", "mutton", "cooked_mutton", "rabbit", "cooked_rabbit", "rabbit_stew", "rabbit_hide", "rabbit_foot", "rabbit_spawn_egg", "white_banner", "light_gray_banner", "gray_banner", "black_banner", "brown_banner", "red_banner", "orange_banner", "yellow_banner", "lime_banner", "green_banner", "cyan_banner", "light_blue_banner", "blue_banner", "purple_banner", "magenta_banner", "pink_banner", "armor_stand", "red_sandstone", "cut_red_sandstone", "chiseled_red_sandstone", "smooth_red_sandstone", "red_sandstone_slab", "red_sandstone_stairs", "spruce_fence", "birch_fence", "jungle_fence", "acacia_fence", "dark_oak_fence", "spruce_trapdoor", "birch_trapdoor", "jungle_trapdoor", "acacia_trapdoor", "dark_oak_trapdoor", "spruce_door", "birch_door", "jungle_door", "acacia_door", "dark_oak_door", "spruce_fence_gate", "birch_fence_gate", "jungle_fence_gate", "acacia_fence_gate", "dark_oak_fence_gate"]
all_versions[scan_for_version("1.7.2")]["item_list"] = ["allium", "azure_bluet", "blue_orchid", "lilac", "oxeye_daisy", "peony", "rose_bush", "sunflower", "orange_tulip", "pink_tulip", "red_tulip", "white_tulip", "tall_grass", "large_fern", "packed_ice", "podzol", "infested_cracked_stone_bricks", "infested_mossy_stone_bricks", "infested_chiseled_stone_bricks", "tropical_fish", "salmon", "cooked_salmon", "pufferfish", "red_sand", "command_block_minecart", "white_stained_glass", "light_gray_stained_glass", "gray_stained_glass", "black_stained_glass", "brown_stained_glass", "red_stained_glass", "orange_stained_glass", "yellow_stained_glass", "lime_stained_glass", "green_stained_glass", "cyan_stained_glass", "light_blue_stained_glass", "blue_stained_glass", "purple_stained_glass", "magenta_stained_glass", "pink_stained_glass", "white_stained_glass_pane", "light_gray_stained_glass_pane", "gray_stained_glass_pane", "black_stained_glass_pane", "brown_stained_glass_pane", "red_stained_glass_pane", "orange_stained_glass_pane", "yellow_stained_glass_pane", "lime_stained_glass_pane", "green_stained_glass_pane", "cyan_stained_glass_pane", "light_blue_stained_glass_pane", "blue_stained_glass_pane", "purple_stained_glass_pane", "magenta_stained_glass_pane", "pink_stained_glass_pane", "acacia_log", "acacia_wood", "acacia_leaves", "acacia_sapling", "dark_oak_log", "dark_oak_wood", "dark_oak_leaves", "dark_oak_sapling", "acacia_planks", "acacia_stairs", "acacia_slab", "dark_oak_planks", "dark_oak_stairs", "dark_oak_slab"]
all_versions[scan_for_version("1.6.1")]["item_list"] = ["white_carpet", "light_gray_carpet", "gray_carpet", "black_carpet", "brown_carpet", "red_carpet", "orange_carpet", "yellow_carpet", "lime_carpet", "green_carpet", "cyan_carpet", "light_blue_carpet", "blue_carpet", "purple_carpet", "magenta_carpet", "pink_carpet", "hay_block", "lead", "diamond_horse_armor", "golden_horse_armor", "iron_horse_armor", "horse_spawn_egg", "name_tag", "terracotta", "coal_block","white_terracotta", "light_gray_terracotta", "gray_terracotta", "black_terracotta", "brown_terracotta", "red_terracotta", "orange_terracotta", "yellow_terracotta", "lime_terracotta", "green_terracotta", "cyan_terracotta", "light_blue_terracotta", "blue_terracotta", "purple_terracotta", "magenta_terracotta", "pink_terracotta"]
all_versions[scan_for_version("1.5")]["item_list"] = ["nether_quartz_ore", "quartz", "nether_brick", "redstone_block", "daylight_detector", "hopper", "comparator", "trapped_chest", "light_weighted_pressure_plate", "heavy_weighted_pressure_plate", "quartz_block", "chiseled_quartz_block", "quartz_pillar", "quartz_slab", "quartz_stairs", "activator_rail", "tnt_minecart", "dropper", "hopper_minecart", "smooth_sandstone", "smooth_quartz"]
all_versions[scan_for_version("1.4.6")]["item_list"] = ["nether_brick_slab", "firework_star", "firework_rocket", "enchanted_book"]
all_versions[scan_for_version("1.4.4")]["item_list"] = ["music_disc_wait"]
all_versions[scan_for_version("1.4.2")]["item_list"] = ["beacon", "command_block", "carrot", "golden_carrot", "potato", "baked_potato", "poisonous_potato", "flower_pot", "item_frame", "oak_button", "cobblestone_wall", "mossy_cobblestone_wall", "map", "creeper_head", "player_head", "skeleton_skull", "wither_skeleton_skull", "zombie_head", "nether_star", "carrot_on_a_stick", "pumpkin_pie", "bat_spawn_egg", "witch_spawn_egg", "anvil", "chipped_anvil", "damaged_anvil"]
all_versions[scan_for_version("1.3.1")]["item_list"] = ["oak_slab","spruce_slab", "birch_slab", "jungle_slab", "writable_book", "written_book", "emerald_ore", "emerald", "ender_chest", "sandstone_stairs", "enchanted_golden_apple", "tripwire_hook", "emerald_block", "spruce_stairs", "birch_stairs", "jungle_stairs","oak_wood", "spruce_wood", "birch_wood", "jungle_wood"]
all_versions[scan_for_version("1.2.4")]["item_list"] = ["spruce_planks", "birch_planks", "jungle_planks", "cut_sandstone", "chiseled_sandstone"]
all_versions[scan_for_version("1.2.1")]["item_list"] = ["jungle_log", "jungle_leaves", "jungle_sapling", "experience_bottle", "fire_charge", "ocelot_spawn_egg", "redstone_lamp", "chiseled_stone_bricks"]
all_versions[scan_for_version("1.1")]["item_list"] = ["creeper_spawn_egg", "skeleton_spawn_egg", "spider_spawn_egg", "slime_spawn_egg", "ghast_spawn_egg", "zombified_piglin_spawn_egg", "enderman_spawn_egg", "cave_spider_spawn_egg", "silverfish_spawn_egg", "blaze_spawn_egg", "magma_cube_spawn_egg", "pig_spawn_egg", "sheep_spawn_egg", "cow_spawn_egg", "chicken_spawn_egg", "squid_spawn_egg", "wolf_spawn_egg", "mooshroom_spawn_egg", "villager_spawn_egg"]
all_versions[scan_for_version("1.0")]["item_list"] = ["nether_bricks", "nether_brick_stairs", "nether_brick_fence", "nether_wart", "blaze_rod", "ghast_tear", "gold_nugget", "mycelium", "lily_pad", "blaze_powder", "magma_cream", "spider_eye", "fermented_spider_eye", "glass_bottle", "music_disc_blocks", "music_disc_chirp", "music_disc_far", "music_disc_mall", "music_disc_mellohi", "music_disc_stal", "music_disc_strad", "music_disc_ward", "music_disc_11", "ender_eye", "end_portal_frame", "cauldron", "enchanting_table", "brewing_stand", "potion", "splash_potion", "end_stone", "glistering_melon_slice", "dragon_egg"]
all_versions.insert(0, {"id": "beta_1.8", "item_list": ["stone_bricks", "cracked_stone_bricks", "mossy_stone_bricks", "infested_stone", "infested_cobblestone", "infested_stone_bricks", "brick_slab", "stone_brick_slab", "brick_stairs", "stone_brick_stairs", "glass_pane", "iron_bars", "oak_fence_gate", "vine", "brown_mushroom_block", "red_mushroom_block", "mushroom_stem", "pumpkin_seeds", "melon_seeds", "melon", "melon_slice", "chicken", "cooked_chicken", "beef", "cooked_beef", "rotten_flesh", "ender_pearl"]})
all_versions.insert(0, {"id": "beta_1.7", "item_list": ["piston", "sticky_piston", "shears"]})
all_versions.insert(0, {"id": "beta_1.6", "item_list": ["dead_bush", "short_grass", "fern", "oak_trapdoor", "filled_map"]})
all_versions.insert(0, {"id": "beta_1.5", "item_list": ["spruce_sapling", "birch_sapling", "powered_rail", "detector_rail", "cobweb"]})
all_versions.insert(0, {"id": "beta_1.4", "item_list": ["cookie"]})
all_versions.insert(0, {"id": "beta_1.3", "item_list": ["cobblestone_slab", "petrified_oak_slab", "sandstone_slab", "smooth_stone", "red_bed", "repeater"]})
all_versions.insert(0, {"id": "beta_1.2", "item_list": ["brown_wool", "black_wool", "sugar", "cake", "dispenser", "note_block", "sandstone", "spruce_log", "spruce_leaves", "birch_log", "birch_leaves", "charcoal", "lapis_ore", "lapis_block", "bone", "bone_meal", "light_gray_dye", "gray_dye", "ink_sac", "cocoa_beans", "red_dye", "orange_dye", "yellow_dye", "lime_dye", "green_dye", "cyan_dye", "light_blue_dye", "lapis_lazuli", "purple_dye", "magenta_dye", "pink_dye"]})
all_versions.insert(0, {"id": "alpha_v1.2.1", "item_list": ["netherrack", "soul_sand", "glowstone", "glowstone_dust", "carved_pumpkin", "jack_o_lantern", "clock", "cod", "cooked_cod"]})
all_versions.insert(0, {"id": "alpha_v1.1.1", "item_list": ["fishing_rod"]})
all_versions.insert(0, {"id": "alpha_v1.1.0", "item_list": ["compass"]})
all_versions.insert(0, {"id": "alpha_v1.0.17", "item_list": ["oak_fence"]})
all_versions.insert(0, {"id": "alpha_v1.0.14", "item_list": ["egg", "jukebox", "music_disc_13", "music_disc_cat", "furnace_minecart", "chest_minecart"]})
all_versions.insert(0, {"id": "alpha_v1.0.11", "item_list": ["clay", "clay_ball", "sugar_cane", "paper", "book", "brick", "slime_ball"]})
all_versions.insert(0, {"id": "alpha_v1.0.8", "item_list": ["leather", "milk_bucket"]})
all_versions.insert(0, {"id": "alpha_v1.0.6", "item_list": ["cactus", "oak_boat"]})
all_versions.insert(0, {"id": "alpha_v1.0.5", "item_list": ["snow_block", "snowball"]})
all_versions.insert(0, {"id": "alpha_v1.0.4", "item_list": ["ice", "snow"]})
all_versions.insert(0, {"id": "alpha_v1.0.1", "item_list": ["redstone_ore", "redstone", "redstone_torch", "oak_pressure_plate", "stone_pressure_plate", "stone_button", "lever", "iron_door"]})
all_versions.insert(0, {"id": "infdev", "item_list": ["golden_apple", "ladder", "oak_sign", "oak_door", "bucket", "water_bucket", "lava_bucket", "rail", "minecart", "spawner", "saddle", "oak_stairs", "cobblestone_stairs"]})
all_versions.insert(0, {"id": "indev", "item_list": ["farmland", "furnace", "wooden_hoe", "stone_hoe", "iron_hoe", "golden_hoe", "diamond_hoe", "bread", "wheat_seeds", "wheat", "porkchop", "cooked_porkchop", "flint", "golden_helmet", "golden_chestplate", "golden_leggings", "golden_boots", "diamond_helmet", "diamond_chestplate", "diamond_leggings", "diamond_boots", "painting"]})
all_versions.insert(0, {"id": "indev_0.31", "item_list": ["torch", "chest", "diamond_ore", "diamond_block", "crafting_table", "leather_helmet", "leather_chestplate", "leather_leggings", "leather_boots", "chainmail_helmet", "chainmail_chestplate", "chainmail_leggings", "chainmail_boots", "iron_helmet", "iron_chestplate", "iron_leggings", "iron_boots", "apple", "iron_shovel", "iron_sword", "flint_and_steel", "iron_axe", "iron_pickaxe", "bow", "coal", "diamond", "gold_ingot", "iron_ingot", "wooden_sword", "wooden_axe", "wooden_pickaxe", "wooden_shovel", "stone_sword", "stone_axe", "stone_pickaxe", "stone_shovel", "diamond_sword", "diamond_axe", "diamond_pickaxe", "diamond_shovel", "stick", "golden_sword", "golden_axe", "golden_pickaxe", "golden_shovel", "bowl", "mushroom_stew", "gunpowder", "string", "feather"]})
all_versions.insert(0, {"id": "classic_0.28", "item_list": ["obsidian"]})
all_versions.insert(0, {"id": "classic_0.26_survival_test", "item_list": ["bookshelf", "bricks", "iron_block", "tnt", "mossy_cobblestone", "iron_block", "smooth_stone_slab"]})
all_versions.insert(0, {"id": "classic_0.0.20a", "item_list": ["gold_block", "dandelion", "poppy", "red_mushroom", "brown_mushroom", "white_wool", "light_gray_wool", "gray_wool", "red_wool", "orange_wool", "yellow_wool", "lime_wool", "green_wool", "cyan_wool", "light_blue_wool", "blue_wool", "purple_wool", "magenta_wool", "pink_wool"]})
all_versions.insert(0, {"id": "classic_0.0.19a", "item_list": ["glass", "sponge"]})
all_versions.insert(0, {"id": "classic_0.0.14a", "item_list": ["sand", "gravel", "coal_ore", "iron_ore", "gold_ore", "oak_log", "oak_leaves"]})
all_versions.insert(0, {"id": "classic_0.0.12a", "item_list": ["bedrock"]})
all_versions.insert(0, {"id": "preclassic", "item_list": ["stone", "grass_block", "dirt", "oak_planks", "cobblestone", "oak_sapling"]})

print("--Creating manual entity type lists for preclassic through 1.14")
all_versions[scan_for_version("1.14")]["entity_type_list"] = ["panda", "pillager", "ravager", "cat", "trader_llama", "wandering_trader", "fox"]
all_versions[scan_for_version("1.13")]["entity_type_list"] = ["trident", "phantom", "turtle", "cod", "salmon", "pufferfish", "tropical_fish", "drowned", "dolphin"]
all_versions[scan_for_version("1.12")]["entity_type_list"] = ["parrot", "illusioner"]
all_versions[scan_for_version("1.11")]["entity_type_list"] = ["llama", "vindicator", "evoker", "vex", "evoker_fangs", "llama_spit"]
all_versions[scan_for_version("1.10")]["entity_type_list"] = ["husk", "polar_bear", "stray"]
all_versions[scan_for_version("1.9")]["shulker_bullet", "dragon_fireball", "spruce_boat", "birch_boat", "jungle_boat", "acacia_boar", "dark_oak_boat", "spectral_arrow", "entity_type_list"] = ["shulker", "lingering_potion", "area_effect_cloud"]
all_versions[scan_for_version("1.8")]["entity_type_list"] = ["armor_stand", "endermite", "guardian", "elder_guardian", "rabbit"]
all_versions[scan_for_version("1.7.2")]["entity_type_list"] = ["command_block_minecart"]
all_versions[scan_for_version("1.6.1")]["entity_type_list"] = ["leash_knot", "horse", "mule", "donkey", "skeleton_horse", "zombie_horse"]
all_versions[scan_for_version("1.5")]["entity_type_list"] = ["hopper_minecart", "spawner_minecart", "tnt_minecart"]
all_versions[scan_for_version("1.4.6")]["entity_type_list"] = ["firework_rocket"]
all_versions[scan_for_version("1.4.2")]["entity_type_list"] = ["item_frame", "wither_skull", "zombie_villager", "wither", "wither_skeleton", "bat", "witch"]
all_versions[scan_for_version("1.2.1")]["entity_type_list"] = ["experience_bottle", "ocelot", "iron_golem"]
all_versions[scan_for_version("1.0")]["entity_type_list"] = ["small_fireball", "eye_of_ender", "ender_pearl", "end_crystal", "splash_potion", "blaze", "magma_cube", "mooshroom", "snow_golem", "villager", "ender_dragon"]
all_versions[scan_for_version("beta_1.8")]["entity_type_list"] = ["experience_orb", "cave_spider", "enderman", "silverfish"]
all_versions[scan_for_version("beta_1.5")]["entity_type_list"] = ["lightning_bolt"]
all_versions[scan_for_version("beta_1.4")]["entity_type_list"] = ["wolf"]
all_versions[scan_for_version("beta_1.2")]["entity_type_list"] = ["squid"]
all_versions.insert(0, {"id": "beta_1.0", "entity_type_list": ["egg"]})
all_versions.insert(0, {"id": "alpha_v1.2.0", "entity_type_list": ["ghast", "zombified_piglin", "fishing_bobber", "fireball"]})
all_versions[scan_for_version("alpha_v1.0.14")]["entity_type_list"] = ["chicken", "chest_minecart", "furnace_minecart"]
all_versions[scan_for_version("alpha_v1.0.11")]["entity_type_list"] = ["slime"]
all_versions[scan_for_version("alpha_v1.0.8")]["entity_type_list"] = ["cow"]
all_versions[scan_for_version("alpha_v1.0.6")]["entity_type_list"] = ["oak_boat"]
all_versions[scan_for_version("alpha_v1.0.5")]["entity_type_list"] = ["snowball"]
all_versions[scan_for_version("infdev")]["entity_type_list"] = ["falling_block", "minecart"]
all_versions[scan_for_version("indev")]["entity_type_list"] = ["painting"]
all_versions[scan_for_version("indev_0.31")]["entity_type_list"] = ["giant"]
all_versions[scan_for_version("classic_0.28")]["entity_type_list"] = ["sheep"]
all_versions[scan_for_version("classic_0.26_survival_test")]["entity_type_list"] = ["spider", "tnt"]
all_versions.insert(0, {"id": "classic_0.24_survival_test", "entity_type_list": ["creeper", "pig", "skeleton", "zombie", "arrow", "item"]})

print("--Interpreting block lists from manual item lists for preclassic through 1.14")
all_versions[scan_for_version("1.14")].pop("block_list")
full_block_list = get_registry_content_list(latest_snapshot,"block")
for version in all_versions:
    if "block_list" in version and version["block_list"] == None:
        version.pop("block_list")
    if not "block_list" in version and "item_list" in version and version["item_list"] != None:
        for item in version["item_list"]:
            if item in full_block_list:
                if not "block_list" in version:
                    all_versions[scan_for_version(version["id"])]["block_list"] = []
                all_versions[scan_for_version(version["id"])]["block_list"].append(item)

print("--Adding technical blocks for preclassic through 1.14")
all_versions[scan_for_version("classic_0.0.12a")]["block_list"].extend(["water", "lava"])
all_versions[scan_for_version("indev_0.31")]["block_list"].extend(["fire", "wall_torch"])
all_versions[scan_for_version("infdev")]["block_list"].extend(["oak_wall_sign"])
all_versions[scan_for_version("alpha_v1.0.1")]["block_list"].extend(["redstone_wall_torch", "redstone_wire"])
all_versions[scan_for_version("alpha_v1.2.1")]["block_list"].extend(["nether_portal"])
all_versions[scan_for_version("beta_1.7")]["block_list"].extend(["moving_piston", "piston_head"])
all_versions[scan_for_version("beta_1.8")]["block_list"].extend(["melon_stem", "pumpkin_stem", "attached_melon_stem", "attached_pumpkin_stem"])
all_versions[scan_for_version("1.0")]["block_list"].extend(["end_portal", "water_cauldron"])
all_versions[scan_for_version("1.3.1")]["block_list"].extend(["cocoa", "tripwire"])
all_versions[scan_for_version("1.4.2")]["block_list"].extend(["potted_dandelion", "potted_poppy", "potted_red_mushroom", "potted_oak_sapling", "potted_birch_sapling", "potted_spruce_sapling", "potted_jungle_sapling", "potted_cactus", "potted_fern", "potted_dead_bush", "carrots", "potatoes", "creeper_wall_head", "player_wall_head", "skeleton_wall_skull", "wither_skeleton_wall_skull", "zombie_wall_head"])
all_versions[scan_for_version("1.7.2")]["block_list"].extend(["potted_allium", "potted_azure_bluet", "potted_oxeye_daisy", "potted_blue_orchid", "potted_orange_tulip", "potted_red_tulip", "potted_white_tulip", "potted_pink_tulip", "potted_acacia_sapling", "potted_dark_oak_sapling"])
all_versions[scan_for_version("1.8")]["block_list"].extend(["white_wall_banner", "light_gray_wall_banner", "gray_wall_banner", "black_wall_banner", "brown_wall_banner", "red_wall_banner", "orange_wall_banner", "yellow_wall_banner", "lime_wall_banner", "green_wall_banner", "cyan_wall_banner", "light_blue_wall_banner", "blue_wall_banner", "purple_wall_banner", "magenta_wall_banner", "pink_wall_banner"])
all_versions[scan_for_version("1.9")]["block_list"].extend(["dragon_wall_head", "end_gateway", "beetroots", "frosted_ice"])
all_versions[scan_for_version("1.13")]["block_list"].extend(["tall_seagrass", "kelp_plant", "cave_air", "void_air", "bubble_column", "tube_coral_wall_fan", "brain_coral_wall_fan", "bubble_coral_wall_fan", "fire_coral_wall_fan", "horn_coral_wall_fan", "dead_tube_coral_wall_fan", "dead_brain_coral_wall_fan", "dead_bubble_coral_wall_fan", "dead_fire_coral_wall_fan", "dead_horn_coral_wall_fan"])
all_versions[scan_for_version("1.14")]["block_list"].extend(["potted_cornflower", "potted_lily_of_the_valley", "potted_wither_rose", "potted_bamboo", "bamboo_sapling", "spruce_wall_sign", "birch_wall_sign", "acacia_wall_sign", "jungle_wall_sign", "dark_oak_wall_sign"])

def save_tag(tag_list,path,id):
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(f"{path}/{id}.json", "w") as new_json:
        json.dump({"values":tag_list},new_json,indent=4)

print("--Saving tag files")
applicable_versions = []
for version in all_versions:
    if "item_list" in version and version["item_list"] != None and len(version["item_list"]) > 0:
        save_tag(version["item_list"],"bldp/tags/item/update",version['id'])
        if not version['id'] in applicable_versions:
            applicable_versions.append(version['id'])
    if "block_list" in version and version["block_list"] != None and len(version["block_list"]) > 0:
        save_tag(version["block_list"],"bldp/tags/block/update",version['id'])
        if not version['id'] in applicable_versions:
            applicable_versions.append(version['id'])
    if "entity_type_list" in version and version["entity_type_list"] != None and len(version["entity_type_list"]) > 0:
        save_tag(version["entity_type_list"],"bldp/tags/entity_type/update",version['id'])
        if not version['id'] in applicable_versions:
            applicable_versions.append(version['id'])

if DEBUG == True:
    Path("debug").mkdir(parents=True, exist_ok=True)
    with open(f"debug/update_tags_versions.json", "w") as new_json:
        json.dump({"versions":applicable_versions},new_json,indent=4)