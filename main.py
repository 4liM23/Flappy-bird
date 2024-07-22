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

    # praying this works
    # 999 would be maximum score so we only need to find 3 digits
    def convert_number(self, n):
        d3 = n//100
        d2 = (n//10)%10
        d1 = n%10
        print(n, d3, d2, d1)


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


    # takes where the faces of bird and obj and checks of collision occurs --> True if there is, otherwise False
    def crash(self, object):
        flag = False
        myLeft = self.rect.x
        myRight = self.rect.x + self.rect.size[0]
        myTop = self.rect.y
        myBottom = self.rect.y + self.rect.size[1]
        otherLeft = object.rect.x
        otherRight = object.rect.x + object.rect.size[0]
        otherTop = object.rect.y 
        otherBottom = object.rect.y + object.rect.size[1]

        # Check if bird is on collision with the pipe

        if otherLeft <= myRight <= otherRight or otherLeft <= myLeft <= otherRight:
            if otherTop <= myBottom <= otherBottom or otherTop <= myTop <= otherBottom:
                flag=True

        # All flagame_state should be False by defualt. True only if there is collision detected
        return flag


class Pipes(pg.sprite.Sprite):
    def __init__(self, bird: Bird, y, up):
        super().__init__()
        self.up = up
        self.bird_size = bird.rect.size[1]
        self.gap_multiplier = 4
        self.vertical_distance = self.bird_size * self.gap_multiplier
        self.y = y
        # loading the images
        self.images = [pg.image.load(rf'{ASSETS}pipe-red.png'), pg.image.load(rf'{ASSETS}pipe-green.png')]

        # selecting the images
        self.image_idx = random.randint(0, 2) % 2
        self.image = self.images[self.image_idx] if not self.up else pg.transform.flip(self.images[self.image_idx],False, True)

        # Where will it be placed
        self.x = (SCREEN_WIDTH // 6) * 5

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


class GameState:

    def __init__(self) -> None:
        # Bird
        self.bird = Bird()
        self.bird_group = pg.sprite.Group()
        self.bird_group.add(self.bird)
        # Ground
        self.ground = Ground()
        self.ground_group = pg.sprite.Group()
        self.ground_group.add(self.ground)
        # Pipes
        self.pipes_list = self.generate_pipe()
        self.pipes_groups = pg.sprite.Group()
        for pipe in self.pipes_list:
            self.pipes_groups.add(pipe)
        
        self.img = ImageHandler()
        self.data_path = r"data.json"
        with open(self.data_path) as f:
            self.my_data = json.load(f)
        self.score = 0
        self.best_score = self.my_data["best_score"]
        self.gameOver = False
        self.running = True

    def generate_pipe(self):
        pipe_list = [0, 0]
        for i in range(2):
            try:
                pipe_list[i] = Pipes(self.bird, pipe_list[0].rect.y, i)
            except Exception:
                pipe_list[i] = Pipes(self.bird, 0, i)
        return pipe_list

    def update_best_score(self):
        self.my_data["best_score"] = self.best_score
        with open(self.data_path, 'w') as f:
            json.dump(self.my_data, f, indent=4)

    def reset_best_score(self):
        self.my_data["best_score"] = 0
        with open(self.data_path, 'w') as f:
            json.dump(self.my_data, f, indent=4)

    # next
    def game_over(self):
        screen.blit(GAMEOVER, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 - SCREEN_HEIGHT // 8))
        self.bird.acceleration = 0
        self.bird.velocity = 0
        self.bird.rect.y = (SCREEN_HEIGHT - SCREEN_HEIGHT // 6) - self.bird.rect.height
        pg.display.flip()
        time.sleep(2)



    def best_score_screen(self):
        screen_center = (self.img.SCREEN_WIDTH // 2, self.img.SCREEN_HEIGHT // 2)
        pg.draw.rect(self.img.BACKGROUND, self.img.BLACK, self.img.digits[1])

# Making a new game state and resetting variables
def newGame():
    game_state = GameState()

game_state = GameState()
while (game_state.running):
    clock.tick(20)
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(game_state.img.BACKGROUND, (0, 0))
    # pipe
    for pipe in game_state.pipes_list:
        pipe.update()
    game_state.pipes_groups.draw(screen)
    game_state.bird.update()
    game_state.bird_group.draw(screen)
    print (game_state.bird.rect.y, SCREEN_HEIGHT - SCREEN_HEIGHT // 6)
    if game_state.bird.rect.y >= (SCREEN_HEIGHT - SCREEN_HEIGHT // 6) :
        game_state.gameOver = True
        game_state.running = False
    pg.display.flip()
    # collision check | makes sure there is no collision with any pipe
    if any(game_state.bird.crash(i) for i in game_state.pipes_list):
        game_state.gameOver = True
        game_state.running = False
        print('crash!')

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_state.running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                game_state.bird.jump()
                game_state.best_score += 1
            if event.key == pg.K_r:
                game_state.best_score_screen()


if game_state.gameOver:
    game_state.game_over()





game_state.update_best_score()
pg.quit()