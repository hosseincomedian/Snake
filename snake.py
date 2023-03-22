import consts


class Snake:

    dx = {'UP': 0, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
    dy = {'UP': -1, 'DOWN': 1, 'LEFT': 0, 'RIGHT': 0}

    def __init__(self, keys, game, pos, color, direction):
        self.keys = keys
        self.cells = [pos]
        self.game = game
        self.game.add_snake(self)
        self.color = color
        self.direction = direction
        game.get_cell(pos).set_color(color)

    def get_head(self):
        return self.cells[-1]

    def val(self, x):
        if x < 0:
            x += self.game.size

        if x >= self.game.size:
            x -= self.game.size

        return x

    def next_move(self):
        full_poss = []
        next_pos = ''
        if self.direction == "DOWN":
            next_pos = self.cells[-1][0], self.val(self.cells[-1][1]+1)
        elif self.direction == "UP":
            next_pos = self.cells[-1][0], self.val(self.cells[-1][1]-1)
        elif self.direction == "RIGHT":
            next_pos = self.val(self.cells[-1][0]+1), self.cells[-1][1]
        elif self.direction == "LEFT":
            next_pos = self.val(self.cells[-1][0]-1), self.cells[-1][1]

        Fruit = next_pos in self.game.fruits
        Full = False

        if Fruit:
            self.cells.append(next_pos)
            self.game.get_cell(next_pos).set_color(self.color)
            self.game.fruits.remove(next_pos)
        else:

            if len(consts.block_cells) > 0:
                for block in consts.block_cells:
                    full_poss.append(tuple(block))
            for snake in self.game.snakes:
                for cell in snake.cells:
                    full_poss.append(cell)
            if next_pos in full_poss:
                Full = True

            if not Full:
                self.game.get_cell(self.cells[0]).set_color(consts.back_color)
                self.game.get_cell(next_pos).set_color(self.color)
                if len(self.cells) == 1:
                    self.cells = [(next_pos)]
                else:
                    self.cells = self.cells[1:]
                    self.cells.append(next_pos)
                    pass

            else:
                self.game.kill(self)

    def handle(self, keys):
        j = {
            "UP": 1,
            "DOWN": -1,
            "RIGHT": 2,
            "LEFT": -2
        }
        for key in keys:
            if key in self.keys:
                if j[self.direction] != -1 * j[self.keys[key]] and j[self.direction] != j[self.keys[key]]:
                    self.direction = self.keys[key]
                    break
