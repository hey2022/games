# FIXME: side collision physics
# TODO: Spin
# TODO: Prevent infinite vertical speed
import sys

import pygame


class JameyBot:
    def __init__(self):
        self.trajectory = game.screen_height // 2

    def predict_trajectory(self):
        if game.ball.speed_x < 0:
            self.trajectory = game.screen_height // 2
        else:
            platform_x = game.screen_length - game.gap - game.platform_length - game.ball.radius
            self.trajectory = game.ball.y
            temp_ball_speed_y = game.ball.speed_y
            for i in range(game.ball.x, platform_x + 1, game.ball.speed_x):
                if self.trajectory + game.ball.radius >= game.screen_height or self.trajectory - game.ball.radius <= 0:
                    temp_ball_speed_y *= -1
                self.trajectory += temp_ball_speed_y

    def move(self):
        platform_x = game.screen_length - game.gap - game.platform_length - game.ball.radius
        platform_y = game.platform1.y + (game.platform_height / 2)
        distance = (self.trajectory - platform_y)
        time = ((platform_x - game.ball.x) / game.ball.speed_x)
        if game.ball.speed_x > 0:
            speed = distance // time
        else:
            speed = distance
        if speed > game.platform_speed:
            speed = game.platform_speed
        elif speed < -game.platform_speed:
            speed = -game.platform_speed
        game.platform1.velocity = speed

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = -game.ball_speed
        self.speed_y = 0

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.check_collision()

    def draw(self):
        pygame.draw.circle(game.screen, 0xffffff, (self.x, self.y), self.radius)

    def check_collision(self):
        if game.platform.x <= self.x - self.radius <= game.platform.x + game.platform_length and game.platform.y - self.radius <= self.y <= game.platform.y + game.platform.height + self.radius:
            self.speed_x *= -1
            self.speed_y += game.platform.velocity // 5
        elif game.platform1.x <= self.x + self.radius <= game.platform1.x + game.platform_length and game.platform1.y - self.radius <= self.y <= game.platform1.y + game.platform1.height + self.radius:
            self.speed_x *= -1
            self.speed_y += game.platform1.velocity // 5

        if self.y - self.radius <= 0 or self.y + self.radius >= game.screen_height:
            self.speed_y *= -1
        if self.x + self.radius >= game.screen_length:
            game.score[0] += 1
            game.setup()
        if self.x - self.radius <= 0:
            game.score[1] += 1
            game.setup()


class Platform:
    velocity = 0

    def __init__(self, x, length, height):
        self.x = x
        self.y = game.screen_height // 2 - height // 2
        self.length = length
        self.height = height

    def move(self):
        self.y += self.velocity
        self.check_collision()

    def draw(self):
        pygame.draw.rect(game.screen, 0xffffff, pygame.Rect(self.x, self.y, self.length, self.height))

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

    def __init__(self, gap, platform_length, platform_height, speed):
        self.ball = None
        self.platform = None
        self.platform1 = None
        self.gap = gap
        self.platform_length = platform_length
        self.platform_height = platform_height
        self.speed = speed
        self.platform_speed = 10
        self.ball_speed = 10

    def setup(self):
        self.platform = Platform(self.gap, self.platform_length, self.platform_height)
        self.platform1 = Platform(game.screen_length - self.platform_length - self.gap, self.platform_length,
                                  self.platform_height)
        self.ball = Ball(game.screen_length // 2, game.screen_height // 2, 5)

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
        text = self.large.render("Game Over", True, 0x99ffcc00)
        text_rect = text.get_rect(center=(self.screen_length // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def display_score(self):
        score_box = self.small.render(f"{self.score[0]} : {self.score[1]}", True, 0xffffff00)
        score_rect = score_box.get_rect(center=(self.screen_length // 2, self.screen_height // 2))
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
    game = Game(50, 10, 100, 60)
    bot = JameyBot()
    game.setup()
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
