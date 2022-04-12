import random
import math
import time
from getkey import getkey,keys
from Fighter import *
from Player import *
from Enemy import *
from Goblin import *

def clear():
  print("\033[H\033[J", end="")

def useItem(user, item, other = "ClassInstance"):
  clear()
  if item == "Potion":
    user.health += 5
    if user.health > user.maxHealth:
      print(user.name + " used the Potion and gained " + str(5 - (user.health - user.maxHealth)) + " health")
      user.health = user.maxHealth
    else:
      print(user.name + " used the Potion and gained 5 health")

  elif item == "Throwing Knife":
    
    if other == "ClassInstance":
      whatHit = detect(user.pos, [], 7, "obstruction", player.orient)
      
      if whatHit[1] == "enemy":
        other = whatHit[0]
        other.health -= 15
        print(user.name + " used the Throwing Knife and did 15 damage to " + other.name)
        if other.health <= 0:
          other.killedBy(user)
          enemiesList.remove(whatHit[0])
          if user.exp >= user.maxExp:
            user.levelUp()
            getkey()
            
      elif whatHit[1] == "rock" or whatHit == "out of range":
        print("You missed")
        
      elif whatHit[1] == "box":
        boxesPos.remove(whatHit[0])
        worldMap[whatHit[0][1]][whatHit[0][0]] = mapBase
    else:
      other.health -= 15
      print(user.name + " used the Throwing Knife and did 15 damage to " + other.name)
    
  time.sleep(.75)

def itemNav(player, enemy = "ClassInstance"):
  itemsCopy = player.items.copy()
  itemMenu = []
  
  while True:
    if itemsCopy != []:
      newItem = itemsCopy[0]
      itemMenu.append([newItem, str(itemsCopy.count(newItem))])
      itemsCopy = list(filter(lambda x: x != newItem, itemsCopy))
    else:
      break

  itemSelection = 0
  itemMenu[itemSelection][0] = ">" + itemMenu[itemSelection][0]
  
  while True:
    clear()
    for itemVal in itemMenu:
      print(itemVal[0] + " x" + itemVal[1])
    print("Left or A to go back")
    upDown = getkey()
    
    if upDown == keys.LEFT or upDown == "a":
      return "exited"
      
    elif upDown == keys.UP or upDown == "w":
      itemMenu[itemSelection][0] = itemMenu[itemSelection][0][1:]
      if itemSelection > 0:
        itemSelection -= 1
      else:
        itemSelection = len(itemMenu) - 1
  
    elif upDown == keys.DOWN or upDown == "s":
      itemMenu[itemSelection][0] = itemMenu[itemSelection][0][1:]
      if itemSelection < len(itemMenu) - 1:
        itemSelection += 1
      else:
        itemSelection = 0
  
    elif upDown == keys.SPACE:
      usedItem = itemMenu[itemSelection][0][1:]
      useItem(player, usedItem, enemy)
      player.items.remove(usedItem)
      time.sleep(.75)
      return "usedItem"

    else:
      continue
      
    itemMenu[itemSelection][0] = ">" + itemMenu[itemSelection][0] 

def doCombat(player, enemy):
  # options: Attack, Inspect, Items, Run, Player
  optionsList = [">Attack", "Items", "Inspect", "Run", "Player"]
  selection = 0
  while True:
    clear()
    print(enemy.fullArt)
    print(enemy.name)
    print(str(enemy.health) + "/" + str(enemy.maxHealth))
    print("-" * 50)
    print(player.name)
    print(str(player.health) + "/" + str(player.maxHealth))
    print()
    print("    ".join(optionsList))



    playerInput = getkey()
    if playerInput == keys.RIGHT or playerInput == "d":
      optionsList[selection] = optionsList[selection][1:]
      if selection < len(optionsList) - 1:
        selection += 1
      else:
        selection = 0
      optionsList[selection] = ">" + optionsList[selection]
      
    elif playerInput == keys.LEFT or playerInput == "a":
      optionsList[selection] = optionsList[selection][1:]
      if selection > 0:
        selection -= 1
      else:
        selection = len(optionsList) - 1
      optionsList[selection] = ">" + optionsList[selection]
      
    elif playerInput == keys.SPACE:
      if selection == 0:
        clear()
        
        if player.speed > enemy.speed:
          player.fight(enemy)
          time.sleep(.75)
          if enemy.health <= 0:
            enemy.killedBy(player)
            time.sleep(.75)
            if player.exp >= player.maxExp:
              player.levelUp()
              getkey()
            break
          enemy.fight(player)
          time.sleep(.75)
          if player.health <= 0:
            break

        else:
          enemy.fight(player)
          time.sleep(.75)
          if player.health <= 0:
            break
          player.fight(enemy)
          if enemy.health <= 0:
            enemy.killedBy(player)
            time.sleep(.75)
            if player.exp >= player.maxExp:
              player.levelUp()
              getkey()
            break
          time.sleep(.75)
          
      elif selection == 1:
        clear()
        if player.items == []:
          print("You don't have any items")
          time.sleep(.75)
        else:
          if itemNav(player, enemy) == "usedItem": 
            if player.health <= 0:
              break
            elif enemy.health <= 0:
              enemy.killedBy(player)
              time.sleep(.75)
              if player.exp >= player.maxExp:
                player.levelUp()
                getkey()
              break
            enemy.fight(player)
            time.sleep(.75)
            if player.health <= 0:
              break
          
            
      elif selection == 2:
        clear()
        print(enemy)
        print("Press any button to exit")
        getkey()
      elif selection == 3:
          clear()
          if random.randint(1, 100) in range(1, enemy.runChance):
            print("You escaped")
            enemy.moveWait = 3
            time.sleep(1)
            break
          else:
            print("You failed to escape")
            time.sleep(.5)
            enemy.fight(player)
            time.sleep(.75)
            if player.health <= 0:
              break
            
      elif selection == 4:
        clear()
        print(player)
        print("Press any button to exit")
        getkey()
        
 
# END OF FIGHTING FUNCTIONS

def printMap(playerX = 0, playerY = 0):
  for y_of_Line, line in enumerate(worldMap):
    
    for enemy in enemiesList:
      if y_of_Line == enemy.pos[1]:
        line = line[:enemy.pos[0]] + [enemy.char] + line[enemy.pos[0] + 1:]
    
    if y_of_Line == playerY:
      line = line[:playerX] + [playerChar] + line[playerX + 1:]
    print(" ".join(line))
    
  print("Level " + str(level))

def canMove(originalX = 0, originalY = 0, xChange = 0, yChange = 0, objectType = ""):
  newX = originalX + xChange
  newY = originalY + yChange
  newPos = [newX, newY]

  if newY < 0 or newY > mapHeight - 1 or newX < 1 or newX > mapLength:
    return False

  if newPos == doorPos:
    if objectType == "player":
      return True
    elif objectType == "box":
      boxesPos.remove([originalX, originalY])
      worldMap[originalY][originalX] = mapBase
      return False
    else:
      return False

  if objectType == "enemy":
    for enemy in enemiesList:
      if [newX, newY] == enemy.pos:
        enemy.chasing = True
        return False
  
  if objectType == "box":
    if newPos == player.pos:
      return False
    for enemy_index, enemy in enumerate(enemiesList):
      if newPos == enemy.pos:
        if canMove(enemy.pos[0], enemy.pos[1], xChange, yChange, "enemy"):
          enemiesList[enemy_index].pos = [enemy.pos[0] + xChange, enemy.pos[1] + yChange]
          enemy.chasing = True
          return True
        else:
          return False

  for rock in rocksPos:
    if rock == newPos:
      return False
  
  for box_index, box in enumerate(boxesPos):
    if box == newPos:
      if canMove(box[0], box[1], xChange, yChange, "box"):
        worldMap[box[1]][box[0]] = mapBase
        boxesPos[box_index][0] += xChange
        boxesPos[box_index][1] += yChange
        box = [boxesPos[box_index][0], boxesPos[box_index][1]]
        worldMap[box[1]][box[0]] = boxChar
      else:
        return False

  return True

def chase(chaserPos = [], targetPos = [], type = ""):
  chaserX = chaserPos[0]
  chaserY = chaserPos[1]
  targetX = targetPos[0]
  targetY = targetPos[1]

  if abs(chaserX - targetX) > abs(chaserY - targetY):
    if chaserX < targetX and canMove(chaserX, chaserY, 1, 0, type):
      chaserX += 1
      return [chaserX, chaserY]
    elif chaserX > targetX and canMove(chaserX, chaserY, -1, 0, type):
      chaserX -= 1
      return [chaserX, chaserY]
      
  elif abs(chaserY - targetY) > abs(chaserX - targetX):
    if chaserY < targetY and canMove(chaserX, chaserY, 0, 1, type):
      chaserY += 1
      return [chaserX, chaserY]
    elif chaserY > targetY and canMove(chaserX, chaserY, 0, -1, type):
      chaserY -= 1
      return [chaserX, chaserY]
  else:
    return [chaserX, chaserY]

  while True:
    randDi = random.randrange(4)
    if randDi == 0 and canMove(chaserX, chaserY, 1, 0, type):
      chaserX += 1
      break
    elif randDi == 1 and canMove(chaserX, chaserY, -1, 0, type):
      chaserX -= 1
      break
    elif randDi == 2 and canMove(chaserX, chaserY, 0, 1, type):
      chaserY += 1
      break
    elif canMove(chaserX, chaserY, 0, -1, type):
      chaserY -= 1
      break

  return [chaserX, chaserY]

def detect(userPos = [], targetPos = [], detectRange = 1, returnType = "tf", direction = "all"):
  if targetPos == [] and returnType == "obstruction":
    if direction == "up":
      targetPos = [userPos[0], userPos[1] - detectRange]
    elif direction == "down":
      targetPos = [userPos[0], userPos[1] + detectRange]
    elif direction == "left":
      targetPos = [userPos[0] - detectRange, userPos[1]]
    elif direction == "right":
      targetPos = [userPos[0] + detectRange, userPos[1]]
      
  xDiff = targetPos[0] - userPos[0]
  yDiff = targetPos[1] - userPos[1]
  path = []
  
  # are both of the things are on the same horizontal line?
  if xDiff == 0 and abs(yDiff) <= detectRange:
    # is the target above or below the user?
    if yDiff < 0 and direction == "up" or yDiff < 0 and direction == "all":
      # create a list of positions between the target and user
      for i in range(1, abs(yDiff) + 1):
        path.append([userPos[0], userPos[1] - i])
    elif direction == "down" or direction == "all":
      # create a list of positions between the target and user
      for i in range(1, yDiff + 1):
        path.append([userPos[0], userPos[1] + i])
        
  elif yDiff == 0 and abs(xDiff) <= detectRange:
    # is the target behind or in front of the user?
    if xDiff < 0 and direction == "left" or xDiff < 0 and direction == "all":
      # create a list of positions between the target and user
      for i in range(1, abs(xDiff) + 1):
        path.append([userPos[0] - i, userPos[1]])
    elif direction == "right" or direction == "all":
      # create a list of positions between the target and user
      for i in range(1, xDiff + 1):
        path.append([userPos[0] + i, userPos[1]])

  if path != []:
    for pathPos in path:
      for rock in rocksPos:
        if rock == pathPos:
          if returnType == "tf":
            return False
          elif returnType == "obstruction":
            return rock + ["rock"]
      for box in boxesPos:
        if box == pathPos:
          if returnType == "tf":
            return False
          elif returnType == "obstruction":
            return box + ["box"]
      for enemy in enemiesList:
        if enemy.pos == pathPos:
          if returnType == "tf":
            return False
          elif returnType == "obstruction":
            return [enemy] + ["enemy"]
  else:
    if returnType == "tf":
      return False
    elif returnType == "obstruction":
      return "out of range"

  if returnType == "tf": 
    return True
  elif returnType == "obstruction":
    return "No obstructions"
      

def createNewMap():
  global player
  global doorPos
  global worldMap
  global rocksPos
  global boxesPos
  global enemies
  global enemyAmount
  global enemiesList
  global everyPos
  global pickupsPos
  player.pos[0] = 1
  player.pos[1] = 0
  doorPos = []
  worldMap = []
  rocksPos = []
  boxesPos = []
  everyPos = []
  pickupsPos = []
  enemiesList = []


  for yVal in range(mapHeight):
    for xVal in range(1, mapLength + 1):
      everyPos.append([xVal, yVal])

  doorPos = everyPos.pop(-1)

  # gets rid of the top Left and bottom right corners as possible
  # places for obstacles - prevents softlocks
  del everyPos[mapLength:mapLength + 2]
  del everyPos[:2]
  del everyPos[mapLength * -1 - 1 : mapLength * -1 + 1]
  del everyPos[-1]

  # creates enemy position 
  for i in range(enemyAmount):
    enemiesList.append(Goblin(random.randint(1, level)))
    enemiesList[-1].pos = everyPos.pop(random.randrange(0, len(everyPos)))
    
  # Generates Rocks
  for i in range(rocksAmount):
    rocksPos.append(everyPos.pop(random.randrange(0, len(everyPos))))

  # Generates Boxes
  for i in range(boxesAmount):
    boxesPos.append(everyPos.pop(random.randrange(0, len(everyPos))))

  # Generates Pickups
  for i in range(pickupsAmount):
    pickupsPos.append(everyPos.pop(random.randrange(0, len(everyPos))))
    
  # Starts with the left border
  baseLine = ["|"]

  # Creates the base line of the map, which every line will be based on
  for i in range(mapLength):
    baseLine += [mapBase]

  # Adds the Right border
  baseLine += ["|"]

  for i in range(mapHeight):
    worldMap.append(baseLine.copy())

  for rock in rocksPos:
    worldMap[rock[1]][rock[0]] = rockChar
  
  for box in boxesPos:
    worldMap[box[1]][box[0]] = boxChar

  for pickup in pickupsPos:
    worldMap[pickup[1]][pickup[0]] = pickupChar

  # Adds the door
  worldMap[-1][-2] = doorChar


# Ħ ȸ Ѫ ѫ Ѧ Ѿ  ҈ Ҩ 	Ӂ ←	↑	→	↓ ⇒ ⇓ ⇐ ⇑ ⊕ ඞ	⊖	⊗	⊘	⊙⊚ ⌛ ⏔	⏕ ⚲ 🚪 ⚳ ⛐ ✨▪ ■
# mapping and movement stuff

worldMap = []
level = 1
playerChar = "⇒"
rockChar = "■"
boxChar = "▧"
mapBase = "-"
doorChar = "E"
mapLength = 30
mapHeight = 20
rocksAmount = 20
rocksPos= []
everyPos = []
doorPos = []
boxesAmount = 40
boxesPos = []
enemyAmount = 8
enemiesList = []

# Fighting Stuff
player = Player("Wesl", "Sword", [], [1, 0])
player.pos = [1, 0]
pickupsList = ["Potion", "Throwing Knife"]
pickupsAmount = 5
pickupsPos = []
pickupChar = "⊚"

# Funny little timer
startTime = time.time()

createNewMap()
printMap(player.pos[0], player.pos[1])

# THE ACTUAL GAME
while True:
  move = getkey()

  # Move UP
  if move == "w" or move == keys.UP:
    playerChar = "⇑"    
    player.orient = "up"
    if canMove(player.pos[0], player.pos[1], 0, -1, "player"):
      player.pos[1] -= 1

  # Move Down
  elif move == "s" or move == keys.DOWN:
    playerChar = "⇓"
    player.orient = "down"
    if canMove(player.pos[0], player.pos[1], 0, 1, "player"):
      player.pos[1] += 1

  # Move Left
  elif move == "a" or move == keys.LEFT:
    playerChar = "⇐"
    player.orient = "left"
    if canMove(player.pos[0],player.pos[1], -1, 0, "player"):
      player.pos[0] -= 1

  # Move Right
  elif move == "d" or move == keys.RIGHT:
    playerChar = "⇒"
    player.orient = "right"
    if canMove(player.pos[0],player.pos[1], 1, 0, "player"):
      player.pos[0] += 1

  # Open item menu - don't progress anything else
  elif move == "i":
    if player.items != []:
      itemNav(player)
      clear()
      printMap(player.pos[0], player.pos[1])
    else:
      print("You don't have any items")
    continue

  # Open player stats - don't progress anything else
  elif move == "p":
    clear()
    print(player)
    print("Press any key to exit")
    getkey()
    clear()
    printMap(player.pos[0], player.pos[1])
    continue
    
  # Don't do anything if an invalid key is pressed
  else:
    continue
  
  if player.pos == doorPos:
    level += 1
    createNewMap()

  for enemy in enemiesList:
    if enemy.chasing:
      if enemy.moveWait <= 0:
        if abs(math.sqrt(((enemy.pos[0] - player.pos[0])**2) + ((enemy.pos[1] - player.pos[1])**2))) <= 6:
          enemy.pos = chase(enemy.pos, player.pos, "enemy")
        else:
          enemy.chasing = False
          
      else:
        enemy.moveWait -= 1
      
    elif detect(enemy.pos, player.pos, enemy.sight, "tf"):
      enemy.chasing = True
      enemy.pos = chase(enemy.pos, player.pos, "enemy")


  i = 0
  while i < len(pickupsPos):
    if player.pos == pickupsPos[i]:
      player.items.append(pickupsList[random.randint(0, len(pickupsList) - 1)])
      worldMap[pickupsPos[i][1]][pickupsPos[i][0]] = mapBase
      pickupsPos.pop(i)
      
      clear()
      print("You picked up a " + player.items[-1])
      player.items.sort()
      time.sleep(.75)
    i += 1
  
  enemy_index = 0
  while enemy_index < len(enemiesList):
    if enemiesList[enemy_index].pos == player.pos:
      doCombat(player, enemiesList[enemy_index])
      clear()
      if enemiesList[enemy_index].health <= 0:
        enemiesList.pop(enemy_index)
      elif player.health <= 0:
        player.die()
        print("GAME OVER: Press r to restart")
        while True:
          restart = getkey()
          if restart == "r":
            level = 1
            createNewMap()
            break
    enemy_index += 1
      
  clear()
  printMap(player.pos[0], player.pos[1])