from copy import deepcopy
import time, os


MAP = """
A C + o + + + + + +
B D + + + + + + + +
+ E + o + o + + + +
+ F o + + + + o + +
+ G o + + + + o + +
+ + o + o + o + + +
+ + + + + + o + + +
+ + + + + + o o o +
+ + + + + + o X o +
+ + + + + + o + + +
"""


class Game:
    def __init__(self):
        self.blocks = set()
        self.height = None
        self.width = None
        self.exit = None
        self.players = dict()
        rows = [row for row in MAP.split("\n") if row]
        self.height = len(rows)
        for row_id, row in enumerate(rows):
            cols = [col for col in row.strip().split(" ")]
            for col_id, v in enumerate(cols):
                self.width = len(cols)
                cor = (row_id, col_id)
                if v == '+':
                    pass
                elif v == 'o':
                    self.blocks.add(cor)
                elif v == 'X':
                    self.exit = cor
                else:
                    self.players[cor] = v

    def find_path(self, start_cor):
        visited_map = {start_cor: None}
        batch = [start_cor]

        def get_path():
            path = []
            node = self.exit
            while node is not None:
                path.append(node)
                node = visited_map[node]
            return path[::-1]

        def is_valid(cor):
            y, x = cor
            return 0 <= y < self.height and 0 <= x < self.width and cor not in self.blocks and cor not in visited_map

        while batch:
            next_batch = []
            for cor in batch:
                if cor == self.exit:
                    return get_path()
                for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    new_cor = (cor[0] + d[0], cor[1] + d[1])
                    if is_valid(new_cor):
                        next_batch.append(new_cor)
                        visited_map[new_cor] = cor
            batch = next_batch

        return []

    def find_paths_for_all_players(self):
        player_paths = dict()
        for cor, player in self.players.items():
            path = self.find_path(cor)
            player_paths[player] = path
            print("player {} - path = {}".format(player, str(path)))
        return player_paths


def serialize_steps(player_paths):
    result = []
    player_info = dict()  # {player: index of path}

    for player, path in player_paths.items():
        player_info[player] = 0

    while player_info:
        result.append(player_info)
        player_info_next = dict()
        cor_set = set()
        for player, idx in player_info.items():
            path = player_paths[player]
            if idx == len(path) - 1:
                continue
            next_cor = player_paths[player][idx+1]
            if next_cor in cor_set:
                player_info_next[player] = idx
            else:
                player_info_next[player] = player_info[player] + 1
            new_idx = player_info_next[player]
            new_cor = player_paths[player][new_idx]
            cor_set.add(new_cor)

        player_info = player_info_next

    for step, status in enumerate(result):
        print("step: {} - {}".format(str(step), str(status)))

    return result


def animate(player_paths, result):
    empty_map = []
    rows = [row for row in MAP.split("\n") if row]
    for row_id, row in enumerate(rows):
        cols = [v if v in ('o', 'X') else '+' for v in row.strip().split(" ")]
        empty_map.append(cols)

    def print_map(m):
        for row in m:
            print(" ".join(row))
        time.sleep(0.8)
        os.system("clear")

    for status in result:
        m = deepcopy(empty_map)
        for player, idx in status.items():
            print("player, index = " + player + ", " + str(idx))
            y, x = player_paths[player][idx]
            m[y][x] = player
        print_map(m)


game = Game()
player_paths = game.find_paths_for_all_players()
result = serialize_steps(player_paths)

animate(player_paths, result)

