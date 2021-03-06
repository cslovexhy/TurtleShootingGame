import copy
import time
import random


class FindDest:
    def __init__(self, map, player, dest):
        self.map = copy.deepcopy(map)
        assert (map and map[0])
        self.m = len(self.map)
        self.n = len(self.map[0])
        self.player = copy.deepcopy(player)
        self.dest = copy.deepcopy(dest)
        assert (self.is_valid(self.player))
        assert (self.is_valid(self.dest))

    def is_valid(self, coord):
        y, x = coord
        return 0 <= y < self.m and 0 <= x < self.n and self.map[y][x] == ' '

    def find_path(self):
        if self.player == self.dest:
            return [self.player]

        prev_point_map = {self.player: None}
        batch = [self.player]
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while batch:
            next_batch = []
            for p in batch:
                for d in dirs:
                    new_p = (p[0] + d[0], p[1] + d[1])
                    if new_p not in prev_point_map and self.is_valid(new_p):
                        next_batch.append(new_p)
                        prev_point_map[new_p] = p
                        # print(new_p)
                        if new_p == self.dest:
                            result = [new_p]
                            node = prev_point_map[new_p]
                            # print("visited = " + str(len(prev_point_map)))
                            # print("new_p = " + str(new_p))
                            # print(prev_point_map)
                            while node:
                                # print("node = " + str(node))
                                result.append(node)
                                node = prev_point_map[node]
                            result = result[::-1]
                            return result

            batch = next_batch

        return []

    def find_path2(self):
        if self.player == self.dest:
            return [self.player]

        prev_point_map1 = {self.player: None}
        prev_point_map2 = {self.dest: None}
        batch1 = [self.player]
        batch2 = [self.dest]
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while batch1 and batch2:
            next_batch1 = []
            next_batch2 = []
            for p in batch1:
                for d in dirs:
                    new_p = (p[0] + d[0], p[1] + d[1])
                    if new_p not in prev_point_map1 and self.is_valid(new_p):
                        next_batch1.append(new_p)
                        prev_point_map1[new_p] = p
                        # print(new_p)
                        if new_p in prev_point_map2:
                            # print("1: " + str(p) + " met " + str(new_p))
                            # print(prev_point_map1)
                            # print(prev_point_map2)
                            # print("visited = " + str(len(prev_point_map1) + len(prev_point_map2)))

                            result1 = [p]
                            node = prev_point_map1[p]
                            while node:
                                # print("node1 = " + str(node))
                                result1.append(node)
                                node = prev_point_map1[node]

                            result2 = [new_p]
                            node = prev_point_map2[new_p]
                            while node:
                                # print("node2 = " + str(node))
                                result2.append(node)
                                node = prev_point_map2[node]
                            return result1[::-1] + result2

            batch1 = next_batch1

            for p in batch2:
                for d in dirs:
                    new_p = (p[0] + d[0], p[1] + d[1])
                    if new_p not in prev_point_map2 and self.is_valid(new_p):
                        next_batch2.append(new_p)
                        prev_point_map2[new_p] = p
                        # print(new_p)
                        if new_p in prev_point_map1:
                            # print("2: " + str(p) + " met " + str(new_p))
                            # print(prev_point_map1)
                            # print(prev_point_map2)
                            # print("visited = " + str(len(prev_point_map1) + len(prev_point_map2)))

                            result2 = [p]
                            node = prev_point_map2[p]
                            while node:
                                # print("node2 = " + str(node))
                                result2.append(node)
                                node = prev_point_map2[node]

                            result1 = [new_p]
                            node = prev_point_map1[new_p]
                            while node:
                                # print("node1 = " + str(node))
                                result1.append(node)
                                node = prev_point_map1[node]
                            return result1[::-1] + result2

            batch2 = next_batch2

        return []

    def animate(self, path):
        alt_map = copy.deepcopy(self.map)
        alt_map[self.dest[0]][self.dest[1]] = 'X'
        for wp in path:
            alt_map[wp[0]][wp[1]] = 'P'
            alt_map_str = "\n".join([" ".join(row) for row in alt_map])
            print("\n" * self.m)
            print(alt_map_str)
            alt_map[wp[0]][wp[1]] = ' '
            time.sleep(0.5)

    def print_maze(self, path, show_path):
        alt_map = copy.deepcopy(self.map)
        alt_map[self.dest[0]][self.dest[1]] = 'X'
        alt_map[self.player[0]][self.player[1]] = 'P'
        if show_path:
            for wp in path[1:-1]:
                alt_map[wp[0]][wp[1]] = '+'
        alt_map_str = "\n".join([" ".join(row) for row in alt_map])
        print(alt_map_str)


class MapGenerator:
    def __init__(self):
        self.row_num = 10
        self.col_num = 10
        self.wall_pct = 30
        self.max_try = 100
        self.player = (0, 0)
        self.dest = (self.row_num - 1, self.col_num - 1)
        self.exclusive_set = {self.player, self.dest}

    def gen_valid_map(self):
        try_count = 1
        while try_count <= self.max_try:
            map = self.get_random_map()
            path_finder = FindDest(map, self.player, self.dest)
            path = path_finder.find_path2()
            if path:
                path_finder.print_maze(path, False)
                print("\n\n\n\n")
                path_finder.print_maze(path, True)
                print("succeeded on #{} try".format(str(try_count)))
                return map, self.player, self.dest
            try_count += 1
        print("wall % = {}, {} tries finished but no valid map is generated".format(self.wall_pct, self.max_try))
        raise

    def get_random_map(self):
        map = [[' '] * self.col_num for _ in range(self.row_num)]
        for r in range(len(map)):
            for c in range(len(map[r])):
                if (r, c) not in self.exclusive_set and random.randint(0, 100) < self.wall_pct:
                    map[r][c] = '#'
        return map


class FindExitGame:

    def __init__(self, map, player, dest):
        self.d_map = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        self.map = copy.deepcopy(map)
        self.m = len(self.map)
        self.n = len(self.map[0])
        self.player = copy.deepcopy(player)
        self.dest = copy.deepcopy(dest)
        self.visited = {copy.deepcopy(self.player)}
        self.step_count = 0
        self.start()

    def start(self):
        self.print_maze()
        while True:
            c = input("Direction (WSAD):")
            if c not in self.d_map:
                continue
            direction = self.d_map[c]
            next_pos = (self.player[0] + direction[0], self.player[1] + direction[1])
            if not self.is_valid(next_pos):
                self.print_maze()
                print("cannot go there")
                continue
            self.player = next_pos
            self.visited.add(copy.deepcopy(self.player))
            self.step_count += 1
            self.print_maze()
            print("moved")
            if self.player == self.dest:
                path = FindDest(self.map, player, dest).find_path2()
                print("Congratulations! You finished in {} steps. Minimum possible step is {}".format(str(self.step_count), str(len(path)-1)))
                return

    def is_valid(self, coord):
        y, x = coord
        return 0 <= y < self.m and 0 <= x < self.n and self.map[y][x] == ' '

    def print_maze(self, show_visited=True):
        alt_map = copy.deepcopy(self.map)
        alt_map[self.dest[0]][self.dest[1]] = 'X'
        alt_map[self.player[0]][self.player[1]] = 'P'
        if show_visited:
            for p in self.visited:
                if p != self.player:
                    alt_map[p[0]][p[1]] = '+'
        alt_map_str = "\n".join([" ".join(row) for row in alt_map])
        print("\n"*len(self.map))
        print(alt_map_str)


map_gen = MapGenerator()
map, player, dest = map_gen.gen_valid_map()

FindExitGame(map, player, dest)