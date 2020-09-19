# https://www.edureka.co/blog/python-turtle-module/

import turtle, math, time, heapq
from functools import partial

WINDOW_X, WINDOW_Y = 800, 600
FRAME = 24
SLEEP_INTERVAL = 1 / FRAME
COLOR_BG = (.8, .8, .8)  # gray
COLOR_PLAYER = (1, 0, 0)  # red
COLOR_ENEMY = (0, 1, 0)
UP, DOWN, RIGHT, LEFT, STOP = "up", "down", "right", "left", "stop"
BATTLE_UNIT_BASE_SPEED = 50 / FRAME      # 50 pixel per second
MISSILE_BASE_SPEED = 200 / FRAME    # 200 pixel per second
ENFORCER = "ENFORCER"
SNIPER = "SNIPER"

AI_DECISION_MOVE = "AI_DECISION_MOVE"


class BattleUnit:
    def __init__(self, start_pos, health, attack, defense, speed=1.0, skills=None):
        if skills is None:
            skills = list()
        self.start_pos = start_pos
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.skills = {skill.key: skill for skill in skills}


class PlayerUnit(BattleUnit):
    def __init__(self, start_pos, health, attack, defense, speed=1.2, skills=None):
        assert len(skills) >= 2
        super().__init__(start_pos, health, attack, defense, speed, skills)
        self.left_click_skill_key = skills[0].key
        self.right_click_skill_key = skills[1].key


class EnemyUnit(BattleUnit):
    def __init__(self, start_pos, health, attack, defense, player, ai_mode=ENFORCER, speed=.5, skills=None):
        super().__init__(start_pos, health, attack, defense, speed, skills)
        self.ai = AI(ai_mode, self, player)


class Skill:
    def __init__(self, name, key, cool_down):
        self.name = name
        self.key = key
        self.cool_down = cool_down
        self.last_used = 0


class SimpleRangedSkill(Skill):
    # conversion means how much % of attack goes into damage
    def __init__(self, name, key, attack_range, flying_speed, conversion, cool_down, shape, color):
        super().__init__(name, key, cool_down)
        self.flying_speed = flying_speed
        self.attack_range = attack_range
        self.conversion = conversion
        self.shape = shape
        self.color = color


class AI:
    def __init__(self, ai_mode, battle_unit, target_unit):
        self.ai_mode = ai_mode
        self.battle_unit = battle_unit
        self.target_unit = target_unit

    def decide(self):
        if self.ai_mode == ENFORCER:
            t = self.target_unit.ui
            tx, ty = t.xcor(), t.ycor()
            b = self.battle_unit.ui
            bx, by = b.xcor(), b.ycor()
            max_step = BATTLE_UNIT_BASE_SPEED * self.battle_unit.speed

            step_x, step_y = 0, 0
            # move horizontally
            if abs(bx - tx) > abs(by - ty):
                if bx > tx:
                    step_x = -min(bx - tx, max_step)
                else:
                    step_x = min(tx - bx, max_step)
            # move vertically
            else:
                if by > ty:
                    step_y = -min(by - ty, max_step)
                else:
                    step_y = min(ty - by, max_step)

            return {"decision": AI_DECISION_MOVE, "step": (step_x, step_y)}
        else:
            raise Exception("ai_mode {} is not supported yet".format(self.ai_mode))


def get_new_cors_4way(t, dist):
    x, y = t.xcor(), t.ycor()
    if t.direction == UP:
        y += dist
    if t.direction == DOWN:
        y -= dist
    if t.direction == RIGHT:
        x += dist
    if t.direction == LEFT:
        x -= dist
    return x, y


def get_new_cors(t, dist):
    if not hasattr(t, "target_pos"):
        return get_new_cors_4way(t, dist)
    else:
        # orig missile pos and target missile pos decides the direction, has nothing to do with current missile pos
        ox, oy = t.orig_pos
        tx, ty = t.target_pos

        dx, dy = tx - ox, ty - oy
        r = math.sqrt(dx * dx + dy * dy)
        theta_cos = math.acos(dx / r)
        theta_sin = math.asin(dy / r)

        dx = dist * math.cos(theta_cos)
        dy = dist * math.sin(theta_sin)

        return t.xcor() + dx, t.ycor() + dy


def go_four_ways(t, direction):
    # t.last_dir = t.direction = direction
    if t.direction == STOP:
        if t.last_dir == direction:
            t.direction = direction
        else:
            t.last_dir = direction
    else:
        t.last_dir = t.direction = direction


def stop_moving(t):
    t.direction = STOP


def get_dist(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


def get_dist_dot_to_line(dot, line_dot_1, line_dot_2):
    # get a, b, c in ax + by + c = 0 first
    x1, y1 = line_dot_1
    x2, y2 = line_dot_2
    if x1 == x2:
        a, b, c = 0, 1, -y1
    elif y1 == y2:
        a, b, c = 1, 0, -x1
    else:
        # y = kx + z =>
        # kx - y + b = 0 =>
        # a = k = (y2-y1)/(x2-x1)
        # b = -1,
        # c = z = y - kx = y1 - k * x1 = y1 - a * x1
        a, b = (y2-y1)/(x2-x1), -1
        c = y1 - a * x1

    # use dot to line formula
    x0, y0 = dot
    dist = abs((a * x0 + b * y0 + c) / math.sqrt(a * a + b * b))

    print("dist from ({}, {}) to line ({}, {}) - ({}, {}) = {}".format(str(x0), str(y0), str(x1), str(y1), str(x2), str(y2), str(dist)))
    return dist


def find_first_collision(moving_obj, potential_target_map, new_cors):
    target_min_heap = []
    for t_id, t in potential_target_map.items():
        dist = t.distance(moving_obj.xcor(), moving_obj.ycor())
        heapq.heappush(target_min_heap, (dist, t_id))

    ox, oy = moving_obj.xcor(), moving_obj.ycor()
    nx, ny = new_cors
    while target_min_heap:
        dist, t_id = heapq.heappop(target_min_heap)
        t = potential_target_map[t_id]
        min_collision_dist = ((20.0 * (t._stretchfactor[0] + moving_obj._stretchfactor[0]) / 2) + (20.0 * (t._stretchfactor[1] + moving_obj._stretchfactor[1]) / 2)) / 2

        c = get_dist((ox, oy), (nx, ny))
        # if missile collides with enemy's current position, count as valid collision
        tx, ty = t.xcor(), t.ycor()
        a = get_dist((tx, ty), (ox, oy))
        b = get_dist((tx, ty), (nx, ny))
        # here need to make sure dot to line dist (line) falls on the line segment
        # this is guaranteed by making sure angles from both ends of the line segment < 90 degrees
        aa, bb, cc = a * a, b * b, c * c
        if cc + aa > bb and cc + bb > aa and get_dist_dot_to_line((tx, ty), (ox, oy), (nx, ny)) <= min_collision_dist:
            return t

        # if missile collides with enemy's prev position, also count as valid collision
        tx, ty = t.prev_pos
        a = get_dist((tx, ty), (ox, oy))
        b = get_dist((tx, ty), (nx, ny))
        aa, bb, cc = a * a, b * b, c * c
        if cc + aa > bb and cc + bb > aa and get_dist_dot_to_line((tx, ty), (ox, oy), (nx, ny)) <= min_collision_dist:
            return t

    return None


def find_first_collision_old(moving_obj, potential_target_map, new_cors):
    target_min_heap = []
    for t_id, t in potential_target_map.items():
        dist = t.distance(moving_obj.xcor(), moving_obj.ycor())
        heapq.heappush(target_min_heap, (dist, t_id))

    ox, oy = moving_obj.xcor(), moving_obj.ycor()
    nx, ny = new_cors
    while target_min_heap:
        dist, t_id = heapq.heappop(target_min_heap)
        t = potential_target_map[t_id]
        tx, ty = t.xcor(), t.ycor()
        # if missile collides with enemy's current position, count as valid collision
        if ox == nx and min(oy, ny) <= ty <= max(oy, ny) and abs(ox - tx) <= 20.0 * (t._stretchfactor[0] + moving_obj._stretchfactor[0]) / 2:
            return t
        elif oy == ny and min(ox, nx) <= tx <= max(ox, nx) and abs(oy - ty) <= 20.0 * (t._stretchfactor[1] + moving_obj._stretchfactor[1]) / 2:
            return t
        # if missile collides with enemy's prev position, also count as valid collision
        tx, ty = t.prev_pos
        if ox == nx and min(oy, ny) <= ty <= max(oy, ny) and abs(ox - tx) <= 20.0 * (t._stretchfactor[0] + moving_obj._stretchfactor[0]) / 2:
            return t
        elif oy == ny and min(ox, nx) <= tx <= max(ox, nx) and abs(oy - ty) <= 20.0 * (t._stretchfactor[1] + moving_obj._stretchfactor[1]) / 2:
            return t

    return None


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
        p.speed(0)
        p.shape("square")
        p.color(COLOR_PLAYER)
        p.penup()
        p.goto(player.start_pos[0], player.start_pos[1])
        p.prev_pos = player.start_pos
        p.last_dir = UP
        p.direction = STOP
        p.player_data = player
        player.ui = p

        # enemy setup
        self.enemies = dict()
        for enemy_id, enemy in enumerate(enemies):
            e = turtle.Turtle()
            e.id = "enemy_" + str(enemy_id)
            e.shape("square")
            e.color(COLOR_ENEMY)
            e.penup()
            e.goto(enemy.start_pos[0], enemy.start_pos[1])
            e.prev_pos = enemy.start_pos
            e.shapesize(enemy.health / player.max_health)
            e.direction = STOP
            e.enemy_data = enemy
            enemy.ui = e
            self.enemies[e.id] = e

        # missiles setup
        self.missiles = dict()

        # event listener setup
        win.listen()
        win.onkey(partial(go_four_ways, p, UP), "w")
        win.onkey(partial(go_four_ways, p, DOWN), "s")
        win.onkey(partial(go_four_ways, p, RIGHT), "d")
        win.onkey(partial(go_four_ways, p, LEFT), "a")
        win.onkey(partial(stop_moving, p), "z")
        win.onclick(self.attack_with_left_click)
        for key in p.player_data.skills:
            win.onkey(partial(self.select_skill, key), key)

        # main loop
        iter_count = 0
        while True:
            win.update()
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
            time.sleep(SLEEP_INTERVAL)
            # p.direction = STOP
            iter_count += 1

    def select_skill(self, skill_key):
        self.player.player_data.left_click_skill_key = skill_key

    def attack_with_left_click(self, target_x, target_y):
        p = self.player
        x, y = p.xcor(), p.ycor()
        if target_x == x and target_y == y:
            print("need some angle to attack, skip")
            return

        skill = p.player_data.skills[p.player_data.left_click_skill_key]
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
                return

        missile = turtle.Turtle()
        m = missile
        m.penup()
        m.id = "missile_" + str(len(self.missiles))
        m.shape(skill.shape)
        m.color(skill.color)
        m.goto(x, y)
        m.orig_pos = (x, y)
        m.target_pos = (target_x, target_y)
        m.shapesize(0.5)
        m.skill_data = skill

        speed_per_sec = MISSILE_BASE_SPEED * FRAME * skill.flying_speed
        max_flying_time = skill.attack_range / speed_per_sec
        # print("speed_per_sec = " + str(speed_per_sec) + ", max_flying_time = " + str(max_flying_time))
        m.ttl = now + max_flying_time

        self.missiles[m.id] = m

    def tick(self):
        # move player
        p = self.player
        x, y = get_new_cors(p, BATTLE_UNIT_BASE_SPEED * p.player_data.speed)
        p.prev_pos = (p.xcor(), p.ycor())
        p.setx(x)
        p.sety(y)

        # enemy ai actions
        for e_id, e in self.enemies.items():
            decision = e.enemy_data.ai.decide()
            if decision['decision'] == AI_DECISION_MOVE:
                step_x, step_y = decision['step']
                orig_x, orig_y = e.xcor(), e.ycor()
                e.prev_pos = (orig_x, orig_y)
                e.setx(orig_x + step_x)
                e.sety(orig_y + step_y)

        # move missiles
        for m_id in self.missiles:
            # print("[tick] checking missile: " + m_id)
            m = self.missiles[m_id]
            skill = m.skill_data
            dist = MISSILE_BASE_SPEED * skill.flying_speed
            x, y = get_new_cors(m, dist)
            orig_x, orig_y = m.orig_pos
            dx, dy = x - orig_x, y - orig_y

            # collision on enemy or wall, TODO: wall
            enemy_hit = find_first_collision(m, self.enemies, (x, y))
            if enemy_hit is not None:
                # TODO: do damage, not instant kill
                enemy_hit.hideturtle()
                del self.enemies[enemy_hit.id]
                print("{} is down, {} left.".format(enemy_hit.id, str(len(self.enemies))))
                m.ttl = 0
            elif math.sqrt(dx * dx + dy * dy) >= skill.attack_range:
                m.ttl = 0

            m.setx(x)
            m.sety(y)

        # why do we need another loop to hide/delete? coz it's not good to delete the iterable while looping through it.
        now = time.time()

        # TODO: here somehow if we hide missile, it stays on the screen sometimes.
        # and we have to loop through all expired missiles to keep hiding them if not.
        # this makes processing time increase somewhat linearly over missile generated historically.
        for m_id, m in self.missiles.items():
            # print("m_id = {}, now = {}, ttl = {}".format(m_id, str(now), str(m.ttl)))
            if not m.isvisible() or now < m.ttl:
                continue
            print("hiding missile id=" + str(m_id))
            # move this thing out of the screen
            m.setx(WINDOW_X)
            m.sety(WINDOW_Y)
            m.hideturtle()


class CasualGame:

    def __init__(self):
        self.dim = (WINDOW_X, WINDOW_Y)

        skill_fire_ball = SimpleRangedSkill(
            name="Fire Ball",
            key='1',
            attack_range=200,
            flying_speed=1,
            conversion=0.7,
            cool_down=0.3,
            shape="circle",
            color="red"
        )
        skill_ice_ball = SimpleRangedSkill(
            name="Ice Ball",
            key='2',
            attack_range=300,
            flying_speed=0.8,
            conversion=0.5,
            cool_down=1,
            shape="circle",
            color="blue"
        )
        player_skills = [skill_fire_ball, skill_ice_ball]
        self.player = PlayerUnit(start_pos=(0, 0), health=100, attack=10, defense=3, speed=1.2, skills=player_skills)

        self.enemies = []

        # 3 enemies
        # self.enemies.append(EnemyUnit(start_pos=(100, 100), health=20, attack=5, defense=2, player=self.player))
        # self.enemies.append(EnemyUnit(start_pos=(100, 0), health=30, attack=5, defense=3, player=self.player))
        # self.enemies.append(EnemyUnit(start_pos=(100, -100), health=50, attack=7, defense=2, player=self.player))

        # 7 enemies
        self.enemies.append(EnemyUnit(start_pos=(100, 100), health=20, attack=5, defense=2, player=self.player))
        self.enemies.append(EnemyUnit(start_pos=(100, 0), health=30, attack=5, defense=3, player=self.player))
        self.enemies.append(EnemyUnit(start_pos=(100, -100), health=50, attack=7, defense=2, player=self.player))
        self.enemies.append(EnemyUnit(start_pos=(100, -200), health=50, attack=7, defense=2, player=self.player))
        self.enemies.append(EnemyUnit(start_pos=(100, -300), health=50, attack=7, defense=2, player=self.player))
        self.enemies.append(EnemyUnit(start_pos=(100, -400), health=50, attack=7, defense=2, player=self.player))
        self.enemies.append(EnemyUnit(start_pos=(100, -500), health=50, attack=7, defense=2, player=self.player))

        self.view = GameView(self.dim, self.player, self.enemies)


game = CasualGame()