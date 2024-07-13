import pygame as pg
import json
import random
import time

ASSETS = r'assets/sprites/'

pg.init()
clock = pg.time.Clock()
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 450

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pg.image.load(rf"{ASSETS}background-day.png")
BACKGROUND = pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

GAMEOVER = pg.image.load(r"assets/sprites/gameover.png").convert_alpha()
GAMEOVER = pg.transform.scale(GAMEOVER, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 12))

class Ground(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(r"assets/sprites/base.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (2 * SCREEN_WIDTH, SCREEN_HEIGHT // 6))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - SCREEN_HEIGHT // 6


class ImageHandler:

    def __init__(self) -> None:
        self.asset = rf"{ASSETS}"
        self.SCREEN_HEIGHT = 700
        self.SCREEN_WIDTH = 450
        self.BACKGROUND = pg.image.load(rf"{ASSETS}background-day.png")
        self.BACKGROUND = pg.transform.scale(self.BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.digits = []
        for i in range(10):
            self.digits.append(pg.image.load(f"{self.asset}{i}.png"))
        self.image = self.digits[0]

    # next
    def convert_number(self):
        pass


class Bird(pg.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.images = [pg.image.load(rf"{ASSETS}bluebird-downflap.png"),
                       pg.image.load(rf"{ASSETS}bluebird-midflap.png"),
                       pg.image.load(rf"{ASSETS}bluebird-upflap.png")]

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


class GameState:
    data_path = r"data.json"
    with open(data_path) as f:
        my_data = json.load(f)

    def __init__(self) -> None:
        self.img = ImageHandler()
        self.data_path = r"data.json"
        with open(self.data_path) as f:
            self.my_data = json.load(f)
        self.score = 0
        self.best_score = self.my_data["best_score"]

    def update_best_score(self):
        self.my_data["best_score"] = self.best_score
        with open(self.data_path, 'w') as f:
            json.dump(self.my_data, f, indent=4)

    # next
    def reset_best_score(self):
        pass

    # next
    def game_over(self):
        pass

    def best_score_screen(self):
        screen_center = (self.img.SCREEN_WIDTH // 2, self.img.SCREEN_HEIGHT // 2)
        pg.draw.rect(self.img.BACKGROUND, self.img.BLACK, self.img.digits[1])


class Pipes(pg.sprite.Sprite):
    def __init__(self, bird: Bird, y, up):
        super().__init__()
        self.up = up
        self.vertical_distance = bird.rect.size[1] * 3
        self.y = y
        # loading the images
        self.images = [pg.image.load(rf'{ASSETS}pipe-red.png'), pg.image.load(rf'{ASSETS}pipe-green.png')]

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

ground = Ground()
ground_group = pg.sprite.Group()
ground_group.add(ground)

# Pipes
pipes_list = generate_pipe(bird)
pipes_groups = pg.sprite.Group()
for pipe in pipes_list:
    pipes_groups.add(pipe)


gameOver = False
running = True
while running:
    clock.tick(20)
    screen.blit(BACKGROUND, (0, 0))

    screen.blit(game_state.img.BACKGROUND, (0, 0))
    # pipe
    for pipe in pipes_list:
        pipe.update()
    pipes_groups.draw(screen)
    bird.update()
    bird_group.draw(screen)
    print (bird.rect.y, SCREEN_HEIGHT - SCREEN_HEIGHT // 6  )
    if bird.rect.y >= (SCREEN_HEIGHT - SCREEN_HEIGHT // 6) :
        gameOver = True
        running = False
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bird.jump()
                game_state.best_score += 1
            if event.key == pg.K_r:
                game_state.best_score_screen()


if gameOver:
    screen.blit(GAMEOVER, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 - SCREEN_HEIGHT // 8))
    bird.acceleration = 0
    bird.velocity = 0
    bird.rect.y = (SCREEN_HEIGHT - SCREEN_HEIGHT // 6) - bird.rect.height
    


game_state.update_best_score()
pg.quit()
