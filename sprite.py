import pygame as pg
from settings import *
from pygame.sprite import Sprite
from utils import *
from os import path
vec = pg.math.Vector2
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite,group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite,group,False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite,group,False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.width / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.width
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

# create player class with Sprite as super class

# def collide_hit_rect(one,two):
#     return one.hit_rect.colliderect(two.rect)

# def collide_with_walls(sprite, group, dir):
#     if dir == 'x':
#         hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
#         if hits:
#             if hits[0].rect.centerx > sprite.hit_rect.centerx:
#                 sprite.pos.x = hits[0].rect.left = sprite.hit_rect.width / 2
#             if hits[0].rect.centerx < sprite.hit_rect.centerx:
#                 sprite.pos.x = hits[0].rect.right = sprite.hit_rect.width /2
#             sprite.vel.x = 0
#             sprite.hit_rect.centerx = sprite.pos.x
#     if dir == 'y':
#         pass

class Player(Sprite):
    def __init__(self,game,x,y):
         self.groups = game.all_sprite
         Sprite.__init__(self, self.groups)
         self.game = game 
         #provides us with raster images for use in animation or otherwise
         self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_shet.png"))
         self.image = pg.Surface((TILESIZE, TILESIZE))
         self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        #  self.image.fill(WHITE)
         self.rect = self.image.get_rect()
         self.rect.x = x
         self.rect.y = y
         self.hit_rect = PLAYER_HIT_RECT
         self.vel = vec(0,0)
         self.pos = vec(x,y) * TILESIZE
                 # start with current frames and last update at 0 so we can cycle thorugh animations
         self.current_frame = 0
         self.last_update = 0
         # accounting for states of player
         self.jumping = False
         self.moving = False
         print("player instance created")
         self.load_images()

    #gets player input
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            # self.vx = -PLAYER_SPEED
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_s]:
            # self.vy = PLAYER_SPEED
            self.vel.y = PLAYER_SPEED
        if keys[pg.K_d]:
            # self.vx = PLAYER_SPEED
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            # self.vy = -PLAYER_SPEED
            self.vel.y = -PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        

    def jump(self):
        pass
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0, TILESIZE,TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            #determines when to display next frame
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
    def update(self):
        self.get_keys()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center
        # these break it, fix later
        self.rect.center = self.hit_rect.center
        
    

class Wall(Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprite, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game 
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx, self.vy = 0,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("crated")