import Utils
from ItemUnitDefinition import *
from BattleUnitDefinition import *

key_to_item = {
    CONSUMABLE_MINOR_HEALTH_POTION: consumable_item_minor_health_potion_sample,
    CONSUMABLE_MINOR_ATTACK_PACK: consumable_item_minor_attack_pack_sample,
    CONSUMABLE_MINOR_DEFENSE_PACK: consumable_item_minor_defense_pack_sample,
}

loot_matrix = {
    ENEMY_TYPE_BIKER: [
        (CONSUMABLE_MINOR_HEALTH_POTION, 20),
        (CONSUMABLE_MINOR_ATTACK_PACK, 5),
    ],
    ENEMY_TYPE_ENFORCER: [
        (CONSUMABLE_MINOR_HEALTH_POTION, 30),
        (CONSUMABLE_MINOR_DEFENSE_PACK, 5),
    ],
    ENEMY_TYPE_FREEZER: [
        (CONSUMABLE_MINOR_HEALTH_POTION, 50),
        (CONSUMABLE_MINOR_ATTACK_PACK, 15),
    ],
    ENEMY_TYPE_FLAMETHROWER: [
        (CONSUMABLE_MINOR_HEALTH_POTION, 50),
        (CONSUMABLE_MINOR_ATTACK_PACK, 10),
        (CONSUMABLE_MINOR_DEFENSE_PACK, 10),
    ],
    ENEMY_TYPE_SUICIDE_DRONE: [
        (CONSUMABLE_MINOR_HEALTH_POTION, 10),
        (CONSUMABLE_MINOR_ATTACK_PACK, 5),
        (CONSUMABLE_MINOR_DEFENSE_PACK, 5),
    ],
    ENEMY_TYPE_UNDERBOSS: [
        (CONSUMABLE_MINOR_HEALTH_POTION, 50),
        (CONSUMABLE_MINOR_ATTACK_PACK, 25),
        (CONSUMABLE_MINOR_DEFENSE_PACK, 25),
    ],
    ENEMY_TYPE_BOSS: [
        (CONSUMABLE_MINOR_ATTACK_PACK, 50),
        (CONSUMABLE_MINOR_DEFENSE_PACK, 50),
    ],
    ENEMY_TYPE_KINGPIN: [
        (CONSUMABLE_MINOR_DEFENSE_PACK, 100),
    ],
}

# some validation on loot matrix
for enemy_type, chance_array in loot_matrix.items():
    total_chance = 0
    for item_key, chance in chance_array:
        total_chance += chance
    if total_chance > 100:
        raise Exception("total loot chance > 100 for enemy_type: {}".format(enemy_type))


def handle_loot_dropping(battle_unit_data):
    loot = None
    enemy_type = battle_unit_data.type
    if enemy_type not in loot_matrix:
        raise Exception("enemy_type {} is not in loot_matrix".format(enemy_type))
    rand_value = random.randint(0, 99)
    threshold = 0
    for item_key, chance in loot_matrix[enemy_type]:
        threshold += chance
        if rand_value < threshold:
            loot = deepcopy(key_to_item[item_key])
            break

    return loot
