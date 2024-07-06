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
    def __init__(self, bird: Bird, y, up):
        super().__init__()
        self.up = up
        self.bird_size = bird.rect.size[1]
        self.gap_multiplier = 4
        self.vertical_distance = self.bird_size * self.gap_multiplier
        self.y = y
        # loading the images
        self.images = [pg.image.load('assets/sprites/pipe-red.png'), pg.image.load('assets/sprites/pipe-green.png')]

        # selecting the images
        self.image_idx = random.randint(0, 2) % 2
        self.image = self.images[self.image_idx] if not self.up else pg.transform.flip(self.images[self.image_idx],
                                                                                       False, True)

        # Where will it be placed
        self.x = SCREEN_WIDTH // 3

        # down
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = (SCREEN_HEIGHT // 2) - self.y + self.vertical_distance

    def update(self):
        self.rect.x -= 10
        if self.rect.x + self.rect.size[0] <= 0:
            self.rect.x = SCREEN_WIDTH + 30

        # Check if bird is on collision with the pipe

        if self.rect.x <= bird.rect.x + bird.rect.size[0] <= self.rect.x + self.rect.size[
            0] or self.rect.x <= bird.rect.x <= self.rect.x + self.rect.size[0]:
            if self.rect.y <= bird.rect.y + bird.rect.size[1] <= self.rect.y + self.rect.size[
                1] or self.rect.y <= bird.rect.y <= self.rect.y + self.rect.size[1]:
                exit()

        # self.image_idx = random.randint(0, 2) % 2
        # self.image = self.images[self.image_idx]


def generate_pipe(bird_ref: Bird):
    pipe_list = [0, 0]
    for i in range(2):
        try:
            pipe_list[i] = Pipes(bird_ref, pipe_list[0].rect.y, i)
        except Exception:
            pipe_list[i] = Pipes(bird, 0, i)
    return pipe_list


bird = Bird()

bird_group = pg.sprite.Group()
bird_group.add(bird)

# Pipes
pipes_list = generate_pipe(bird)
pipes_groups = pg.sprite.Group()
for pipe in pipes_list:
    pipes_groups.add(pipe)

running = True
while running:
    clock.tick(20)
    screen.blit(BACKGROUND, (0, 0))
    # pipe
    for pipe in pipes_list:
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
