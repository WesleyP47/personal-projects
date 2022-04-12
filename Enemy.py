from Fighter import *

class Enemy(Fighter):

  def __init__(self, level = 1,  weapon = "Nothing", item = [], pos = [], chasing = False, maxHealth = 6, attack = 4, defense = 1, speed = 1, char = "母", name = "Tommi", expGain = 1, moveWait = 0, sight = 1, runChance = 1, fullArt = ""):
    Fighter.__init__(self, name, char, level, maxHealth, attack, defense, speed, weapon, item, pos)
    self.expGain = expGain
    self.moveWait = moveWait
    self.chasing = chasing
    self.sight = sight
    self.runChance = runChance

  def killedBy(self, other):
    other.exp += self.expGain
    print(other.name + " Killed " + self.name + " and gained " + str(self.expGain) + " Exp")
      