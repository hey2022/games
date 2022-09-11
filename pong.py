import random
import sys

import pygame


class JameyBot:
    def __init__(self):
        self.trajectory = game.screen_height // 2
        self.platform_x = game.screen_length - game.gap - game.platform_length - game.ball.radius

    # predict y coordinate of the ball when it reaches the platform
    def predict_trajectory(self):
        if game.ball.speed_x <= 0:
            self.trajectory = game.screen_height // 2
        else:
            self.trajectory = game.ball.y
            temp_ball_speed_y = game.ball.speed_y
            for i in range(game.ball.x, self.platform_x + 1, game.ball.speed_x):
                pygame.draw.circle(game.screen, 0x00ffff, (i, self.trajectory), 1)
                if self.trajectory + game.ball.radius >= game.screen_height and temp_ball_speed_y > 0 or self.trajectory - game.ball.radius <= 0 and temp_ball_speed_y < 0:
                    temp_ball_speed_y *= -1
                self.trajectory += temp_ball_speed_y
        pygame.draw.circle(game.screen, 0x00ffff, (self.platform_x, self.trajectory), 5)

    # move to the predicted trajectory in a "smooth way"
    def move(self):
        platform_y = game.platform1.y + (game.platform_height / 2)
        distance = (self.trajectory - platform_y)
        time = ((self.platform_x - game.ball.x) / game.ball.speed_x)
        # calculate the speed the platform needs to move
        if game.ball.speed_x > 0:
            speed = distance // time
        else:
            speed = distance
        # prevents platform from move past max speed
        if speed > game.platform_speed:
            speed = game.platform_speed
        elif speed < -game.platform_speed:
            speed = -game.platform_speed
        game.platform1.velocity = speed


class Ball:
    def __init__(self, x, y, radius):
        self.rotate = 0
        self.min_speed = game.ball_speed / 1.8
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = (1 - random.randint(0, 1) * 2) * game.ball_speed
        self.speed_y = 0
        self.rotate_help = 0

    def move(self):
        # prevents the speed_x ever from being lower than half of the speed_y
        if abs(self.speed_x) < abs(self.speed_y / 2):
            self.speed_x *= 1.1
        # prevents speed_x from going below min_speed
        if 0 < self.speed_x < self.min_speed:
            self.speed_x = self.min_speed
        if 0 >= self.speed_x > -self.min_speed:
            self.speed_x = -self.min_speed
        self.x += self.speed_x
        self.y += self.speed_y
        self.check_collision()

    def draw(self):
        pygame.draw.circle(game.screen, 0xffffff, (self.x, self.y), self.radius)
        pygame.draw.aaline(game.screen, 0xffffff, (self.x, self.y),
                           (self.x + self.speed_x * 3, self.y + self.speed_y * 3))

    def get_v(self):
        return (self.x * self.x + self.y * self.y) ** 0.5

    # collision physics
    def check_collision(self):
        is_bounce = False
        # collide with left platform
        if game.platform.x <= self.x - self.radius <= game.platform.x + game.platform_length and game.platform.y - self.radius < self.y < game.platform.y + game.platform.height + self.radius:
            self.speed_x *= -1
            self.speed_y = game.platform.velocity // 5 + self.speed_y / 1.05
            self.rotate = -game.platform.velocity + self.rotate / 2
            is_bounce = True

        # collide with right platform
        elif game.platform1.x <= self.x + self.radius <= game.platform1.x + game.platform_length and game.platform1.y - self.radius < self.y < game.platform1.y + game.platform1.height + self.radius:
            self.speed_x *= -1
            self.speed_y = game.platform1.velocity // 5 + self.speed_y / 1.05
            self.rotate = game.platform1.velocity + self.rotate / 2
            is_bounce = True
            pass
        # collide with top wall
        if self.y - self.radius <= 0 and self.speed_y < 0:
            self.speed_y *= -1
            is_bounce = True
        # collide with bottom wall
        if self.y + self.radius >= game.screen_height and self.speed_y > 0:
            self.speed_y *= -1
            is_bounce = True
        # reaches beyond the platform
        if self.x - self.radius >= game.screen_length:
            game.score[0] += 1
            game.setup()
        if self.x + self.radius <= 0:
            game.score[1] += 1
            game.setup()
            pass
        # if is_bounce just collided with something
        if is_bounce:
            self.rotate /= 1.3


class Platform:
    velocity = 0

    def __init__(self, x, length, height):
        self.x = x
        self.y = game.screen_height // 2 - game.platform_height // 2
        self.length = length
        self.height = height

    def move(self):
        self.y += self.velocity
        self.check_collision()

    def draw(self):
        pygame.draw.rect(game.screen, 0xffffff, pygame.Rect(self.x, self.y, self.length, self.height))

    # prevents platform from going outside the screen
    def check_collision(self):
        if self.y <= 0:
            self.y = 0
            self.velocity = 0
        elif self.y + self.height >= game.screen_height:
            self.y = game.screen_height - self.height
            self.velocity = 0


class Game:
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_length, screen_height = screen.get_size()
    large = pygame.font.SysFont("Consolas", screen_length // 10)
    small = pygame.font.SysFont("Consolas", screen_length // 25)
    score = [0, 0]

    def __init__(self, gap, platform_length, platform_height, speed, win_point):
        self.ball = None
        self.platform = None
        self.platform1 = None
        self.gap = gap
        self.platform_length = platform_length
        self.platform_height = platform_height
        self.speed = speed
        self.platform_speed = 10
        self.ball_speed = 10
        self.win_point = win_point

    # called when a point is scored and resets to the initial state
    def setup(self):
        if self.score[0] >= self.win_point or self.score[1] >= self.win_point:
            self.game_over()
        self.platform = Platform(self.gap, self.platform_length, self.platform_height)
        self.platform1 = Platform(game.screen_length - self.platform_length - self.gap, self.platform_length,
                                  self.platform_height)
        self.ball = Ball(game.screen_length // 2, game.screen_height // 2, 5)

    # control platform velocity with keyboard input
    def control(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.platform.velocity = -self.platform_speed
            if event.key == pygame.K_s:
                self.platform.velocity = self.platform_speed
            if event.key == pygame.K_UP:
                self.platform1.velocity = -self.platform_speed
            if event.key == pygame.K_DOWN:
                self.platform1.velocity = self.platform_speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.platform.velocity = 0
            if event.key == pygame.K_s:
                self.platform.velocity = 0
            if event.key == pygame.K_UP:
                self.platform1.velocity = 0
            if event.key == pygame.K_DOWN:
                self.platform1.velocity = 0

    def game_over(self):
        self.display()
        text = self.large.render("Game Over", True, 0xffffffff)
        text_rect = text.get_rect(center=(self.screen_length // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def display_score(self):
        score_box = self.small.render(f"{self.score[0]} : {self.score[1]}", True, 0xffffffff)
        score_rect = score_box.get_rect(center=(self.screen_length // 2, self.screen_height // 8))
        self.screen.blit(score_box, score_rect)

    def move(self):
        self.platform.move()
        self.platform1.move()
        self.ball.move()

    def display(self):
        self.platform.draw()
        self.platform1.draw()
        self.ball.draw()
        self.display_score()
        pygame.display.flip()

    def tick(self):
        self.clock.tick(self.speed)


if __name__ == '__main__':
    game = Game(50, 10, 100, 60, 11)
    game.setup()
    bot = JameyBot()
    while True:
        game.screen.fill(0x000000)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                game.control()
        bot.predict_trajectory()
        bot.move()
        game.move()
        game.display()
        game.tick()
