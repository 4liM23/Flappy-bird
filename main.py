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

BACKGROUND_LIGHT = pg.image.load(rf"{ASSETS}background-day.png")
BACKGROUND_LIGHT = pg.transform.scale(BACKGROUND_LIGHT, (SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND_DARK = pg.image.load(rf"{ASSETS}background-night.png")
BACKGROUND_DARK = pg.transform.scale(BACKGROUND_DARK, (SCREEN_WIDTH, SCREEN_HEIGHT))

# here | make a function so  you can choose dark mode or light mode
BACKGROUND = BACKGROUND_DARK

LABEL = pg.image.load(rf"{ASSETS}label_flappy_bird.png").convert_alpha()
LABEL = pg.transform.scale(LABEL, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 12))

GAMEOVER = pg.image.load(rf"{ASSETS}gameover.png").convert_alpha()
GAMEOVER = pg.transform.scale(GAMEOVER, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 12))

MENU = pg.image.load(rf"{ASSETS}panel_score.png").convert_alpha()
MENU = pg.transform.scale(MENU, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))

BUTTON_PLAY = pg.image.load(rf"{ASSETS}button_play.png").convert_alpha()
BUTTON_PLAY = pg.transform.scale(BUTTON_PLAY, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 16))

BUTTON_MENU = pg.image.load(rf"{ASSETS}button_menu.png").convert_alpha()
BUTTON_MENU = pg.transform.scale(BUTTON_MENU, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 16))

class Digit(pg.sprite.Sprite):
    
    def __init__(self, type="L") :
        super().__init__()
        self.asset = ASSETS
        self.digits = []
        if type == "M":
            for i in range(10):
                self.digits.append(pg.image.load(f"{self.asset}number_large_{i}.png"))
        else:
            for i in range(10):
                self.digits.append(pg.image.load(f"{self.asset}{i}.png"))
        self.image:pg.Surface = self.digits[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, new_number):
        self.number = new_number
        self.image = self.digits[self.number]
        self.rect = self.image.get_rect()

class ImageHandler:

    def __init__(self, type="L", x=0, y=0) -> None:
        self.x = x
        self.y = y
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.digit_group = pg.sprite.Group()
        self.d3=Digit(type)
        self.d2=Digit(type)
        self.d1=Digit(type)
        self.set_position()
        self.digit_group.add_internal(self.d3, 3)
        self.digit_group.add_internal(self.d2, 3)
        self.digit_group.add_internal(self.d1, 3)

    def set_position(self):
        if self.x==0 and self.y==0 :
            self.d3.rect.y=self.d2.rect.y=self.d1.rect.y = SCREEN_HEIGHT//16
            self.d2.rect.x = SCREEN_WIDTH//2 - self.d2.rect.size[0]//2
            self.d3.rect.x = self.d2.rect.x - self.d3.rect.size[0]
            self.d1.rect.x = self.d2.rect.x + self.d2.rect.size[0]
        else:
            self.d3.rect.y=self.d2.rect.y=self.d1.rect.y = self.y
            self.d2.rect.x = self.x - self.d2.rect.size[0]//2
            self.d3.rect.x = self.d2.rect.x - self.d3.rect.size[0]
            self.d1.rect.x = self.d2.rect.x + self.d2.rect.size[0]

    # praying this works
    # 999 would be maximum score so we only need to find 3 digits
    def convert_number(self, n):
        n3 = n//100
        n2 = (n//10)%10
        n1 = n%10
        self.d3.update(n3);self.d2.update(n2);self.d1.update(n1)
        self.set_position()



class Ground(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(r"assets/sprites/base.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (2 * SCREEN_WIDTH, SCREEN_HEIGHT // 5))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - SCREEN_HEIGHT // 6


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

        self.counted_score = False

    def update(self):
        self.rect.x -= 10
        if self.rect.x + self.rect.size[0] <= 0:
            self.rect.x = SCREEN_WIDTH + 30
            self.counted_score = False

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
        pipe_list = []
        for i in range(2):
            try:
                pipe_list.append(Pipes(self.bird, pipe_list[0].rect.y, i))
            except Exception:
                pipe_list.append(Pipes(self.bird, 0, i))
        return pipe_list

    def score_update(self):
        if (self.pipes_list[0].rect.center[0] < self.bird.rect.center[0]) and self.pipes_list[0].counted_score == False:
            self.score+=1
            self.pipes_list[0].counted_score = True

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



# Making a new game state and resetting variables
def newGame():
    game_state = GameState()
    while (game_state.running):
        clock.tick(20)
        screen.blit(BACKGROUND, (0, 0))
        # pipe
        for pipe in game_state.pipes_list:
            pipe.update()
        game_state.pipes_groups.draw(screen)
        game_state.bird.update()
        game_state.bird_group.draw(screen)
        game_state.score_update()
        game_state.img.convert_number(game_state.score)
        game_state.img.digit_group.draw(screen)
        pg.display.flip()
        # Debug
        print (game_state.bird.rect.y, SCREEN_HEIGHT - SCREEN_HEIGHT // 6)
        # ground-hit check | makes sure the bird is above allowed limit (ground)
        if game_state.bird.rect.y >= (SCREEN_HEIGHT - SCREEN_HEIGHT // 6) :
            game_state.gameOver = True
            game_state.running = False

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

    if game_state.gameOver:
        if game_state.score > game_state.best_score :
            game_state.best_score = game_state.score
        game_state.update_best_score()
        game_state.game_over()
        menuGameOver(game_state.score, game_state.best_score)

def menuGameOver(score, bestscore):
    # initializing both final score and best score digits
    menu_score = ImageHandler("M", SCREEN_WIDTH//2 + MENU.get_width()//3, (SCREEN_HEIGHT // 2 - SCREEN_HEIGHT // 12) + MENU.get_height()//3)
    menu_score.convert_number(score)
    menu_bestscore = ImageHandler("M", SCREEN_WIDTH//2 + MENU.get_width()//3,(SCREEN_HEIGHT // 2 - SCREEN_HEIGHT // 12) + (MENU.get_height()//3)*2)
    menu_bestscore.convert_number(bestscore)
    # displaying gameover menu, than digits on top
    screen.blit(MENU, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - SCREEN_HEIGHT // 12))
    menu_score.digit_group.draw(screen)
    menu_bestscore.digit_group.draw(screen)
    pg.display.flip()

    time.sleep(2)


if __name__ == "__main__":
    newGame()