# TODO: add endscreen
# FIXME: collision physics
# TODO: tweak speed

import sys

import pygame


class Ball:
    speed_x = 10
    speed_y = 2

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(screen, 0xffffff, (self.x, self.y), self.radius)

    def check_collision(self):
        if platform.x <= self.x - self.radius <= platform.x + length and platform.y <= self.y <= platform.y + platform.height or platform1.x <= self.x + self.radius >= platform1.x and platform1.y <= self.y <= platform1.y + platform1.height:
            self.speed_x *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= 1000:
            self.speed_y *= -1


class Platform:
    def __init__(self, x, y, length, height):
        self.x = x
        self.y = y
        self.length = length
        self.height = height

    def up(self):
        self.y -= 10

    def down(self):
        self.y += 10

    def draw(self):
        pygame.draw.rect(screen, 0xffffff, pygame.Rect(self.x, self.y, self.length, self.height))


def move():
    if keys_pressed["w"]:
        platform.up()
    if keys_pressed["s"]:
        platform.down()
    if keys_pressed["UP"]:
        platform1.up()
    if keys_pressed["DOWN"]:
        platform1.down()


def determine_keys_pressed():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            keys_pressed["w"] = True
        if event.key == pygame.K_s:
            keys_pressed["s"] = True
        if event.key == pygame.K_UP:
            keys_pressed["UP"] = True
        if event.key == pygame.K_DOWN:
            keys_pressed["DOWN"] = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            keys_pressed["w"] = False
        if event.key == pygame.K_s:
            keys_pressed["s"] = False
        if event.key == pygame.K_UP:
            keys_pressed["UP"] = False
        if event.key == pygame.K_DOWN:
            keys_pressed["DOWN"] = False


def game_end(self, text):
    text = self.large.render(text, True, 0x99ffcc00)
    text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
    self.screen.blit(text, text_rect)
    pygame.display.flip()
    while True:
        for event_1 in pygame.event.get():
            if event_1.type == pygame.KEYDOWN and event_1.key == pygame.K_ESCAPE or event_1.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0))
    screen_length, screen_height = screen.get_size()

    length = 10
    height = 50
    gap = 10
    platform = Platform(gap, screen_height // 2 - height // 2, length, height)
    platform1 = Platform(screen_length - length - gap, screen_height // 2 - height // 2, length, height)
    ball = Ball(screen_length // 2, screen_height // 2, 5)
    keys_pressed = {"w": False, "s": False, "UP": False, "DOWN": False}
    while True:
        screen.fill(0x000000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                determine_keys_pressed()
        move()
        platform.draw()
        platform1.draw()
        ball.move()
        ball.check_collision()
        ball.draw()
        pygame.display.flip()
        clock.tick(60)
