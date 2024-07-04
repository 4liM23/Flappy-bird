import pygame as pg
import json 


pg.init()
clock = pg.time.Clock()
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 450

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pg.image.load(r".\assets\sprites\background-day.png")
BACKGROUND = pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))


class Bird(pg.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
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
        self.image_number+=1
        self.image_number%=3
        self.image = self.images[self.image_number]

        # updating falling variables and y position
        self.fall_time += 1
        self.velocity = self.velocity - (self.acceleration * self.fall_time)
        self.rect.y -= self.velocity

    def jump(self):
        self.velocity = 12
        self.rect.y += self.velocity
        self.fall_time= 0


class GameState():

    data_path = r".\data.json"
    with open(data_path) as f:
        my_data = json.load(f)
    
    def __init__(self) -> None:
        self.data_path = r".\data.json"
        with open(self.data_path) as f:
            self.my_data = json.load(f)
        self.score = 0
        self.best_score = self.my_data["best_score"]

    def update_best_score(self):
        self.my_data["best_score"] = self.best_score
        with open (self.data_path, 'w') as f:
            json.dump(self.my_data, f, indent=4)

    def reset_best_score(self):
        pass

    def game_over(self):
        pass




bird = Bird()
game_state = GameState()
bird_group = pg.sprite.Group()
bird_group.add(bird)
pg.display.set_caption(str(game_state.best_score))

running = True 
while running:
    clock.tick(20)
    screen.blit(BACKGROUND, (0, 0))
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

game_state.update_best_score()
pg.quit()
