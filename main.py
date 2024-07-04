import pygame as pg

pg.init()
clock = pg.time.Clock()
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 450

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pg.image.load(r"assets/sprites/background-day.png")
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


class Bird(pg.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.images = [pg.image.load(r"./assets/sprites\bluebird-downflap.png"),
                                pg.image.load(r"./assets/sprites\bluebird-midflap.png"),
                                pg.image.load(r"./assets/sprites\bluebird-upflap.png")]


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




bird = Bird()

ground = Ground()
ground_group = pg.sprite.Group()
ground_group.add(ground)

bird_group = pg.sprite.Group()
bird_group.add(bird)



running = True 
gameOver = False
while running:
    clock.tick(20)
    screen.blit(BACKGROUND, (0, 0))
    if gameOver:
        screen.blit(GAMEOVER, (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 - SCREEN_HEIGHT // 8))
    ground_group.draw(screen)
    bird.update()
    bird_group.draw(screen)
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bird.jump()
        print (bird.rect.y, SCREEN_HEIGHT - SCREEN_HEIGHT // 6  )
        if bird.rect.y >= (SCREEN_HEIGHT - SCREEN_HEIGHT // 6) :
            gameOver = True

        


pg.quit()
