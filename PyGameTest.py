# https://www.edureka.co/blog/python-turtle-module/

import turtle, math, time, heapq
from functools import partial
from copy import deepcopy
from SkillDefinition import *
from BattleUnitDefinition import *
from Utils import *
from Constants import *


class GameView:

    def __init__(self, dim, player, enemies):

        # window setup
        self.win = turtle.Screen()
        win = self.win
        win.title("Small game")
        win.bgcolor(COLOR_BG)
        win.setup(width=dim[0], height=dim[1])
        win.tracer(0)

        # player setup
        self.player = turtle.Turtle()
        p = self.player
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
                break

            # debug starts
            if 0: #  0 == iter_count % 20:
                turtles = win.turtles()
                visible_count = 0
                for t in turtles:
                    if t.isvisible():
                        visible_count += 1
                print("total count = {}, visible turtle count = {}, missile count = {}".format(
                    str(len(turtles)),
                    str(visible_count),
                    str(len(self.missiles))
                ))
            # debug ends
            self.tick()
            if not self.enemies:
                print("You win.")
                win.ttl = time.time() + 3
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
        # print("angle = " + str(angle))
        p.prev_pos = (p.xcor(), p.ycor())
        p.goto(x, y)
        # print("[1] set p angle = " + str(moving_angle))
        if p.stop:
            p.setheading(p.shooting_angle)
        else:
            p.setheading(moving_angle)

        # enemy ai actions
        for e_id, e in self.enemies.items():
            decision = e.battle_unit_data.ai.decide()
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
            enemy_hit = find_first_collision(m, self.enemies, (x, y))
            if enemy_hit is not None:
                dead = handle_missile_damage(enemy_hit, m)
                # enemy_hit.hideturtle()
                if dead:
                    del self.enemies[enemy_hit.id]
                    print("{} is down, {} left.".format(enemy_hit.id, str(len(self.enemies))))
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
            bu_hit = find_first_collision(m, {"player": self.player}, (x, y))
            if bu_hit is not None:
                dead = handle_missile_damage(bu_hit, m)
                if dead:
                    self.player.alive = False
                    print("Player down.")
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

        player_skills = [skill_fire_ball, skill_ice_ball]
        self.player = PlayerUnit(start_pos=(0, 0), health=STANDARD_HEALTH, attack=20, defense=3, speed=1.2, skills=player_skills)

        self.enemies = []

        # 3 enemies
        self.enemies.append(EnemyUnit(start_pos=(100, 100), health=20, attack=5, defense=2, player=self.player))
        self.enemies.append(EnemyUnit(start_pos=(100, 0), health=30, attack=5, defense=3, player=self.player))
        self.enemies.append(EnemyUnit(start_pos=(100, -100), health=50, attack=7, defense=2, player=self.player))

        # 7 enemies
        # self.enemies.append(EnemyUnit(start_pos=(100, 100), health=20, attack=5, defense=2, player=self.player, speed=.5))
        # self.enemies.append(EnemyUnit(start_pos=(100, 0), health=30, attack=5, defense=3, player=self.player, speed=.55))
        # self.enemies.append(EnemyUnit(start_pos=(100, -100), health=50, attack=7, defense=2, player=self.player, speed=.6))
        # self.enemies.append(EnemyUnit(start_pos=(100, -200), health=50, attack=7, defense=2, player=self.player, speed=.65))
        # self.enemies.append(EnemyUnit(start_pos=(100, -300), health=50, attack=7, defense=2, player=self.player, speed=.7))
        # self.enemies.append(EnemyUnit(start_pos=(100, -400), health=50, attack=7, defense=2, player=self.player, speed=.75))
        # self.enemies.append(EnemyUnit(start_pos=(100, -500), health=50, attack=7, defense=2, player=self.player, speed=.8))

        self.view = GameView(self.dim, self.player, self.enemies)


game = CasualGame()