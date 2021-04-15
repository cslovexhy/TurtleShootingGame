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
        assert(h >= 3 and w >= 3)
        self.h = h
        self.w = w
        self.winning_threshold = self.h * self.w * .6
        self.snake = deque([(1, 2), (1, 1)])
        self.snakeSet = set(self.snake)
        self.apple = self.generate_apple()
        self.start()

    def generate_apple(self):
        while True:
            cor = randint(0, self.h-1), randint(0, self.w-1)
            # print("cor = " + str(cor))
            if cor not in self.snakeSet:
                return cor

    def is_invalid(self, cor):
        y, x = cor
        hit_body = cor in self.snakeSet
        out_of_bound = y < 0 or y >= self.h or x < 0 or x >= self.w
        if hit_body:
            print("hit body")
        if out_of_bound:
            print("out of bound")
        return hit_body or out_of_bound

    def move(self, dir):
        head = self.snake[0]
        if dir not in DIR_MAP:
            print("invalid input, no action")
            return False

        delta = DIR_MAP[dir]
        new_head = (head[0] + delta[0], head[1] + delta[1])

        if len(self.snake) > 1 and new_head == self.snake[1]:
            # print("moving into neck, no action")
            return False

        if new_head != self.apple:
            self.snakeSet.remove(self.snake.pop())

        if self.is_invalid(new_head):
            return True

        self.snake.appendleft(new_head)
        self.snakeSet.add(new_head)

        if new_head == self.apple:
            self.apple = self.generate_apple()

        return False

    # from here below is nice to have but not required.
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

    def start(self):
        while True:
            self.print_board()
            dir = input("- - - - - - - - - dir[w/s/a/d] = ?")
            # print("dir = {}".format(dir))
            dead = self.move(dir)
            if dead:
                print("you lose")
                break
            elif len(self.snake) >= self.winning_threshold:
                print("you win")
                break


game = SnakeGame(3, 3)
