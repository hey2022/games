import heapq
import math
import random
import sys

import pygame


class Game:
    pygame.init()
    pygame.display.set_caption("Snake game")
    times = pygame.time.Clock()

    def __init__(self, width, height, block, speed, ai):
        self.screen = pygame.display.set_mode((width, height))
        self.width, self.height = pygame.display.get_surface().get_size()
        self.large = pygame.font.SysFont("Consolas", self.width // 10)
        self.small = pygame.font.SysFont("Consolas", self.width // 25)
        self.ai = ai
        self.speed = speed
        self.block = block

    def game_end(self, text):
        self.screen.fill(0x565656)
        text = self.large.render(text, True, 0x99ffcc00)
        text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
        self.screen.blit(text, text_rect)
        snake.display_score()
        snake.display_steps()
        pygame.display.flip()
        while True:
            for event_1 in pygame.event.get():
                if event_1.type == pygame.KEYDOWN and event_1.key == pygame.K_ESCAPE or event_1.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


class AStar:
    def h_cost(self, node, goal):
        return abs(node[0] - goal[1]) + abs(node[0] - goal[1])

    def reconstruct_path(self, came_from, current):
        total_path = [list(current)]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, list(current))
        return total_path[1:]

    def valid(self, coords):
        if list(coords) in snake.snake_body or coords[0] >= game.width or coords[0] < 0 or coords[1] >= game.height or \
                coords[1] < 0:
            return False
        return True

    def a_star(self, start, goal):
        open_set = []
        heapq.heappush(open_set, ((0, 0), start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.h_cost(start, goal)}
        while len(open_set) > 0:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                return self.reconstruct_path(came_from, current)
            neighbors = [(current[0], current[1] - game.block), (current[0] + game.block, current[1]),
                         (current[0], current[1] + game.block), (current[0] - game.block, current[1])]
            for neighbor in neighbors:
                if self.valid(neighbor):
                    new_g = g_score.get(current) + game.block
                    if new_g < g_score.get(neighbor, math.inf):
                        came_from[neighbor] = current
                        g_score[neighbor] = new_g
                        f_score[neighbor] = new_g + self.h_cost(neighbor, goal)
                        if ((f_score[neighbor], self.h_cost(neighbor, goal)), neighbor) not in open_set:
                            heapq.heappush(open_set, ((f_score[neighbor], self.h_cost(neighbor, goal)), neighbor))
        return False


class Snake:
    snake_body = []
    direction = "right"
    temp_direction = "right"
    score = 0
    inverse = []
    steps = 0
    path = []
    path_index = 0

    def gen_path(self):
        self.path = a_star.a_star((self.snake_pos[0], self.snake_pos[1]), (food.food_pos[0], food.food_pos[1]))
        self.path_index = 0

    def get_dir(self):
        if self.path[self.path_index][0] == self.snake_pos[0] + game.block:
            self.temp_direction = "right"
        elif self.path[self.path_index][0] == self.snake_pos[0] - game.block:
            self.temp_direction = "left"
        elif self.path[self.path_index][1] == self.snake_pos[1] + game.block:
            self.temp_direction = "down"
        elif self.path[self.path_index][1] == self.snake_pos[1] - game.block:
            self.temp_direction = "up"

    def __init__(self, size):
        self.snake_pos = [game.width // 4, game.height // 2]
        for i in range(size):
            self.snake_body.append([game.width // 4, game.height // 2])

    # def bot(self):
    #     if self.snake_pos[0] == 0 and self.snake_pos != [0, 0]:
    #         self.temp_direction = "up"
    #     elif self.snake_pos[1] / game.block % 2 == 0:
    #         if self.snake_pos[0] == game.width - game.block:
    #             self.temp_direction = "down"
    #         else:
    #             self.temp_direction = "right"
    #     elif self.snake_pos[1] / game.block % 2 == 1:
    #         if self.snake_pos[0] == game.block and self.snake_pos != [game.block, game.height - game.block]:
    #             self.temp_direction = "down"
    #         else:
    #             self.temp_direction = "left"

    def bot(self):
        self.get_dir()
        self.path_index += 1

    def display_score(self):
        score = game.small.render(f"Score: {self.score}", True, 0x00ffff00)
        game.screen.blit(score, (10, 10))

    def draw_snake(self):
        for position in self.snake_body:
            pygame.draw.rect(game.screen, 0x99ffcc,
                             (position[0] + game.block * 0.05, position[1] + game.block * 0.05, game.block * 0.9,
                              game.block * 0.9))
        pygame.draw.rect(game.screen, 0x00ffff, (self.snake_pos[0] + game.block // 4,
                                                 self.snake_pos[1] + game.block // 4,
                                                 game.block // 2, game.block // 2))

    def display_steps(self):
        steps = game.small.render(f"Steps: {self.steps}", True, 0x00ffff00)
        steps_rect = steps.get_rect()
        steps_rect.right = game.width - 10
        steps_rect.top = 10

        game.screen.blit(steps, steps_rect)

    def draw_path(self):
        for i in self.path[self.path_index:]:
            pygame.draw.rect(game.screen, 0x0000ff,
                             (i[0] + game.block * 0.05, i[1] + game.block * 0.05, game.block * 0.9, game.block * 0.9))

    def draw(self):
        self.draw_snake()
        self.display_score()
        self.display_steps()

    def move_head(self):
        self.direction = self.temp_direction
        if self.direction == "right":
            self.snake_pos[0] += game.block
        elif self.direction == "left":
            self.snake_pos[0] -= game.block
        elif self.direction == "up":
            self.snake_pos[1] -= game.block
        elif self.direction == "down":
            self.snake_pos[1] += game.block
        self.steps += 1

    def control(self):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            if self.direction != "left":
                self.temp_direction = "right"
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            if self.direction != "right":
                self.temp_direction = "left"
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if self.direction != "up":
                self.temp_direction = "down"
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            if self.direction != "down":
                self.temp_direction = "up"

    def check_collision(self):
        if self.snake_pos[0] >= game.width or self.snake_pos[0] < 0 or self.snake_pos[1] >= game.height or \
                self.snake_pos[1] < 0:
            game.game_end("Game Over ._.")
        if self.snake_pos in self.snake_body:
            game.game_end("Game Over ._.")


class Food:
    food_pos = [0, 0]

    def __init__(self):
        self.generate_food()

    def draw(self):
        pygame.draw.circle(game.screen, 0xff0000,
                           (self.food_pos[0] + game.block // 2, self.food_pos[1] + game.block // 2), game.block // 2)

    def generate_food(self):
        while True:
            self.food_pos[0] = random.randint(0, game.width // game.block - 1) * game.block
            self.food_pos[1] = random.randint(0, game.height // game.block - 1) * game.block
            if self.food_pos not in snake.snake_body:
                break


if __name__ == "__main__":
    game = Game(800, 800, 20, 20, True)
    snake = Snake(3)
    food = Food()
    a_star = AStar()
    snake.gen_path()
    if len(snake.snake_body) >= game.width * game.height // game.block ** 2:
        game.game_end("You win!")
    while True:
        game.screen.fill(0x565656)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                snake.control()
        if game.ai:
            snake.bot()
        snake.move_head()
        if snake.snake_pos == food.food_pos:
            snake.score += 1
            snake.snake_body.insert(0, list(snake.snake_pos))
            if len(snake.snake_body) >= game.width * game.height // game.block ** 2:
                game.game_end("You Win!")
            food.generate_food()
            if game.ai:
                snake.gen_path()
        else:
            snake.snake_body.pop()
            snake.check_collision()
            snake.snake_body.insert(0, list(snake.snake_pos))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if game.ai:
            snake.draw_path()
        snake.draw()
        food.draw()

        pygame.display.flip()
        game.times.tick(game.speed)
