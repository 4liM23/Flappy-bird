import pygame as pg

pg.init()
clock = pg.time.Clock()
SCREEN_HEIGHT = 1600
SCREEN_WIDTH = 900

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pg.image.load(r"RC24\git_project1\Flappy-bird\assets\sprites\background-day.png")
BACKGROUND = pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))


class ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = 

class Bird(pg.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.images = [pg.image.load(r"RC24\git_project1\Flappy-bird\assets\sprites\bluebird-downflap.png"),
                                pg.image.load(r"RC24\git_project1\Flappy-bird\assets\sprites\bluebird-midflap.png"),
                                pg.image.load(r"RC24\git_project1\Flappy-bird\assets\sprites\bluebird-upflap.png")]


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

bird_group = pg.sprite.Group()
bird_group.add(bird)



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

pg.quit()
