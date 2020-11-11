from Constants import *
from AIDefinition import *
from SkillDefinition import *
from ColorDefinition import *

# --- ENEMY TYPES ---
ENEMY_TYPE_BIKER = "biker"
ENEMY_TYPE_ENFORCER = "enforcer"
ENEMY_TYPE_FREEZER = "freezer"
ENEMY_TYPE_FLAMETHROWER = "flamethrower"
ENEMY_TYPE_SUICIDE_DRONE = "suicide_drone"
ENEMY_TYPE_UNDERBOSS = "underboss"

PLAYER_BASE_VISUAL_RANGE = 250

# --- SPEED RELATED ---
SPEED_FACTOR = 1.2
SPEED_PLAYER = 2.0 * SPEED_FACTOR
SPEED_ENEMY_NORMAL = 1.0 * SPEED_FACTOR
SPEED_ENEMY_FAST = 1.2 * SPEED_FACTOR
SPEED_ENEMY_VERY_FAST = 1.5 * SPEED_FACTOR
SPEED_ENEMY_ULTRA_FAST = 2.5 * SPEED_FACTOR

# --- ATTACK/DEFENSE/HEALTH RELATED ---
HEALTH_PLAYER = 100
ATTACK_PLAYER = 30
DEFENSE_PLAYER = 10
# enemy attack has to be higher than player base defense
HEALTH_ENEMY_VERY_WEAK, ATTACK_ENEMY_VERY_WEAK, DEFENSE_ENEMY_VERY_WEAK = 5, 2, 0
HEALTH_ENEMY_WEAK, ATTACK_ENEMY_WEAK, DEFENSE_ENEMY_WEAK = 20, 5, 1
HEALTH_ENEMY_NORMAL, ATTACK_ENEMY_NORMAL, DEFENSE_ENEMY_NORMAL = 40, 7, 2
HEALTH_ENEMY_STRONG, ATTACK_ENEMY_STRONG, DEFENSE_ENEMY_STRONG = 60, 10, 3
HEALTH_ENEMY_VERY_STRONG, ATTACK_ENEMY_VERY_STRONG, DEFENSE_ENEMY_VERY_STRONG = 100, 15, 5
HEALTH_ENEMY_SUPER_STRONG, ATTACK_ENEMY_SUPER_STRONG, DEFENSE_ENEMY_SUPER_STRONG = 200, 30, 10

HEALTH_REGEN_PLAYER = 2.0
HEALTH_REGEN_ENEMY_NORMAL = 0.0
HEALTH_REGEN_BOSS = 0.5

# --- AGGRO RELATED ---
# if player stays too close, will gain enemy's aggro
AGGRO_RANGE_FOR_ENEMY_NORMAL = 150
AGGRO_RANGE_FOR_ENEMY_SCOUT = 200
AGGRO_RANGE_FOR_ENEMY_TOWER = 250
# rally radius around the enemy being hit.
AGGRO_RANGE_FOR_HIT = 150


class BattleUnit:
    def __init__(self, health, attack, defense, speed=SPEED_ENEMY_NORMAL, color=GREEN, skills=None, health_regen=HEALTH_REGEN_ENEMY_NORMAL):
        if skills is None:
            skills = list()
        self.start_pos = None
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        # skill key start from 1 and keep adding. assuming player never loses any skill
        self.skills = {str(i+1): skill for i, skill in enumerate(skills)}
        self.health_regen = health_regen
        self.color = color
        self.effects = dict()

    def set_start_pos(self, pos):
        """
        This has to be set from after init
        :param pos:
        :return:
        """
        self.start_pos = pos

    def get_shape_size(self):
        max_possible = MIN_SHAPE_PCT + (self.max_health / (STANDARD_HEALTH * MAX_SHAPE_PCT))
        pct = MIN_SHAPE_PCT + (max_possible - MIN_SHAPE_PCT) * (self.health / self.max_health)
        return pct

    def add_effects(self, effects):
        for effect_type, effect in effects.items():
            effect_with_apply_time = copy_effects_with_apply_time(effect)
            if effect_type not in self.effects:
                print("effect {} added".format(str(effect_type)))
            else:
                print("effect {} replaced ".format(str(effect_type)))
            self.effects[effect_type] = effect_with_apply_time

    def get_speed(self):
        if EFFECT_SLOW_MOVEMENT not in self.effects:
            return self.speed

        # handle effect expiring case
        now = time.time()
        e = self.effects[EFFECT_SLOW_MOVEMENT]
        if now - e[EFFECT_KEY_APPLY_TIME] > e[EFFECT_KEY_DURATION]:
            del self.effects[EFFECT_SLOW_MOVEMENT]
            return self.speed

        # handle effect active case
        return self.speed * (1 - e[EFFECT_KEY_PERCENT] / 100)


class PlayerUnit(BattleUnit):
    def __init__(self, health=STANDARD_HEALTH, attack=ATTACK_PLAYER, defense=DEFENSE_PLAYER, speed=SPEED_PLAYER, color=ORANGE, skills=None, health_regen=HEALTH_REGEN_PLAYER):
        if skills is None:
            skills = [
                # deepcopy(skill_punch),
                # deepcopy(skill_nova),
                # deepcopy(skill_fire_ball),
                # deepcopy(skill_ice_ball),
                # deepcopy(skill_icy_blast),
                deepcopy(skill_poison_nova),
            ]
        assert len(skills) >= 1
        super().__init__(
            health=health,
            attack=attack,
            defense=defense,
            speed=speed,
            color=color,
            skills=skills,
            health_regen=health_regen
        )
        self.visual_range = PLAYER_BASE_VISUAL_RANGE
        self.left_click_skill_key = '1' # first skill is '1', corresponding to keyboard


class EnemyUnit(BattleUnit):
    def __init__(self, type, health, attack, defense, ai_mode=ENFORCER, speed=SPEED_ENEMY_NORMAL, color=GREEN, skills=None, aggro_range=AGGRO_RANGE_FOR_ENEMY_NORMAL, health_regen=0.0):
        if skills is None:
            skills = get_skill_list_by_mode(ai_mode)
        assert len(skills) >= 1
        super().__init__(
            health=health,
            attack=attack,
            defense=defense,
            speed=speed,
            color=color,
            skills=skills,
            health_regen=health_regen
        )
        self.type = type
        self.aggro_range = aggro_range
        self.left_click_skill_key = '1'
        self.ai = AI(ai_mode, self)

    def set_player(self, player):
        self.ai.set_target_unit(player)


player_sample = PlayerUnit()

enemy_biker_sample = EnemyUnit(
    type=ENEMY_TYPE_BIKER,
    health=HEALTH_ENEMY_WEAK,
    attack=ATTACK_ENEMY_WEAK,
    defense=DEFENSE_ENEMY_WEAK,
    speed=SPEED_ENEMY_VERY_FAST,
    color=GREEN
)

enemy_enforcer_sample = EnemyUnit(
    type=ENEMY_TYPE_ENFORCER,
    health=HEALTH_ENEMY_NORMAL,
    attack=ATTACK_ENEMY_NORMAL,
    defense=DEFENSE_ENEMY_STRONG,
    speed=SPEED_ENEMY_FAST,
    color=DARK_GREEN
)

enemy_freezer_sample = EnemyUnit(
    type=ENEMY_TYPE_FREEZER,
    health=HEALTH_ENEMY_NORMAL,
    attack=ATTACK_ENEMY_STRONG,
    defense=DEFENSE_ENEMY_WEAK,
    color=BLUE,
    skills=deepcopy([skill_ice_ball])
)

enemy_flamethrower_sample = EnemyUnit(
    type=ENEMY_TYPE_FLAMETHROWER,
    health=HEALTH_ENEMY_STRONG,
    attack=ATTACK_ENEMY_STRONG,
    defense=DEFENSE_ENEMY_STRONG,
    color=RED,
    skills=deepcopy([skill_fire_ball])
)

enemy_suicide_drone_sample = EnemyUnit(
    type=ENEMY_TYPE_SUICIDE_DRONE,
    health=HEALTH_ENEMY_VERY_WEAK,
    attack=ATTACK_ENEMY_SUPER_STRONG,
    defense=0,
    speed=SPEED_ENEMY_ULTRA_FAST,
    color=BLACK,
    aggro_range=AGGRO_RANGE_FOR_ENEMY_SCOUT,
    skills=deepcopy([skill_suicide_attack])
)

enemy_underboss_sample = EnemyUnit(
    type=ENEMY_TYPE_UNDERBOSS,
    health=HEALTH_ENEMY_SUPER_STRONG,
    attack=ATTACK_ENEMY_VERY_STRONG,
    defense=DEFENSE_ENEMY_VERY_STRONG,
    color=PURPLE,
    speed=SPEED_ENEMY_VERY_FAST,
    skills=deepcopy([skill_fire_ball, skill_ice_ball]),
    health_regen=HEALTH_REGEN_BOSS
)

enemy_boss_sample = EnemyUnit(
    type=ENEMY_TYPE_UNDERBOSS,
    health=HEALTH_ENEMY_SUPER_STRONG * 2,
    attack=ATTACK_ENEMY_VERY_STRONG,
    defense=DEFENSE_ENEMY_VERY_STRONG,
    color=BLACK,
    speed=SPEED_ENEMY_VERY_FAST,
    skills=deepcopy([skill_poison_dart, skill_fire_dart, skill_icy_blast, skill_fire_ring]),
    health_regen=HEALTH_REGEN_BOSS
)
