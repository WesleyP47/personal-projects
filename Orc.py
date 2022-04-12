from Enemy import *
import random
import math

class Orc(Enemy):
  def __init__(self, level = 1,  weapon = "Stick", pos = [], item = [], chasing = False, maxHealth = 13, attack = 10, defense = 4, speed = 8, char = "G", name = "Goblin", expGain = 2, moveWait = 0, sight = 5, runChance = 70):
    Enemy.__init__(self, level, weapon, item, pos, chasing, maxHealth, attack, defense, speed, char, name, expGain, moveWait, sight, runChance)
    self.fullArt = r"""             ,      ,
            /(.-""-.)\
        |\  \/      \/  /|
        | \ / =.  .= \ / |
        \( \   o\/o   / )/
         \_, '-/  \-' ,_/
           /   \__/   \
           \ \__/\__/ /
         ___\ \|--|/ /___
       /`    \      /    `\
      /       '----'       \
    """
    
    for i in range(0, self.level):
      self.maxHealth += random.randint(2, 3)
      self.attack += random.choices((1, 2, 3), weights = (5, 2, 1), k = 1)[0]
      self.defense += random.choices((0, 1, 2), weights = (3, 7, 1), k = 1)[0]
      self.speed += random.choices((1, 2, 4), weights = (2, 6, 1), k = 1)[0]
      if self.runChance > 45:
        if random.randint(1, 3) == 1:
          self.runChance -= 5
      if self.expGain < 20:
        self.expGain += 2
        
    self.health = self.maxHealth 