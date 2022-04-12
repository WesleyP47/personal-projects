from Fighter import *
import math
import random

class Player(Fighter):

  def __init__(self, name = "Tommi", weapon = "Sword", items = [], pos = [1, 0], char = "웃", maxHealth = 20, attack = 12, defense = 9, speed = 8, level = 1, exp = 0, maxExp = 15, orient = "right"):
    Fighter.__init__(self, name, char, level, maxHealth, attack, defense, speed, weapon, items, pos)

    self.exp = exp
    self.maxExp = maxExp
    self.pos = pos
    self.orient = orient

  def __repr__(self):
    return Fighter.__repr__(self) + "\nExp: " + str(self.exp) + "\nExp to next Lvl: " + str(self.maxExp - self.exp)

  def die(self):
    print(self.name + " has died.")
    self.__init__(self.name)
    
  def levelUp(self):
    healthUp = random.choices((2, 3, 4), weights = (3, 5, 2), k = 1)[0]
    attackUp = random.choices((1, 2, 3), weights = (4, 4, 2), k = 1)[0]
    defenseUp = random.randint(1, 3)
    speedUp = random.choices((0, 1, 2), weights = (1, 6, 3), k = 1)[0]
    
    self.level += 1
    self.exp -= self.maxExp
    self.maxExp += math.ceil(self.maxExp/3)
    self.maxHealth += healthUp
    self.health = self.maxHealth
    self.attack += attackUp
    self.defense += defenseUp
    self.speed += speedUp

    print(self.name + " Leveled Up!")
    print(self.name + "\nHealth: +" + str(healthUp) + "\nAttack: +" + str(attackUp) + "\nDefense: +" + str(defenseUp) + "\nSpeed: +" + str(speedUp))
    
    
    
  