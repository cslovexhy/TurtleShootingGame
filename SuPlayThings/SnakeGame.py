from collections import deque
from random import randint

DIR_MAP = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1)
}


class SnakeGame:
    def __init__(self, h, w):
        assert(h >= 5 and w >= 5)
        self.h = h
        self.w = w
        self.winning_threshold = self.h * self.w / 2
        self.snake = deque([(1, 2), (1, 1)])
        self.snakeSet = set(self.snake)
        self.apple = self.generate_apple()
        self.start()

    def print_board(self):
        for i in range(self.h):
            row = []
            for j in range(self.w):
                cor = (i, j)
                if cor in self.snakeSet:
                    if cor == self.snake[0]:
                        row.append('x')
                    else:
                        row.append('o')
                elif cor == self.apple:
                    row.append('a')
                else:
                    row.append('.')
            print(" ".join(row))
        print("- - - - - - - -")

    def start(self):
        while True:
            self.print_board()
            dir = input("dir[w/s/a/d] = ?")
            print("dir = {}".format(dir))
            dead = self.move(dir)
            if dead:
                print("you lose")
                break
            elif len(self.snake) >= self.winning_threshold:
                print("you win")
                break

    def generate_apple(self):
        while True:
            cor = randint(0, self.h-1), randint(0, self.w-1)
            if cor not in self.snakeSet:
                return cor

    def is_invalid(self, cor):
        y, x = cor
        return cor in self.snakeSet or y < 0 or y > self.h or x < 0 or x >= self.w

    def move(self, dir):
        head = self.snake[0]
        assert(dir in DIR_MAP)
        delta = DIR_MAP[dir]
        new_head = (head[0] + delta[0], head[1] + delta[1])
        if self.is_invalid(new_head):
            return True

        self.snake.appendleft(new_head)
        self.snakeSet.add(new_head)
        if new_head == self.apple:
            self.apple = self.generate_apple()
        else:
            self.snakeSet.remove(self.snake.pop())

        return False


game = SnakeGame(5, 5)
