import sys

import pygame as py
from pygame.locals import QUIT
from pygame.time import Clock

level_1 = 'levels/Level 1.png'
py.init()
clock = Clock()
width, height = 512, 500
Surf = py.display.set_mode((width, height))
py.display.set_caption('Geomtry Dash Beta Testing')
#all_sprites_group = py.sprite.Group()
base_path = 'sprites/Base.png'
base_img_reg = py.image.load(base_path)
base_img = py.transform.scale(base_img_reg, (width, 150))
base_rect = base_img.get_rect()
base_rect.bottom = (height + 50)

bg_path = 'sprites/gd_beta_bg.png'
bg_img_reg = py.image.load(base_path)
bg_img = py.transform.scale(base_img_reg, (width, 150))
bg_rect = base_img.get_rect()
bg_rect.center = (height, width)


#prepare spikes for displaying

spike_grp = py.sprite.Group()

#game var
game_speed = 4.5
block_y = height / 2
block_y_vel = 0
gravity = 4
game = True
rotate = False

block_group = py.sprite.Group()

class Block(py.sprite.Sprite):
  def __init__(self):
    super().__init__()
    #Load the sprites into the game
    block_img_path = 'sprites/block.png'
    self.reg = py.image.load(block_img_path)
    self.image = py.transform.scale(self.reg, (50, 50))
    self.rect = self.image.get_rect()
    self.rect.center = (width // 2, height // 2)
    self.mask = py.mask.from_surface(self.image)
    #Game variables
    self.block_y = height / 2
    self.block_y_vel = 0
    self.grounded = False
    self.gravity = 4
  def update(self, *_args, **_kwargs):
    #Update the Block's velocity and its position
    self.block_y += self.block_y_vel
    self.block_y_vel += 0.05
    self.rect.center = (width // 2 - 75, int(self.block_y))
    if self.rect.colliderect(base_rect):
      self.grounded = True
      self.gravity = 0.0
      self.block_y_vel = 0
    if not self.rect.colliderect(base_rect):
      self.grounded = False
    if block.mask.overlap(stereo.mask, (block.rect.x - stereo.rect.x, block.rect.y - stereo.rect.y)):
      self.grounded = True
      self.gravity = 0.0
      self.block_y_vel = 0
    if not block.mask.overlap(stereo.mask, (block.rect.x - stereo.rect.x, block.rect.y - stereo.rect.y)):
      self.grounded = False

      
  def draw(self):
    Surf.blit(self.image, self.rect)
class Spike(py.sprite.Sprite):

  def __init__(self, color, height, width):
    super().__init__()

    # self.image = pygame.Surface([width, height])
    self.image = py.image.load('sprites/Spike.png').convert_alpha()
    self.image.set_colorkey(color)
    # pygame.draw.rect(self.image,
    #             color,
    #             pygame.Rect(0, 0, width, height))
    self.rect = self.image.get_rect()
    self.rect.size = (width, height)
    self.mask = py.mask.from_surface(self.image)

  def update(self, *_args, **_kwargs):
    self.rect.x -= int(game_speed)
    self.rect.bottom = base_rect.top 
class Level(py.sprite.Sprite):
  def __init__(self, path):
    super().__init__()
    self.image = py.image.load(str(path))
    self.rect = self.image.get_rect()
    self.rect.size = (300, 300)
    self.mask = py.mask.from_surface(self.image)
  def update(self, *_args, **_kwargs):
    self.rect.x -= int(game_speed)
    self.rect.bottom = base_rect.top
  def draw(self):
    Surf.blit(self.image, self.rect)
    self.update()



stereo = Level(level_1)




def spawn_spikes():
  new_spike = Spike("teal", 40, 40)
  spike_grp.add(new_spike)
  new_spike.rect.center = 590, 0
  print("spawning new spike")


spawn_spikes()
block = Block()
block_group.add(block)
while game:
  #Handle Event
  for event in py.event.get():
    if event.type == QUIT:
      py.quit()
      sys.exit()
    if event.type == py.MOUSEBUTTONDOWN and block.grounded is True:
      block.block_y_vel = -2
      block.gravity = 0.02
      grounded = False 
    block_group.update()
      

  if block.rect.colliderect(base_rect):
    block.gravity = 0
    block.block_y_vel = 0
    block.grounded = True
  for spike in spike_grp:
    if block.mask.overlap(spike.mask, (block.rect.x - spike.rect.x,  block.rect.y -\
                                       spike.rect.y)):
      print("You Died")
      py.time.wait(500)
      spike.kill()
      spawn_spikes()
  #block jumping
  keys = py.key.get_pressed()
  if keys[py.K_SPACE] and block.grounded is True:
    block.block_y_vel = -2
    block.gravity = 0.02
    grounded = False 
  block_group.update()
  #blit sprites into surface
  spike_grp.update()
  
  Surf.fill((244, 250, 252))
  Surf.blit(bg_img, bg_rect)
  spike_grp.draw(Surf)
  Surf.blit(bg_img, bg_rect)
  for spike in spike_grp:
    if spike.rect.right < 0:
      spike.kill()
      spawn_spikes()
  Surf.blit(base_img, base_rect)
  block_group.draw(Surf)
  # stereo.draw()
  clock.tick(100)
  py.display.update()