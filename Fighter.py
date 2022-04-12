import random 
import math

class Fighter:

  def __init__(self, name = "", char = "母", level = 1, maxHealth = 1, attack = 1, defense = 1, speed = 1, weapon = "Nothing", items = [], pos = []):
    self.name = name
    self.char = char
    self.level = level
    self.maxHealth = maxHealth
    self.health = maxHealth
    self.speed = speed
    self.attack = attack
    self.defense = defense
    self.weapon = weapon 
    self.items = items
    self.pos = pos
  

  def __repr__(self):
    return self.name + "\nLevel: " + str(self.level) + "\nHealth: " + str(self.health) + "/" + str(self.maxHealth) + "\nAttack: " + str(self.attack) + "\nDefense " + str(self.defense) + "\nSpeed: " + str(self.speed) + "\nWeapon: " + self.weapon + "\nItems: " + ", ".join(self.items)

  def fight(self, other):
    weaponDamage = 0
    weaponBonus = 0
    
    weaponDamage = weaponDict[self.weapon][0]
    
    if weaponDict[self.weapon][1] != 0:
      weaponBonus = random.randint(1, weaponDict[self.weapon][1])
        
    damage = math.ceil((weaponDamage + weaponBonus) * (math.sqrt(self.attack / other.defense)))
    other.health -= damage
    print(self.name + " dealt " + str(damage) + " damage to " + other.name)
      
        
weaponDict = {
  "Nothing" : [+1, 0],
  "Sword" : [+4, 4, "melee"],
  "Axe" : [+3, 8, "melee"],
  "Stick" : [+1, 4, "melee"],
  "Rapier" : [+2, 8, "melee"],
  "Rock" : [+2, 4, "melee"],
  "Laser Gun" : [+5, 0, "ranged"]
}

weaponAdjDict = {
  "Chipped" : [-2, 0],
  "Polished" : [+3, 0]
}