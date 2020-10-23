# https://www.edureka.co/blog/python-turtle-module/

import turtle, math, time, heapq
from functools import partial
from copy import deepcopy
from SkillDefinition import *
from BattleUnitDefinition import *
from LevelDefinition import *
from Utils import *
from Constants import *


class GameView:

    def __init__(self, dim, level, player, enemies, walls):

        self.level_complete = False

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

        # player setup
        self.player = turtle.Turtle()
        p = self.player
        p.id = "player_0"
        p.alive = True
        p.speed(0)
        p.shape("turtle")
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
            e = turtle.Turtle()
            e.id = "enemy_" + str(enemy_id)
            e.aggro = False
            e.shape("turtle")
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
        for wall_id, wall in enumerate(walls):
            w = turtle.Turtle()
            w.id = "wall_" + str(wall_id)
            w.shape(wall.shape)
            w.color(wall.color)
            w.penup()
            w.goto(wall.pos[0], wall.pos[1])
            w.direction = STOP
            w.wall_unit_data = wall
            self.walls[w.id] = w
            self.walls_cor_set.add(wall.pos)

        # event listener setup
        win.listen()
        win.onkey(partial(stop_moving, p), 's')
        win.onclick(self.move_with_left_click)
        win.onclick(self.attack_with_right_click, 2)
        for key in p.battle_unit_data.skills:
            win.onkey(partial(self.select_skill, key), key)

        # main loop
        iter_count = 0
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
            iter_count += 1

    def select_skill(self, skill_key):
        self.player.battle_unit_data.left_click_skill_key = skill_key

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
        print("target pos updated: " + str(p.target_pos))
        p.stop = False

    def attack_with_right_click(self, target_x, target_y):
        p = self.player
        fire_missile(p, (target_x, target_y), self.missiles)

    def enemy_attack(self, attacker, target_cor):
        return fire_missile(attacker, target_cor, self.enemy_missiles)

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
        x, y, moving_angle = get_new_cors(p, BATTLE_UNIT_BASE_SPEED * p.battle_unit_data.get_speed(), True)
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
        for e_id, e in self.enemies.items():
            if not e.aggro:
                e.aggro = e.distance(p.xcor(), p.ycor()) <= e.battle_unit_data.aggro_range
                continue
            decision = e.battle_unit_data.ai.decide(self.walls_cor_set)
            # print("decision for enemy {} is: {}".format(str(e_id), str(decision)))
            if decision['decision'] == AI_DECISION_ATTACK:
                target_cor = decision['target_cor']
                self.enemy_attack(e, target_cor)
            elif decision['decision'] == AI_DECISION_MOVE:
                next_x, next_y, angle = decision['next_stop']
                e.prev_pos = (e.xcor(), e.ycor())
                e.goto(next_x, next_y)
                e.setheading(angle)

        # move player missiles
        added_missile_shards = []
        for m_id, m in self.missiles.items():
            if not m.isvisible():
                continue
            skill = m.skill_data
            dist = MISSILE_BASE_SPEED * skill.flying_speed
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
                        unit.aggro = True
                    if dead:
                        del self.enemies[enemy_hit.id]
                        print("{} is down, {} left.".format(enemy_hit.id, str(len(self.enemies))))
                elif "wall_" in obj_hit.id:
                    print("hit wall")
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
            dist = MISSILE_BASE_SPEED * skill.flying_speed
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
                        self.player.alive = False
                        print("Player down.")
                    if hasattr(skill, "health_burn"):
                        dead = handle_missile_damage(m.owner, m)
                        if dead:
                            del self.enemies[m.owner.id]
                elif "wall_" in obj_hit.id:
                    print("hit wall")
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

        # TODO: here somehow if we hide missile, it stays on the screen sometimes.
        # and we have to loop through all expired missiles to keep hiding them if not.
        # this makes processing time increase somewhat linearly over missile generated historically.
        def handle_missile_visibility(missiles):
            for m_id, m in missiles.items():
                # print("m_id = {}, now = {}, ttl = {}".format(m_id, str(now), str(m.ttl)))
                if not m.isvisible() or now < m.ttl:
                    continue
                # print("hiding missile id=" + str(m_id))
                # move this thing out of the screen
                m.setx(WINDOW_X)
                m.sety(WINDOW_Y)
                m.hideturtle()

        handle_missile_visibility(self.missiles)
        handle_missile_visibility(self.enemy_missiles)

        # handle health regen
        if self.player.alive:
            handle_health_regen(self.player)
        for e_id, e in self.enemies.items():
            handle_health_regen(e)


class CasualGame:

    def __init__(self):
        self.dim = (WINDOW_X, WINDOW_Y)

        for level in range(START_LEVEL, MAX_LEVEL+1):
            self.player, self.enemies, self.walls = get_units_by_level(level)
            print("Initiating level {}".format(str(level)))
            self.view = GameView(self.dim, level, self.player, self.enemies, self.walls)
            if not self.view.level_complete:
                print("level {} failed, game over.".format(str(level)))
                break
            else:
                print("level {} is complete".format(str(level)))


game = CasualGame()
