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
        win.bgcolor(COLOR_BG)
        win.setup(width=dim[0], height=dim[1])
        win.tracer(0)
        if hasattr(win, "ttl"):
            delattr(win, "ttl")

        # player setup
        self.player = turtle.Turtle()
        p = self.player
        p.id = "player_0"
        p.alive = True
        p.speed(0)
        p.shape("turtle")
        p.color(COLOR_PLAYER)
        p.penup()
        p.goto(player.start_pos[0], player.start_pos[1])
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
            e.shape("turtle")
            e.color(COLOR_ENEMY)
            e.penup()
            e.goto(enemy.start_pos[0], enemy.start_pos[1])
            e.prev_pos = deepcopy(enemy.start_pos)
            e.target_pos = deepcopy(enemy.start_pos)
            e.orig_pos = deepcopy(enemy.start_pos)
            e.shapesize(get_shape_size(enemy.health))
            e.direction = STOP
            e.battle_unit_data = enemy
            enemy.ui = e
            self.enemies[e.id] = e

        # missiles setup
        self.missiles = dict()
        self.enemy_missiles = dict()

        # wall setup
        self.walls = dict()
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
        p.target_pos = (target_x, target_y)
        p.stop = False

    def attack_with_right_click(self, target_x, target_y):
        p = self.player
        fire_missile(p, (target_x, target_y), self.missiles)

    def enemy_attack(self, attacker, target_cor):
        return fire_missile(attacker, target_cor, self.enemy_missiles)

    def tick(self):
        # move player
        p = self.player
        x, y, moving_angle = get_new_cors(p, BATTLE_UNIT_BASE_SPEED * p.battle_unit_data.speed, True)
        obj_hit = find_first_collision(p, self.walls, (x, y))
        if obj_hit is None:
            p.prev_pos = (p.xcor(), p.ycor())
            p.goto(x, y)
            # print("[1] set p angle = " + str(moving_angle))
            if p.stop:
                p.setheading(p.shooting_angle)
            else:
                p.setheading(moving_angle)
        else:
            # print("player hit a wall, cannot go")
            p.stop = True

        # enemy ai actions
        for e_id, e in self.enemies.items():
            decision = e.battle_unit_data.ai.decide()
            # print("decision for enemy {} is: {}".format(str(e_id), str(decision)))
            if decision['decision'] == AI_DECISION_ATTACK:
                target_cor = decision['target_cor']
                self.enemy_attack(e, target_cor)
            elif decision['decision'] == AI_DECISION_MOVE:
                next_x, next_y, angle = decision['next_stop']
                obj_hit = find_first_collision(e, self.walls, (next_x, next_y))
                if obj_hit is None:
                    e.prev_pos = (e.xcor(), e.ycor())
                    e.goto(next_x, next_y)
                    e.setheading(angle)
                else:
                    # enemy hit a wall
                    pass

        # move player missiles
        for m_id, m in self.missiles.items():
            if not m.isvisible():
                continue
            skill = m.skill_data
            dist = MISSILE_BASE_SPEED * skill.flying_speed
            x, y, _ = get_new_cors(m, dist)
            orig_x, orig_y = m.orig_pos
            dx, dy = x - orig_x, y - orig_y
            m.right(skill.spin)

            # collision on enemy or wall, TODO: wall
            obj_hit = find_first_collision(m, combine_map(self.enemies, self.walls), (x, y))
            if obj_hit is not None:
                if "enemy_" in obj_hit.id:
                    print("hit enemy")
                    enemy_hit = obj_hit
                    dead = handle_missile_damage(enemy_hit, m)
                    if dead:
                        del self.enemies[enemy_hit.id]
                        print("{} is down, {} left.".format(enemy_hit.id, str(len(self.enemies))))
                elif "wall_" in obj_hit.id:
                    print("hit wall")
                    wall_hit = obj_hit
                    dead = handle_missile_damage_on_wall(wall_hit, m)
                    if dead:
                        del self.walls[wall_hit.id]
                        print("{} is down.".format(wall_hit.id))
                m.ttl = 0
            elif math.sqrt(dx * dx + dy * dy) >= skill.attack_range:
                m.ttl = 0

            m.goto(x, y)

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
                elif "wall_" in obj_hit.id:
                    print("hit wall")
                    wall_hit = obj_hit
                    dead = handle_missile_damage_on_wall(wall_hit, m)
                    if dead:
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
                print("hiding missile id=" + str(m_id))
                # move this thing out of the screen
                m.setx(WINDOW_X)
                m.sety(WINDOW_Y)
                m.hideturtle()

        handle_missile_visibility(self.missiles)
        handle_missile_visibility(self.enemy_missiles)


class CasualGame:

    def __init__(self):
        self.dim = (WINDOW_X, WINDOW_Y)

        for level in range(MIN_LEVEL, MAX_LEVEL+1):
            self.player = get_player_by_level(level)
            self.enemies = get_enemies_by_level(level, self.player)
            self.walls = get_walls_by_level(level)
            print("Initiating level {}".format(str(level)))
            self.view = GameView(self.dim, level, self.player, self.enemies, self.walls)
            if not self.view.level_complete:
                print("level {} failed, game over.".format(str(level)))
                break
            else:
                print("level {} is complete".format(str(level)))


game = CasualGame()
