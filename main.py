import pygame as pg
import random
import json
import random
import time


pg.init()
clock = pg.time.Clock()
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 450

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pg.image.load(r"assets/sprites/background-day.png")
BACKGROUND = pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
class ImageHandler():

    def __init__(self) -> None:
        self.asset = r".\assets\sprites\\"
        self.SCREEN_HEIGHT = 700
        self.SCREEN_WIDTH = 450
        self.BACKGROUND = pg.image.load(r".\assets\sprites\background-day.png")
        self.BACKGROUND = pg.transform.scale(self.BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.ZERO = pg.image.load(self.asset+"0.png")
        self.ONE = pg.image.load(self.asset+"1.png")
        self.TWO = pg.image.load(self.asset+"2.png")
        self.THREE = pg.image.load(self.asset+"3.png")
        self.FOUR = pg.image.load(self.asset+"4.png")
        self.FIVE = pg.image.load(self.asset+"5.png")
        self.SIX = pg.image.load(self.asset+"6.png")
        self.SEVEN = pg.image.load(self.asset+"7.png")
        self.EIGHT = pg.image.load(self.asset+"8.png")
        self.NINE = pg.image.load(self.asset+"9.png")



    # next
    def convert_number(self):
        pass




class Bird(pg.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.images = [pg.image.load(r"assets/sprites/bluebird-downflap.png"),
                       pg.image.load(r"assets/sprites/bluebird-midflap.png"),
                       pg.image.load(r"assets/sprites/bluebird-upflap.png")]
        self.images = [pg.image.load(r".\assets\sprites\bluebird-downflap.png"),
                        pg.image.load(r".\assets\sprites\bluebird-midflap.png"),
                        pg.image.load(r".\assets\sprites\bluebird-upflap.png")]


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


class GameState():

    data_path = r".\data.json"
    with open(data_path) as f:
        my_data = json.load(f)
    
    def __init__(self) -> None:
        self.img = ImageHandler()
        self.data_path = r".\data.json"
        with open(self.data_path) as f:
            self.my_data = json.load(f)
        self.score = 0
        self.best_score = self.my_data["best_score"]

    def update_best_score(self):
        self.my_data["best_score"] = self.best_score
        with open (self.data_path, 'w') as f:
            json.dump(self.my_data, f, indent=4)

    #next
    def reset_best_score(self):
        pass

    #next
    def game_over(self):
        pass

    def best_score_screen(self):
        screen_center = (self.img.SCREEN_WIDTH//2, self.img.SCREEN_HEIGHT//2)
        pg.draw.rect(self.img.BACKGROUND, self.img.BLACK, self.img.ONE)


class Pipes(pg.sprite.Sprite):
    def __init__(self, bird: Bird, y, up):
        super().__init__()
        self.up = up
        self.vertical_distance = bird.rect.size[1] * 3
        self.y = y
        # loading the images
        self.images = [pg.image.load('assets/sprites/pipe-red.png'), pg.image.load('assets/s        prites/pipe-green.png')]

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
game_state = GameState()
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
    i = 0
    for pipe in pipes_list:
        i += 1
        pipe.update()
    pipes_groups.draw(screen)

    screen.blit(game_state.img.BACKGROUND, (0, 0))
    bird.update()
    bird_group.draw(screen)
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bird.jump()
                game_state.best_score+=1
            if event.key == pg.K_r:
                game_state.best_score_screen()


game_state.update_best_score()
pg.quit()
