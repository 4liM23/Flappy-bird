import pygame as pg
import random

pg.init()
clock = pg.time.Clock()
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 450

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pg.image.load(r"assets/sprites/background-day.png")
BACKGROUND = pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))


class Bird(pg.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.images = [pg.image.load(r"assets/sprites/bluebird-downflap.png"),
                       pg.image.load(r"assets/sprites/bluebird-midflap.png"),
                       pg.image.load(r"assets/sprites/bluebird-upflap.png")]

        self.image_number = 0
        self.image = self.images[self.image_number]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 6
        self.rect.y = SCREEN_HEIGHT // 2
        self.fall_time = 0
        self.velocity = 0
        self.acceleration = 0.1

    # Vf = Vi + a * t
    def update(self):
        # updating flapping animation
        self.image_number += 1
        self.image_number %= 3
        self.image = self.images[self.image_number]

        # updating falling variables and y position
        self.fall_time += 1
        self.velocity = self.velocity - (self.acceleration * self.fall_time)
        self.rect.y -= self.velocity

    def jump(self):
        self.velocity = 12
        self.rect.y += self.velocity
        self.fall_time = 0


class Pipes(pg.sprite.Sprite):
    def __init__(self, bird: Bird):
        super().__init__()
        self.vertical_distance = bird.rect.size[1] * 2

        # loading the images
        self.images = [pg.image.load('assets/sprites/pipe-red.png'), pg.image.load('assets/sprites/pipe-green.png')]

        # selecting the images
        self.image_idx = random.randint(0, 2) % 2
        self.image_down = self.images[self.image_idx]

        # Process the image for the pip coming from above
        # self.image_up = pg.transform.rotate(pg.transform.scale(self.images[self.image_idx], ()), 180)
        self.image_up = pg.transform.rotate(self.images[self.image_idx], 180)
        # Where will it be placed
        self.x = SCREEN_WIDTH // 6

        # down
        self.rect_down = self.image_down.get_rect()
        self.rect_down.x = self.x
        self.rect_down.y = SCREEN_HEIGHT // 2

        # Up
        self.rect_up = self.image_up.get_rect()
        self.rect_up.x = self.x
        self.rect_up.y = self.rect_down.y - self.rect_down.size[1] - self.vertical_distance

    def update(self):
        self.image_idx = random.randint(0, 2) % 2
        self.image_down, self.image_up = self.images[self.image_idx], self.images[self.image_idx]



bird = Bird()

bird_group = pg.sprite.Group()
bird_group.add(bird)

# Pipes
pipe = Pipes(bird)
pipes_groups = pg.sprite.Group()
pipes_groups.add(pipe)

running = True
while running:
    clock.tick(20)
    screen.blit(BACKGROUND, (0, 0))
    # pipe
    pipe.update()
    pipes_groups.draw(screen)

    bird.update()
    bird_group.draw(screen)
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bird.jump()

pg.quit()
