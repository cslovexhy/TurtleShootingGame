import math, time, heapq, random
import turtle
from Constants import *
from SkillDefinition import *


def rand_f(f1, f2):
    """
    :param f1: start floating num, max precision is 4, e.g. 1.0001
    :param f2: end floating num, same precision
    :return: a random float number within [f1, f2]
    """
    assert(f1 <= f2)
    f1 *= 10000
    f2 *= 10000
    return random.randint(int(f1), int(f2)) / 10000


def to_int_degree(theta):
    return int(theta / math.pi * 180)


def get_angle_for_vector(o, t):
    ox, oy = o
    tx, ty = t
    dx, dy = tx - ox, ty - oy
    r = math.sqrt(dx * dx + dy * dy)
    theta_cos = math.acos(dx / r)
    theta = abs(theta_cos) if ty >= oy else -abs(theta_cos)
    return theta


def get_new_cors(t, dist, hard_stop=False):
    # t: moving turtle
    # dist: max stride can take
    # hard_stop: should stop at .target_pos or can move a little further
    assert hasattr(t, "target_pos")
    assert hasattr(t, "orig_pos")

    if t.target_pos == t.orig_pos:
        return t.orig_pos[0], t.orig_pos[1], t.heading()

    # orig turtle pos and target turtle pos decides the direction, has nothing to do with current turtle pos
    ox, oy = t.orig_pos
    tx, ty = t.target_pos
    cx, cy = t.xcor(), t.ycor()

    if hard_stop:
        # For player moving, if we are closer to target than 1 max step,
        # just go there directly, no more calculation needed
        c2t_dist = get_dist((cx, cy), (tx, ty))
        theta = get_angle_for_vector((ox, oy), (tx, ty))
        if c2t_dist < dist:
            return tx, ty, to_int_degree(theta)

    theta = get_angle_for_vector((ox, oy), (tx, ty))
    dx = dist * math.cos(theta)
    dy = dist * math.sin(theta)

    return t.xcor() + dx, t.ycor() + dy, to_int_degree(theta)


def stop_moving(t):
    t.orig_pos = (t.xcor(), t.ycor())
    t.target_pos = (t.xcor(), t.ycor())


def get_dist(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


def get_dist_dot_to_line(dot, line_dot_1, line_dot_2, id, msg):
    # get a, b, c in ax + by + c = 0 first
    x1, y1 = line_dot_1
    x2, y2 = line_dot_2
    if x1 == x2:
        a, b, c = 1, 0, -x1
    elif y1 == y2:
        a, b, c = 0, 1, -y1
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

    # print("dist from {} ({}) ({}, {}) to line ({}, {}) - ({}, {}) = {}".format(id, msg, str(x0), str(y0), str(x1), str(y1), str(x2), str(y2), str(dist)))
    return dist


def find_first_collision(moving_obj, potential_target_map, new_cors):
    target_min_heap = []
    for t_id, t in potential_target_map.items():
        dist = t.distance(moving_obj.xcor(), moving_obj.ycor())
        heapq.heappush(target_min_heap, (dist, t_id))

    ox, oy = moving_obj.xcor(), moving_obj.ycor()
    nx, ny = new_cors
    # print("ox, oy = ({}, {})  nx, ny = ({}, {})".format(str(ox), str(oy), str(nx), str(ny)))
    while target_min_heap:
        dist, t_id = heapq.heappop(target_min_heap)
        t = potential_target_map[t_id]
        min_collision_dist = ((20.0 * (t._stretchfactor[0] + moving_obj._stretchfactor[0]) / 2) +
                              (20.0 * (t._stretchfactor[1] + moving_obj._stretchfactor[1]) / 2)) / 2

        c = get_dist((ox, oy), (nx, ny))
        # if missile collides with enemy's current position, count as valid collision
        tx, ty = t.xcor(), t.ycor()
        a = get_dist((tx, ty), (ox, oy))
        b = get_dist((tx, ty), (nx, ny))
        # handle too-close case, regardless of direction
        if min(a, b) < min_collision_dist:
            # print("return 1")
            return t
        # here need to make sure dot to line dist (line) falls on the line segment
        # this is guaranteed by making sure angles from both ends of the line segment < 90 degrees
        aa, bb, cc = a * a, b * b, c * c
        if cc + aa > bb and cc + bb > aa and get_dist_dot_to_line((tx, ty), (ox, oy), (nx, ny), t_id, "curr") <= min_collision_dist:
            print("tx, ty = ({}, {}), a = {}, b = {}, c = {}, aa = {}, bb = {}, cc = {}, dist_dot_to_line = {}, min_collision_dist = {}".format(
                str(tx), str(ty), str(a), str(b), str(c), str(aa), str(bb), str(cc), str(get_dist_dot_to_line((tx, ty), (ox, oy), (nx, ny), t_id, "curr")), str(min_collision_dist)
            ))
            # print("return 2")
            return t

        # if missile collides with enemy's prev position, also count as valid collision
        if hasattr(t, "prev_pos"):
            tx, ty = t.prev_pos
            a = get_dist((tx, ty), (ox, oy))
            b = get_dist((tx, ty), (nx, ny))
            # handle too-close case, regardless of direction
            if min(a, b) < min_collision_dist:
                # print("return 3")
                return t
            aa, bb, cc = a * a, b * b, c * c
            if cc + aa > bb and cc + bb > aa and get_dist_dot_to_line((tx, ty), (ox, oy), (nx, ny), t_id, "prev") <= min_collision_dist:
                # print("return 4")
                return t
        # walls don't have prev pos, so no need to do this.
        else:
            pass

    return None


def get_shape_size(health):
    return max(MIN_SHAPE_PCT/100, health/STANDARD_HEALTH)


def handle_missile_damage(battle_unit, missile):
    bu, m = battle_unit, missile
    damage = max(0, m.owner.battle_unit_data.attack * m.skill_data.conversion - bu.battle_unit_data.defense)
    health = bu.battle_unit_data.health
    print("attack = {}, conversion = {}, defense = {}, damage = {}, health = {}".format(
        str(m.owner.battle_unit_data.attack), str(m.skill_data.conversion), str(bu.battle_unit_data.defense), str(damage), str(health)))
    health = max(0, health - damage)
    print("health after = " + str(health))
    bu.battle_unit_data.health = health
    if health == 0:
        bu.hideturtle()
        return True
    else:
        bu.shapesize(get_shape_size(health))
        bu.battle_unit_data.add_effects(m.skill_data.effects)
        return False


def handle_missile_damage_on_wall(wall_unit, missile):
    wu, m = wall_unit, missile
    damage = max(0, m.owner.battle_unit_data.attack * m.skill_data.conversion - wu.wall_unit_data.defense)
    health = wu.wall_unit_data.health
    print("attack = {}, conversion = {}, defense = {}, damage = {}, health = {}".format(
        str(m.owner.battle_unit_data.attack), str(m.skill_data.conversion), str(wu.wall_unit_data.defense), str(damage), str(health)))
    health = max(0, health - damage)
    print("health after = " + str(health))
    wu.wall_unit_data.health = health
    if health == 0:
        wu.hideturtle()
        return True
    else:
        return False


def fire_missile(attacker, target_cor, missile_list):
    p = attacker
    target_x, target_y = target_cor
    x, y = p.xcor(), p.ycor()
    if target_x == x and target_y == y:
        print("need some angle to attack, skip")
        return False
    angle = to_int_degree(get_angle_for_vector((x, y), (target_x, target_y)))
    p.target_pos = (x, y)
    p.stop = True
    p.shooting_angle = angle
    # print("[2] set p angle = " + str(angle))
    skill = p.battle_unit_data.skills[p.battle_unit_data.left_click_skill_key]
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
            return False

    missile = turtle.Turtle()
    m = missile
    m.penup()
    m.id = "missile_" + str(len(missile_list))
    m.shape(skill.shape)
    m.color(skill.color)
    m.goto(x, y)
    m.orig_pos = (x, y)
    m.target_pos = (target_x, target_y)
    m.shapesize(0.5)
    m.skill_data = skill
    m.owner = p

    speed_per_sec = MISSILE_BASE_SPEED * FRAME * skill.flying_speed
    max_flying_time = skill.attack_range / speed_per_sec
    # print("speed_per_sec = " + str(speed_per_sec) + ", max_flying_time = " + str(max_flying_time))
    m.ttl = now + max_flying_time

    missile_list[m.id] = m

    return True


def combine_map(m1, m2):
    m = dict()
    for k, v in m1.items():
        m[k] = v
    for k, v in m2.items():
        m[k] = v
    return m


def find_path(a, b, blocks):
    cost_hp = [(0, a, None)]
    visited = {a: (None, 0)}
    closest = [a, get_dist(a, b)]
    while cost_hp:
        if b in visited:
            break
        cost, cor, prev = heapq.heappop(cost_hp)
        x, y = cor
        for dx in (-20, 0, 20):
            for dy in (-20, 0, 20):
                new_x, new_y = x + dx, y + dy
                new_cor = (new_x, new_y)
                # if visited or hit a wall, continue
                if new_cor in blocks:
                    continue
                # if diagonal a -> b step got blocked by something like below, continue
                # a x  or  a x  or  a +
                # x b      + b      x b
                if (new_x, y) in blocks or (x, new_y) in blocks:
                    continue
                new_cost = visited[cor][1] + get_dist(cor, new_cor)
                if new_cor in visited and visited[new_cor][1] <= new_cost:
                    continue
                visited[new_cor] = (cor, new_cost)
                heapq.heappush(cost_hp, (new_cost, new_cor, cor))
                dist = get_dist(new_cor, b)
                if dist < closest[1]:
                    closest = [new_cor, dist]

    def back_trace(p):
        result = []
        while p is not None:
            result.append(p)
            p = visited[p][0]
        return result

    if b not in visited:
        # print("not reachable, go to closest point {}".format(str(closest[0])))
        res = back_trace(closest[0])
        return False, res[::-1]

    res = back_trace(b)
    return True, res[::-1]


# from a to b, considering walls cannot be passed
def get_way_points(a, b, walls_cor_set):
    result = []

    def to_way_point(cor):
        x, y = cor
        new_cor = (round((x - 10) / 20) * 20 + 10, round((y - 10) / 20) * 20 + 10)
        return new_cor

    new_a = to_way_point(a)
    new_b = to_way_point(b)

    # print("a = {}, new_a = {}, b = {}, new_b = {}".format(str(a), str(new_a), str(b), str(new_b)))
    # print("walls = {}".format(str(walls_cor_set)))

    # a and b maybe double added, but should be ok.
    valid, path = find_path(new_a, new_b, walls_cor_set)

    if valid:  # not valid means we do not go to destination, rather we go to one of the closest points
        result.append(a)
        result.extend(path[1:-1])
        result.append(b)
    else:
        result.append(a)
        result.extend(path[1:])

    result = result[::-1]
    # print("way points = {}".format(str(result)))
    return result
