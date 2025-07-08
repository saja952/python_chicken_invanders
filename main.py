import pygame
import sys
from pygame import mixer
import random
import pygame.font
from tkinter import Tk, Button



def start_game():
    global countdown
    countdown = 3
    root.destroy()


def show_play_button():
    global root
    root = Tk()
    root.title("Play Game")
    root.geometry("400x200")

    play_button = Button(root, text="Play", command=start_game)
    play_button.pack()

    root.mainloop()

show_play_button()

pygame.init()
clock = pygame.time.Clock()
fps = 60


screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('chicken Invanders SAJA ')



font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)



#sound_exp = pygame.mixer.Sound(r"C:\Users\Asus\Desktop\saja_game\laser.wav")
#sound_exp.set_volume(0.25)

#sound_bullet = pygame.mixer.Sound(r"C:\Users\Asus\Desktop\saja_game\laser.wav")
#sound_bullet.set_volume(0.25)

#sound_fs = pygame.mixer.Sound(r"C:\Users\Asus\Desktop\saja_game\Retro, Laser Shot 04.wav")
# sound_fs.set_volume(0.25)

rows = 3
cols = 6
chicken_cooldown = 5000
last_chicken_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0  #0 is no game over, 1 means player has won, -1 means player has lost


red = (255, 0, 0)
green = (0, 255, 0)
white= (255, 255, 255)




bg = pygame.image.load("bg2.jpg")

icon_image=pygame.image.load("Chicken.jpg")
pygame.display.set_icon(icon_image)

def draw_bg():
    screen.blit(bg, (0, 0))




score_value = 0
font_score = pygame.font.SysFont('Constantia', 30)

def update_score(value):
    global score_value
    score_value += value

def show_score():
    score_text = font_score.render("Score: " + str(score_value), True, white)
  #  screen.blit(score_text,(10و20





def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('shipp.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        speed = 8
        cooldown = 500
        game_over = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()

        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            #sound_fs.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            self.last_shot = time_now

        self.mask = pygame.mask.from_surface(self.image)

        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosions.add(explosion)
            self.kill()
            game_over = -1
        return game_over


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        global score_value
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, chickens, True):
            self.kill()
            #sound_exp.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosions.add(explosion)
            update_score(10)


class Chicken(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('chi.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 100: ##########
            self.move_direction *= -1
            self.move_counter *= self.move_direction

class Chicken_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('chi_shot.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, ships, False, pygame.sprite.collide_mask):
            self.kill()
           # sound_exp.play()
            #reduce spaceship health
            ship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosions.add(explosion)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load('chi_shot.png')
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))

            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0


    def update(self):
        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


ships = pygame.sprite.Group()
bullets = pygame.sprite.Group()
chickens = pygame.sprite.Group()
chicken_bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()


def create_chickens():
    for row in range(rows):
        for item in range(cols):
            chicken = Chicken(100 + item * 100, 100 + row * 70)
            chickens.add(chicken)

create_chickens()


ship = Ship(int(screen_width / 2), screen_height - 100, 3)
ships.add(ship)

while True:

    clock.tick(fps)
    draw_bg()

    if countdown == 0:

        time_now = pygame.time.get_ticks()

        if time_now - last_chicken_shot > chicken_cooldown and len(chicken_bullets) < 5 and len(chickens) > 0:
            shot_chicken = random.choice(chickens.sprites())
            chicken_bullet = Chicken_Bullets(shot_chicken.rect.centerx, shot_chicken.rect.bottom)
            chicken_bullets.add(chicken_bullet)
            last_chicken_shot = time_now

        if len(chickens) == 0:
            game_over = 1

        if game_over == 0:
            game_over = ship.update()
            bullets.update()
            chickens.update()
            chicken_bullets.update()
        else:
            if game_over == -1:
                draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
            if game_over == 1:
                draw_text('YOU WIN!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))

    if countdown > 0:
        draw_text('GET READY!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    explosions.update()



    ships.draw(screen)
    bullets.draw(screen)
    chickens.draw(screen)
    chicken_bullets.draw(screen)
    explosions.draw(screen)
    show_score()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()



    pygame.display.update()

pygame.quit()