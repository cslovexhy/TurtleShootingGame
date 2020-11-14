# https://www.edureka.co/blog/python-turtle-module/

import turtle, math, time, heapq
from functools import partial
from copy import deepcopy
from SkillDefinition import *
from BattleUnitDefinition import *
from ShapeDefinition import *
from LootDefinition import *
from LevelDefinition import *
from Utils import *
from Constants import *


class GameView:

    def __init__(self, dim, level, player, enemies, walls, items):

        self.level_complete = False

        self.item_id_auto_increased = 0
        self.enemy_id_auto_increased = 0
        self.enemy_missile_id_auto_increased = 0
        self.player_missile_id_auto_increased = 0

        # window setup
        print("init 1")
        self.win = turtle.Screen()
        win = self.win
        win.title("Small game, level {}".format(str(level)))
        # learned from here: https://stackoverflow.com/questions/34687998/turtle-screen-fullscreen-on-program-startup
        win.screensize(dim[0], dim[1])
        win.setup(width=1.0, height=1.0, startx=None, starty=None)
        win.bgcolor(GRAY)
        win.tracer(0)
        if hasattr(win, "ttl"):
            delattr(win, "ttl")
        # canvas setup
        self.canvas = self.win.getcanvas()
        self.scroll_ttl = 0

        # register shapes
        register_all_shapes(win)

        # player setup
        self.player = turtle.Turtle(SHAPE_SHARK)
        p = self.player
        p.id = "player_0"
        p.alive = True
        p.speed(0)
        p.color(player.color)
        p.penup()
        self.move_player(player.start_pos[0], player.start_pos[1])
        p.prev_pos = deepcopy(player.start_pos)
        p.target_pos = deepcopy(player.start_pos)
        p.orig_pos = deepcopy(player.start_pos)
        p.last_dir = UP
        p.direction = STOP
        p.stop = True
        p.shooting_angle = 0
        p.battle_unit_data = player
        player.ui = p

        # enemy setup
        self.enemies = dict()
        for enemy_id, enemy in enumerate(enemies):
            e = turtle.Turtle(SHAPE_TURTLE)
            e.id = self.get_next_enemy_id()
            e.last_aggro = 0
            e.color(enemy.color)
            e.penup()
            e.goto(enemy.start_pos[0], enemy.start_pos[1])
            e.prev_pos = deepcopy(enemy.start_pos)
            e.target_pos = deepcopy(enemy.start_pos)
            e.orig_pos = deepcopy(enemy.start_pos)
            e.shapesize(enemy.get_shape_size())
            e.direction = STOP
            e.battle_unit_data = enemy
            enemy.ui = e
            self.enemies[e.id] = e

        # missiles setup
        self.missiles = dict()
        self.enemy_missiles = dict()

        # wall setup
        self.walls = dict()
        self.walls_cor_set = set()
        self.walls_visited = set()
        for wall_id, wall in enumerate(walls):
            w = turtle.Turtle(wall.shape)
            w.id = "wall_" + str(wall_id)
            w.color(wall.color)
            w.penup()
            w.goto(wall.pos[0], wall.pos[1])
            w.direction = STOP
            w.wall_unit_data = wall
            self.walls[w.id] = w
            self.walls_cor_set.add(wall.pos)

        # item setup
        self.items = dict()
        for item_id, item in enumerate(items):
            i = turtle.Turtle(item.shape)
            i.id = self.get_next_item_id()
            i.color(item.color)
            i.penup()
            i.goto(item.pos[0], item.pos[1])
            i.direction = STOP
            i.item_unit_data = item
            self.items[i.id] = i

        # event listener setup
        win.listen()
        win.onkey(partial(stop_moving, p), 's')
        win.onclick(self.left_click_callback)
        win.onclick(self.attack_with_right_click, 2)
        self.bind_skills()

        # main loop
        iter_count = 0
        prev = time.time()
        while True:
            win.update()
            # grace period before window shut down
            if hasattr(win, 'ttl'):
                now = time.time()
                if now < win.ttl:
                    time.sleep(win.ttl - now)
                else:
                    print("ttl expired")
                win.clear()
                break

            self.tick()
            if not self.enemies:
                print("You win.")
                win.ttl = time.time() + 3
                self.level_complete = True
            if not self.player.alive:
                print("You lose.")
                win.ttl = time.time() + 3
            time.sleep(SLEEP_INTERVAL)
            # p.direction = STOP
            now = time.time()
            if now >= prev + 1:
                update_frame(iter_count + 1)
                # print("Frame Rate: " + str(iter_count))
                iter_count = 0
                prev = now
            else:
                iter_count += 1

    def get_next_item_id(self):
        old_id = self.item_id_auto_increased
        self.item_id_auto_increased += 1
        return "item_" + str(old_id)

    def get_next_enemy_missile_id(self):
        old_id = self.enemy_missile_id_auto_increased
        self.enemy_missile_id_auto_increased += 1
        return old_id

    def get_next_player_missile_id(self):
        old_id = self.player_missile_id_auto_increased
        self.player_missile_id_auto_increased += 1
        return old_id

    def get_next_enemy_id(self):
        old_id = self.enemy_id_auto_increased
        self.enemy_id_auto_increased += 1
        return "enemy_" + str(old_id)

    def bind_skills(self):
        for key in self.player.battle_unit_data.skills:
            self.win.onkey(partial(self.select_skill, key), key)

    def select_skill(self, skill_key):
        self.player.battle_unit_data.left_click_skill_key = skill_key
        print("player selected skill {}".format(self.player.battle_unit_data.skills[skill_key].name))

    def left_click_callback(self, target_x, target_y):
        for item_id, item in self.items.items():
            cor = (item.xcor(), item.ycor())
            is_player_nearby = get_dist((self.player.xcor(), self.player.ycor()), cor) < 50
            is_click_on_item = get_dist((target_x, target_y), cor) < 30
            if is_player_nearby and is_click_on_item:
                self.pick_up_item(item_id)
                return
        # if not item pickup, left click just mean moving.
        self.move_with_left_click(target_x, target_y)

    def pick_up_item(self, item_id):
        player_data = self.player.battle_unit_data
        handle_item_pick_up(player_data, self.items[item_id].item_unit_data, self.bind_skills)
        item = self.items[item_id]
        item.hideturtle()
        del self.items[item_id]

    def move_with_left_click(self, target_x, target_y):
        p = self.player
        p.orig_pos = (p.xcor(), p.ycor())

        # use way point for player, less control and less fun
        # p.way_points = get_way_points(p.orig_pos, (target_x, target_y), self.walls_cor_set)
        # if p.way_points:
        #     p.target_pos = deepcopy(p.way_points[-1])
        #     print("target pos updated: " + str(p.target_pos))
        #     p.stop = False
        p.target_pos = (target_x, target_y)
        # print("target pos updated: " + str(p.target_pos))
        p.stop = False

    def attack_with_right_click(self, target_x, target_y):
        p = self.player
        skill = p.battle_unit_data.skills[p.battle_unit_data.left_click_skill_key]
        if isinstance(skill, SimpleNovaSkill):
            self.fire_nova(p, self.missiles)
        else:
            self.fire_missile(p, (target_x, target_y), self.missiles)

    def enemy_attack(self, attacker, target_cor):
        skill = attacker.battle_unit_data.skills[attacker.battle_unit_data.left_click_skill_key]
        if isinstance(skill, SimpleSummonSkill):
            print("skill.battle_unit.type = " + str(skill.battle_unit.type))
            return self.add_summoned_enemy(skill, target_cor)
        elif isinstance(skill, SimpleNovaSkill):
            self.fire_nova(attacker, self.enemy_missiles)
        else:
            self.fire_missile(attacker, target_cor, self.enemy_missiles)
        return []

    def add_summoned_enemy(self, skill, target_cor):

        now = time.time()
        if not skill.last_used:
            skill.last_used = now
        else:
            time_since_last_use = now - skill.last_used
            if time_since_last_use > skill.cool_down:
                skill.last_used = now
            else:
                print("{} in cool down, wait for {} seconds".format(
                    skill.name,
                    str(skill.cool_down - time_since_last_use)
                ))
                return []

        enemy_sample = skill.battle_unit
        enemy_sample.start_pos = target_cor
        new_enemies = []
        for i in range(skill.count):
            enemy = deepcopy(enemy_sample)
            enemy.set_player(self.player.battle_unit_data)
            e = turtle.Turtle(enemy.shape)
            e.last_aggro = 0
            e.color(enemy.color)
            e.penup()
            e.goto(enemy.start_pos[0], enemy.start_pos[1])
            e.prev_pos = deepcopy(enemy.start_pos)
            e.target_pos = deepcopy(enemy.start_pos)
            e.orig_pos = deepcopy(enemy.start_pos)
            e.shapesize(enemy.get_shape_size())
            e.direction = STOP
            e.battle_unit_data = enemy
            enemy.ui = e
            print("e.battle_unit_data = " + str(vars(e.battle_unit_data)))
            print("e.battle_unit_data.ui = " + str(vars(e.battle_unit_data.ui)))
            new_enemies.append(e)
        return new_enemies

    def move_player(self, x, y):
        self.player.goto(x, y)

        if not ENABLE_CANVAS_MOVING:
            return

        def get_fraction(v, total, window_size):
            min_v, max_v = total / -2, total / 2
            if v <= min_v + window_size / 2:
                return 0
            if v >= max_v - window_size / 2:
                return 1
            fraction = (v - (min_v + window_size / 2)) / total
            return fraction

        if time.time() - 0.05 < self.scroll_ttl:
            return

        scroll_fraction_x = get_fraction(x, WINDOW_X, self.win.window_width())
        scroll_fraction_y = get_fraction(y, WINDOW_Y, self.win.window_height())
        self.canvas.xview_moveto(scroll_fraction_x)
        self.canvas.yview_moveto(1 - self.win.window_height() / WINDOW_Y - scroll_fraction_y)
        self.scroll_ttl = time.time()
        # print("x = {}, window_x = {}, window_width = {}, fraction_x = {}, canvas.xview() = {}".format(x, WINDOW_X, self.win.window_width(), scroll_fraction_x, self.canvas.xview()))
        # print("y = {}, window_y = {}, window_height = {}, fraction_y = {}, canvas.yview() = {}".format(y, WINDOW_Y, self.win.window_height(), scroll_fraction_y, self.canvas.yview()))

    def tick(self):
        # move player
        p = self.player
        p.shapesize(p.battle_unit_data.get_shape_size())
        x, y, moving_angle = get_new_cors(p, get_battle_unit_base_speed() * p.battle_unit_data.get_speed(), True)
        # print("x = {}, y = {}, moving_angle = {}".format(str(x), str(y), str(moving_angle)))
        obj_hit = find_first_collision(p, self.walls, (x, y))
        if obj_hit is None:
            p.prev_pos = (p.xcor(), p.ycor())
            if p.prev_pos != (x, y):
                self.move_player(x, y)
            # print("[1] set p angle = " + str(moving_angle))
            if p.stop:
                p.setheading(p.shooting_angle)
            else:
                p.setheading(moving_angle)
            # this won't happen unless we enable path find for player in move_with_left_click
            if hasattr(p, "way_points"):
                if p.way_points:
                    if (p.xcor(), p.ycor()) == p.way_points[-1]:
                        p.way_points.pop()
                        if p.way_points:
                            p.orig_pos = (p.xcor(), p.ycor())
                            p.target_pos = deepcopy(p.way_points[-1])
                            print("target pos updated 2: " + str(p.target_pos))
        else:
            # print("player hit a wall, cannot go, pos = ({}, {}) obj = {}".format(str(p.xcor()), str(p.ycor()), str(obj_hit.wall_unit_data.pos)))
            # print("target pos 3: " + str(p.target_pos))
            # print("orig pos 3: " + str(p.orig_pos))
            p.stop = True

        # enemy ai actions
        new_enemies = []
        for e_id, e in self.enemies.items():
            if e.distance(p.xcor(), p.ycor()) <= e.battle_unit_data.aggro_range:
                e.last_aggro = time.time()
            decision = e.battle_unit_data.ai.decide(self.walls_cor_set)
            # print("decision for enemy {} is: {}".format(str(e_id), str(decision)))
            if decision['decision'] == AI_DECISION_ATTACK:
                target_cor = decision['target_cor']
                summoned_enemies = self.enemy_attack(e, target_cor)
                new_enemies.extend(summoned_enemies)
            elif decision['decision'] == AI_DECISION_MOVE:
                next_x, next_y, angle = decision['next_stop']
                e.prev_pos = (e.xcor(), e.ycor())
                e.goto(next_x, next_y)
                e.setheading(angle)

        # if summoned new enemies, need to add them here, cannot modify self.enemies while looping it.
        print("added {} new enemies".format(str(len(new_enemies))))
        for e in new_enemies:
            e.id = self.get_next_enemy_id()
            print("next id = " + str(e.id))
            self.enemies[e.id] = e

        # move player missiles
        added_missile_shards = []
        for m_id, m in self.missiles.items():
            if not m.isvisible():
                continue
            skill = m.skill_data
            dist = get_missile_base_speed() * skill.flying_speed
            x, y, _ = get_new_cors(m, dist)
            orig_x, orig_y = m.orig_pos
            dx, dy = x - orig_x, y - orig_y
            m.right(skill.spin)

            # collision on enemy or wall
            obj_hit = find_first_collision(m, combine_map(self.enemies, self.walls), (x, y))
            if obj_hit is not None:
                if "enemy_" in obj_hit.id:
                    print("hit enemy")
                    enemy_hit = obj_hit
                    dead = handle_missile_damage(enemy_hit, m)
                    missile_shards = trigger_splash(p, enemy_hit, m)
                    if missile_shards:
                        added_missile_shards.extend(missile_shards)
                    aggro_list = get_units_within_range(self.enemies, (enemy_hit.xcor(), enemy_hit.ycor()), AGGRO_RANGE_FOR_HIT)
                    for unit in aggro_list:
                        unit.last_aggro = time.time()
                    if dead:
                        self.handle_dead_enemy(enemy_hit)
                elif "wall_" in obj_hit.id:
                    # print("hit wall")
                    wall_hit = obj_hit
                    dead = handle_missile_damage_on_wall(wall_hit, m)
                    if dead:
                        self.walls_cor_set.remove(self.walls[wall_hit.id].wall_unit_data.pos)
                        del self.walls[wall_hit.id]
                        print("{} is down.".format(wall_hit.id))
                m.ttl = 0
            elif math.sqrt(dx * dx + dy * dy) >= skill.attack_range:
                m.ttl = 0

            m.goto(x, y)

        for m in added_missile_shards:
            m_id = "missile_" + str(len(self.missiles))
            m.id = m_id
            self.missiles[m_id] = m

        # move enemy missiles
        for m_id, m in self.enemy_missiles.items():
            if not m.isvisible():
                continue
            skill = m.skill_data
            dist = get_missile_base_speed() * skill.flying_speed
            x, y, _ = get_new_cors(m, dist)
            orig_x, orig_y = m.orig_pos
            dx, dy = x - orig_x, y - orig_y
            m.right(skill.spin)

            # collision on enemy or wall, TODO: wall
            obj_hit = find_first_collision(m, combine_map({p.id: p}, self.walls), (x, y))
            if obj_hit is not None:
                if "player_" in obj_hit.id:
                    print("hit player")
                    player_hit = obj_hit
                    dead = handle_missile_damage(player_hit, m)
                    if dead:
                        self.handle_dead_player()
                    if hasattr(skill, "health_burn"):
                        dead = handle_missile_damage(m.owner, m)
                        if dead:
                            if m.owner.id in self.enemies:
                                del self.enemies[m.owner.id]
                            else:
                                print("killed before suicide could happen")
                elif "wall_" in obj_hit.id:
                    # print("hit wall")
                    wall_hit = obj_hit
                    dead = handle_missile_damage_on_wall(wall_hit, m)
                    if dead:
                        self.walls_cor_set.remove(self.walls[wall_hit.id].wall_unit_data.pos)
                        del self.walls[wall_hit.id]
                        print("{} is down.".format(wall_hit.id))

                m.ttl = 0
            elif math.sqrt(dx * dx + dy * dy) >= skill.attack_range:
                m.ttl = 0

            m.goto(x, y)

        # why do we need another loop to hide/delete? coz it's not good to delete the iterable while looping through it.
        now = time.time()

        def handle_missile_visibility(missiles):
            to_remove_set = set()
            # print("missile count = " + str(len(missiles)))
            for m_id, m in missiles.items():
                # print("m_id = {}, now = {}, ttl = {}".format(m_id, str(now), str(m.ttl)))
                if not m.isvisible() or now < m.ttl:
                    continue
                # print("hiding missile id=" + str(m_id))
                # move this thing out of the screen
                m.setx(WINDOW_X)
                m.sety(WINDOW_Y)
                m.hideturtle()
                to_remove_set.add(m_id)

            for m_id in to_remove_set:
                del missiles[m_id]

        handle_missile_visibility(self.missiles)
        handle_missile_visibility(self.enemy_missiles)

        # handle player visibility
        self.update_visibility()

        # handle health regen
        if self.player.alive:
            if handle_effect_damage(self.player):
                self.handle_dead_player()
        if self.player.alive:
            handle_health_regen(self.player)

        dead_enemy_ids = set()
        for e_id, e in self.enemies.items():
            if handle_effect_damage(e):
                dead_enemy_ids.add(e_id)
            else:
                handle_health_regen(e)

        for e_id in dead_enemy_ids:
            self.handle_dead_enemy(self.enemies[e_id])

    def add_item_to_screen(self, item, cor):
        if item is None:
            return
        i = turtle.Turtle(item.shape)
        i.id = self.get_next_item_id()
        i.color(item.color)
        i.penup()
        i.goto(cor[0], cor[1])
        i.direction = STOP
        i.item_unit_data = item
        self.items[i.id] = i
        print("item added, total item count = " + str(len(self.items)))

    def update_visibility(self):
        if not ENABLE_WAR_MIST:
            return

        def too_close(cor, radius):
            for c in centers:
                if get_dist(cor, c) <= radius:
                    return True
            return False

        centers = [(self.player.xcor(), self.player.ycor())]
        p_radius = self.player.battle_unit_data.visual_range
        # TODO: have different visual range for player's missiles
        # for _, m in self.missiles.items():
        #     centers.append((m.xcor(), m.ycor()))

        for _, e in self.enemies.items():
            if too_close((e.xcor(), e.ycor()), p_radius):
                e.showturtle()
            else:
                e.hideturtle()

        for _, w in self.walls.items():
            cor = (w.xcor(), w.ycor())
            if too_close(cor, p_radius):
                w.color(w.wall_unit_data.color)
                w.showturtle()
                self.walls_visited.add(cor)
            else:
                if cor in self.walls_visited:
                    w.color(w.wall_unit_data.color_dim)
                else:
                    w.hideturtle()

    def fire_missile(self, attacker, target_cor, missile_list, ignore_cool_down=False):
        p = attacker
        skill = p.battle_unit_data.skills[p.battle_unit_data.left_click_skill_key]
        target_x, target_y = target_cor
        x, y = p.xcor(), p.ycor()
        if target_x == x and target_y == y:
            print("need some angle to attack, skip")
            return False
        angle = to_int_degree(get_angle_for_vector((x, y), (target_x, target_y)))
        p.target_pos = (x, y)
        p.stop = True
        p.shooting_angle = angle

        now = time.time()
        if not ignore_cool_down:
            if not skill.last_used:
                skill.last_used = now
            else:
                time_since_last_use = now - skill.last_used
                if time_since_last_use > skill.cool_down:
                    skill.last_used = now
                else:
                    print("{} in cool down, wait for {} seconds".format(
                        skill.name,
                        str(skill.cool_down - time_since_last_use)
                    ))
                    return False

        missile = turtle.Turtle()
        m = missile
        m.penup()
        if p == self.player:
            m.id = self.get_next_player_missile_id()
        else:
            m.id = self.get_next_enemy_missile_id()
        m.shape(skill.shape)
        m.color(skill.color)
        m.goto(x, y)
        m.orig_pos = (x, y)
        m.target_pos = (target_x, target_y)
        m.shapesize(0.5)
        m.skill_data = skill
        m.owner = p

        speed_per_sec = get_missile_base_speed() * FRAME * skill.flying_speed
        max_flying_time = skill.attack_range / speed_per_sec
        # print("speed_per_sec = " + str(speed_per_sec) + ", max_flying_time = " + str(max_flying_time))
        m.ttl = now + max_flying_time

        missile_list[m.id] = m

        return True

    def handle_dead_enemy(self, enemy_hit):
        # if enemy killed by player's damage, enter loot dropping logic
        loot_item = handle_loot_dropping(enemy_hit.battle_unit_data)
        self.add_item_to_screen(loot_item, (enemy_hit.xcor(), enemy_hit.ycor()))
        del self.enemies[enemy_hit.id]
        print("{} is down, {} left.".format(enemy_hit.id, str(len(self.enemies))))

    def handle_dead_player(self):
        self.player.alive = False
        print("Player down.")

    # so far only player can fire this, TODO: allow enemy do this too
    def fire_nova(self, attacker, missile_list):
        # here i'm only copying 1 skill for all missiles, hope nothing bad happens.
        skill = deepcopy(attacker.battle_unit_data.skills[attacker.battle_unit_data.left_click_skill_key])
        shard_count = skill.shard_count
        print("shard_count = " + str(shard_count))
        center = (attacker.xcor(), attacker.ycor())
        for i in range(shard_count):
            radius = skill.attack_range
            angle = to_radian(int(360 / shard_count * i))
            dest_x = center[0] + math.cos(angle) * radius
            dest_y = center[1] + math.sin(angle) * radius
            dest = (dest_x, dest_y)
            # print("dest = " + str(dest))
            ignore_cool_down = i != 0
            can_fire = self.fire_missile(attacker, dest, missile_list, ignore_cool_down)
            if not can_fire:
                print("nova in cool down")
                return


class CasualGame:

    def __init__(self):
        self.dim = (WINDOW_X, WINDOW_Y)

        for level in range(START_LEVEL, MAX_LEVEL+1):
            self.player, self.enemies, self.walls, self.items = get_units_by_level(level)
            print("Initiating level {}".format(str(level)))
            self.view = GameView(self.dim, level, self.player, self.enemies, self.walls, self.items)
            if not self.view.level_complete:
                print("level {} failed, game over.".format(str(level)))
                break
            else:
                print("level {} is complete".format(str(level)))


game = CasualGame()
