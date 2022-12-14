import pygame
import os
from settings import *
from support import *
from timer import timer

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, group):
    super().__init__(group)

    self.import_assets()
    self.status = "down_idle"
    self.frame_index = 0

    # general setup
    self.image = self.animations[self.status][self.frame_index]
    self.rect = self.image.get_rect(center = pos)

    # movement atrributes
    self.direction = pygame.math.Vector2()
    self.pos = pygame.math.Vector2(self.rect.center)
    self.speed = 200

    # timers
    self.timers = {
      'tool_use': timer(350, self.use_tool)
    }

    # tools
    self.selected_tool = 'water'


  def use_tool(self):
    print(self.selected_tool)


  def import_assets(self):
    self.animations = {'up' : [], 'down' : [], 'left' : [], 'right' : [],
                      'right_idle' : [], 'left_idle' : [], 'up_idle' : [], 'down_idle' : [],
                      'right_hoe' : [], 'left_hoe' : [], 'up_hoe' : [], 'down_hoe' : [],
                      'right_axe' : [], 'left_axe' : [], 'up_axe' : [], 'down_axe' : [],
                      'right_water' : [], 'left_water' : [], 'up_water' : [], 'down_water' : []}
    for animation in self.animations.keys():
      full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphics', 'character\\') + animation
      self.animations[animation] = import_folder(full_path)

  def animate(self,dt):
    self.frame_index += 4 * dt
    if self.frame_index >= len(self.animations[self.status]):
      self.frame_index = 0
    self.image = self.animations[self.status][int(self.frame_index)]

  def input(self):
    keys = pygame.key.get_pressed()

    # direction
    if not self.timers['tool_use'].active:
      if keys[pygame.K_UP]:
        self.direction.y = -1
        self.status = "up"
      elif keys[pygame.K_DOWN]:
        self.direction.y = 1
        self.status = "down"
      else:
        self.direction.y = 0
      
      if keys[pygame.K_LEFT]:
        self.direction.x = -1
        self.status = "left"
      elif keys[pygame.K_RIGHT]:
        self.direction.x = 1
        self.status = "right"
      else:
        self.direction.x = 0


      # tool use

      if keys[pygame.K_SPACE]:
        self.timers['tool_use'].activate()
        self.direction = pygame .math.Vector2()
        self.frame_index = 0

  def get_status(self):
    # idle
    if self.direction.magnitude() == 0:
      self.status = self.status.split('_')[0] + '_idle'

    if self.timers['tool_use'].active:
      self.status = self.status.split('_')[0] + '_' + self.selected_tool
    
  def update_timers(self):
    for timer in self.timers.values():
      timer.update()

  def move(self, dt):

    # normalizing a vector
    if self.direction.magnitude() > 0:
      self.direction = self.direction.normalize()

    # horizontal movement
    self.pos.x += self.direction.x * self.speed * dt
    self.rect.centerx = self.pos.x

    # vertical movement
    self.pos.y += self.direction.y * self.speed * dt
    self.rect.centery = self.pos.y

  def update(self, dt):
    self.input()
    self.get_status()
    self.update_timers()
    self.move(dt)
    self.animate(dt)