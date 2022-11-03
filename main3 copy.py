#Sources: 
    #https://stackoverflow.com/questions/43587734/how-to-spawn-a-sprite-after-a-time-limit-and-how-to-display-a-timer-pygame
    # ^used for mob spawn in timer
# import libraries and modules
# from platform import platform
from copyreg import remove_extension
from tkinter import Y, font
from unicodedata import combining
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import time
import sys 


# game settings 
WIDTH = 500
HEIGHT = 800
FPS = 30


vec = pg.math.Vector2
        

# player settings
PLAYER_GRAV = 0.8
PLAYER_FRIC = 0.025
SCORE = 0

#platform settings
PLATFORM_GRAV = 0.1

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pg.display.set_mode((800, 800),0,32)
def draw_text(text, size, color, x, y):
            font_name = pg.font.match_font('arial')
            txtfont = pg.font.Font(font_name, size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
            screen.blit(text_surface, text_rect)
 
# A variable to check for the status later
click = False
 
# Main container function that holds the buttons and game functions

def main_menu():


    while True:

        screen.fill(WHITE)
        draw_text('Main Menu', txtfont, BLUE, 250, 40)
 
        mx, my = pg.mouse.get_pos()

        #creating buttons
        button_1 = pg.Rect(200, 100, 200, 50)
        button_2 = pg.Rect(200, 180, 200, 50)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                rules()
        pg.draw.rect(screen, (255, 0, 0), button_1)
        pg.draw.rect(screen, (255, 0, 0), button_2)
 
        #writing text on top of button
        draw_text('PLAY', font, (255,255,255), screen, 270, 115)
        draw_text('OPTIONS', font, (255,255,255), screen, 250, 195)


        # click = False
        # for event in pg.event.get():
        #     if event.type == QUIT:
        #         pg.quit()
        #         sys.exit()
        #     if event.type == KEYDOWN:
        #         if event.key == K_ESCAPE:
        #             pg.quit()
        #             sys.exit()


def rules():
    
    screen = pg.display.set_mode((600, 300),0,32)
    screen.fill(WHITE)
    draw_text("The Rules are simple: ", 50, BLACK, WIDTH / 2, HEIGHT / 2)

    


def game():
    endcount = 0

    def draw_text(text, size, color, x, y):
            font_name = pg.font.match_font('arial')
            font = pg.font.Font(font_name, size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
            screen.blit(text_surface, text_rect)

    def colorbyte(): 
        return random.randint(0,255)

    # sprites...
    class Player(Sprite):
        def __init__(self):
            Sprite.__init__(self)
            self.image = pg.Surface((50, 50))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH/2, HEIGHT/2)
            self.pos = vec(WIDTH/2, HEIGHT/2)
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            # self.rect.x = x
            # self.rect.y = y
            
        def controls(self):
            keys = pg.key.get_pressed()
            # if keys[pg.K_w]:
            #     self.acc.y = -5
            if keys[pg.K_a]:
                self.acc.x = -3
            # if keys[pg.K_s]:
            #     self.acc.y = 5
            if keys[pg.K_d]:
                self.acc.x = 3
        def jump(self):
            # self.rect.x += 1
            hits = pg.sprite.spritecollide(self, all_plats, True)
            # self.rect.x += -1
        
            # while hits == True: 
            #     PLATFORM_GRAV == 0
            if hits:
                self.vel.y = -15
        def update(self):
            self.acc = vec(0,PLAYER_GRAV)
            self.controls()
            
            self.acc.x += self.vel.x * -0.2
            self.vel += self.acc
            self.pos += self.vel 
            self.rect.midbottom = self.pos

            if self.rect.x < 0:
                self.pos*=-1
            if self.rect.y < 0:
                self.vel*=-1  

            # if self.rect.x == WIDTH - self.rect.width:
            #     self.pos*=-1
            # if self.rect.y == HEIGHT - self.rect.height:
            #     self.pos*=-1
            if self.rect.x > WIDTH - self.rect.width: 
                self.pos*=-1
            if self.rect.y >= HEIGHT + self.rect.height:
                # self.kill()
                screen.fill(WHITE)
                draw_text("YOU LOST  :( ", 50, BLACK, WIDTH / 2, HEIGHT / 2)
                pg.display.update()
                pg.time.delay(5000)
                # time.sleep(5)
                pg.quit()
                

    # platforms
    class Platform(Sprite):
        def __init__(self, x, y, w, h):
            Sprite.__init__(self)
            self.image = pg.Surface((w, h))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.vel = vec(0,0)
            self.acc = vec(0,0)
            self.pos = vec(WIDTH/2, HEIGHT/2)
        def update(self):
            self.rect.y += 2.5
            if self.rect.y > HEIGHT - self.rect.height:
                self.kill()

            #Platform Gravity####################
            # self.acc = vec(0,PLATFORM_GRAV)
            # self.acc.x += self.vel.x * -0.001
            # self.vel += self.acc
            # self.pos += self.vel
            # self.rect.midbottom = self.pos

            #self.rect.y += .5
            # self.vel += self.acc
            # self.pos += self.vel + 0.5 * self.acc

    # movingplat = Platform(200,150,200,150) 
    # def movingplat =

    class MovingPlat(Platform):
        def __init__(self, x, y, w, h, color):
            Sprite.__init__(self)
            self.image = pg.Surface((w, h))
            self.color = color
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.rect.center = (WIDTH/2, HEIGHT/2)
            self.pos = vec(WIDTH/2, HEIGHT/2)
            self.vel = vec(0,0)
            self.acc = vec(0,0)
        def update(self):
                self.rect.y += 2.5
                self.rect.x += 1 
                if self.rect.y > HEIGHT - self.rect.height:
                    self.kill()
            # self.acc = vec(0,PLATFORM_GRAV)
            # self.acc.x += self.vel.x * -0.001
            # self.vel += self.acc
            # self.pos += self.vel 

            # self.rect.midbottom = self.pos
        #     #self.rect.x += random.randint(-3,3)
        #     self.rect.x += 1
        #     self.rect.x -+ 1
        #     self.rect.y += -0.8

    
        
    class Mob(Sprite):
        def __init__(self, x, y, w, h, color):
            Sprite.__init__(self)
            self.image = pg.Surface((w, h))
            self.color = color
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        def reset_pos(self):
            self.rect.y = randint(0,20)
            self.rect.x = randint(50,300)
        def update(self):
            self.rect.y += 4
            if self.rect.y > 800: 
                self.reset_pos()

            


    # init pygame and create a window
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Game...")
    clock = pg.time.Clock()
    
    # create groups
    all_sprites = pg.sprite.Group()
    all_plats = pg.sprite.Group()
    mobs = pg.sprite.Group()

    # instantiate classes
    player = Player()
    plat = Platform(50, 150, 75, 25)
    plat2 = Platform(289, 150, 75, 25)
    movplat1 = MovingPlat(0,1,75,25, BLUE)


    m = Mob(randint(50,300), randint(0,20), 25, 25, (colorbyte(),colorbyte(),colorbyte()))
    all_sprites.add(m)
    mobs.add(m)


    # print(m)

    # for i in range(SCORE):

        # m = Platform(randint(0,WIDTH), randint(0,HEIGHT), 100, 25)
        # all_sprites.add(m)
        # all_plats.add(m)
        # print(m)


    # done = False

    # while not done:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             done = True

    #         # Decrease timer to get a countdown.
    #         timer -= dt
    #         # When the timer is below or equal to 0, we spawn
    #         # a new block.
    #         if timer <= 0:
    #             all_sprites.add(m)
    #             all_plats.add(m)
    #             print(m)
    #             # Reset the countdown timer to one second.
    #             timer = 1
        

    #         pg.display.flip()
    #         # dt = time in seconds that passed since last tick.
    #         # Divide by 1000 to convert milliseconds to seconds.
    #         dt = clock.tick(30) / 1000



    # add player to all sprites group
    all_sprites.add(player)
    all_plats.add(plat, plat2)

    # add platform to all sprites group
    all_sprites.add(plat)
    all_sprites.add(plat2)

    # add things to their respective groups
    all_plats.add(movplat1)

    # def mobcountspawn(): 
    #     m = Mob(randint(50,450), 0, 25, 25, (colorbyte(),colorbyte(),colorbyte()))
    #     all_sprites.add(m)
    #     mobs.add(m)
    #     time.sleep(4)
    #     print('Mob has spawned')

    # for i in range(100,0,-1):
    #     m = Mob(randint(50,450), 0, 25, 25, (colorbyte(),colorbyte(),colorbyte()))
    #     all_sprites.add(m)
    #     mobs.add(m)
    #     print('Mob has spawned')
    #     time.sleep(4)

        


    # Game loop
    running = True
    while running:
        # keep the loop running using clock
        clock.tick(FPS)

        hits = pg.sprite.spritecollide(player, all_plats, False)
        if hits:
            player.pos.y = hits[0].rect.top
            player.vel.y = 5
        mobhits = pg.sprite.spritecollide(player, mobs, True)
        if mobhits:
            SCORE += 1
            p = Platform(randint(50,300), 0, 100, 25)
            all_plats.add(p)
            # print(m)

            mp = MovingPlat(randint(50,100),300,75,25, BLUE)
            all_plats.add(mp)
            

            m = Mob(randint(50,450), 0, 25, 25, (colorbyte(),colorbyte(),colorbyte()))
            all_sprites.add(m)
            mobs.add(m)
            # print(m)

        # while running:
        #     time.sleep(5)
        #     m = Mob(randint(50,450), 0, 25, 25, (colorbyte(),colorbyte(),colorbyte()))
        #     all_sprites.add(m)
        #     mobs.add(m)

        # guppyspawncount = 0
        # while guppyspawncount == 0:
        #     if self.rect.y >= HEIGHT: #- self.rect.height: 
        #         m = Mob(randint(50,300), randint(0,20), 25, 25, (colorbyte(),colorbyte(),colorbyte()))
        #         all_sprites.add(m)
        #         mobs.add(m)
        #         guppyspawncount == 1
        # # guppyspawncount -=1

        for event in pg.event.get():
            # check for closed window
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    player.jump()
            
        ############ Update ##############
        # update all sprites
        all_sprites.update()
        all_plats.update()
        pg.display.update()

        ############ Draw ################
        # draw the background screen
        screen.fill(BLACK)
        # draw text
        draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
        # draw_text("Next Orb Spawn In: " + str(timer), 22, WHITE, 100, 25)
        # draw all sprites
        all_sprites.draw(screen)
        all_plats.draw(screen)

        # buffer - after drawing everything, flip display
        pg.display.flip()

main_menu()


