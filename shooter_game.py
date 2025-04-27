#Создай собственный Шутер!
from random import randint 

from pygame import *

from time import time as timer

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(100, 600)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)
    
win_width, win_height = 700, 500 # создаем окно приложения
window = display.set_mode((win_width, win_height))

display.set_caption('Шутер')
background = transform.scale(image.load('space.png'), (win_width, win_height))

#картинка, координата x, координата y, скорость, размер по x, размер по y
rocket = Player('ufo.png', 300, 445, 10, 100, 50)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('rocket.png', randint(100, 600), -40, randint(2, 7), 60, 60)
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(100, 600), -40, randint(2, 7), 60, 60)
    asteroids.add(asteroid)

life = 3 #счетчик жизней

mixer.init()
mixer.music.load('space.ogg')
# mixer.music.play()
fire = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 36)

game = True
finish = False
clock = time.Clock()
fps = 60

rel_time = False
num_fire = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    rocket.fire()
                    fire.play()
                if rel_time == False and num_fire >= 10:
                    rel_time = True
                    last_time = timer()
                    

    if finish != True:
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
    
        text_score = font1.render('Счет: ' + str(score), 1, (255,255,255))
        text_lost = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))

        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))

        rocket.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprite_list:
            score += 1
            monster = Enemy('rocket.png', randint(100, 600), -40, randint(2, 7), 60, 60)
            monsters.add(monster)
        
        if sprite.spritecollide(rocket, asteroids, True):
            life -= 1
        
        text_life = font1.render('Жизни: ' + str(life), 1, (255,255,255))
        window.blit(text_life, (10, 80))

        if rel_time == True:
            new_time = timer()
            if new_time - last_time < 3:
                reload = font1.render('Перезарядка', 1, (255,255,255))
                window.blit(reload, (250, 450))
            else:
                num_fire = 0
                rel_time = False

        if score == 120:
            finish = True
            font2 = font.Font(None, 70) 
            win = font2.render('YOU WON!', True, (250, 215, 0))
            window.blit(win, (200, 200))

        if lost == 60 or life == 0:
            finish = True
            font2 = font.Font(None, 70) 
            lose = font2.render('YOU LOSE!', True, (255, 215, 0))
            window.blit(lose, (200, 200))

    display.update()
    clock.tick(fps)












