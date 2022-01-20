import random

# a list of unnecessary actions that make the results more interesting 
dramaticList = ["destroyed", "decimated", "obliterated", "walloped", "beat", "crippled", "evicerated", "fricked up", "hammered", "killed", "murdered", "demolished", "rocked"]

# a list of every throw in the game used by the AI
throwList = ["rock", "paper", "scissors", "sword", "shield", "gun", "the rock", "slime", "laser", "stick", "rainbow", "tornado", "arrow", "cannon", "charizard"]

beatDict = {
  "rock" : ["gun", "sword", "scissors", "tornado", "stick", "arrow", "cannon"],
  "paper" : ["shield", "rock", "the rock", "rainbow", "cannon", "arrow", "tornado"],
  "scissors" : ["paper", "the rock", "sword", "laser", "rainbow", "arrow", "slime"],
  "sword" : ["paper", "the rock", "gun", "laser", 'stick', 'charizard', 'rainbow'],
  "shield" : ["rock", "scissors", "sword", 'slime', 'laser', 'stick', 'arrow'],
  "gun" : ["shield", "scissors", "paper", 'stick', 'charizard', 'arrow', 'tornado'],
  "the rock" : ["rock", "gun", "shield", 'stick', 'charizard', 'slime', 'laser'],
  "slime" : ["rock", 'sword', 'gun', 'paper', 'charizard', 'arrow', 'cannon'],
  "laser" : ["slime", 'paper', 'gun', 'tornado', 'rock', 'rainbow', 'charizard'],
  "stick" : ["slime", 'scissors', 'paper', 'cannon', 'laser', 'rainbow', 'tornado'],
  "rainbow": ["slime", 'tornado', 'gun', 'shield', 'rock', 'cannon', 'the rock'],
  "tornado" : ["slime", 'cannon', 'shield', 'the rock', 'arrow', 'sword', 'scissors'],
  "arrow" : ['laser', 'stick', 'the rock', 'sword', 'charizard', 'rainbow', 'cannon'],
  "cannon" : ['shield', 'sword', 'scissors', 'the rock', 'charizard', 'gun', 'laser'],
  "charizard" : ['scissors', 'tornado', 'rock', 'paper', 'shield', 'stick', 'rainbow']
}

# Tommi's brain  -  the list contains several lists with the throw that they represent, and their weight in the randomly generated attack
tommiDict = {
  "rock" : 3,
  "paper" : 3,
  "scissors" : 3,
  "sword" : 3,
  "shield" : 3,
  "gun" : 3,
  "the rock" : 3,
  "slime" : 3,
  "laser" : 3,
  "stick" : 3,
  "rainbow" : 3,
  "tornado" : 3,
  "arrow" : 3,
  "cannon" : 3,
  "charizard" : 3,
}

evilTommiDict = {
  "rock" : 3,
  "paper" : 3,
  "scissors" : 3,
  "sword" : 3,
  "shield" : 3,
  "gun" : 3,
  "the rock" : 3,
  "slime" : 3,
  "laser" : 3,
  "stick" : 3,
  "rainbow" : 3,
  "tornado" : 3,
  "arrow" : 3,
  "cannon" : 3,
  "charizard" : 3,
}

startingHealth =  20
playerOneHealth = startingHealth
playerTwoHealth = startingHealth
throwOne = ""
throwTwo = ""
winner = ""
playBot = False
playTommi = False
trainEvilTommi = False
trainRandomTommi = False
tommiThrowIndex = 0

# clears the screen using code from the mystical land of stack overflow
def clear():
  print("\033[H\033[J", end="")

# Determines what Tommi will throw
def tommiAttack(goodOrEvil = "good"):
  total = 0
  throwNum = 0
  count = 0
  # adds up all of the numerical values in tommiList and gets a random number between one and the total
  if goodOrEvil.lower() == "good":
    for weight in tommiDict.values():
      total += weight
      throwNum = random.randrange(1, total + 1)

    for key in tommiDict:
      count += tommiDict[key]
      if count >= throwNum:
        return key

  elif goodOrEvil.lower() == "evil":
    for weight in evilTommiDict.values():
      total += weight
      throwNum = random.randrange(1, total + 1)

    for key in evilTommiDict:
      count += evilTommiDict[key]
      if count >= throwNum:
        return key

# the most basic form of AI learning - does what doesn't work less and does what does work more
def learn(goodOrEvil = "good"):
  if goodOrEvil.lower() == "good":
    if winner == "playerOne" and tommiDict[throwTwo] > 1:
      tommiDict[throwTwo] -= 1
    elif winner == "playerTwo":
      tommiDict[throwTwo] += 1

  elif goodOrEvil.lower() == "evil":
    if winner == "playerTwo" and evilTommiDict[throwOne] > 1:
      evilTommiDict[throwOne] -= 1
  
    elif winner == "playerOne":
      evilTommiDict[throwOne] += 1

def beatCheck(winList):
  for i in winList:
    if throwTwo == i:
      return "playerOne"
  for legalThrow in throwList:
    if throwTwo == legalThrow:
      return "playerTwo"
  return ""

def setUp():
  global nameOne
  global nameTwo
  global playBot
  global startingHealth
  global playerOneHealth
  global playerTwoHealth
  global playTommi
  global trainRandomTommi
  global trainEvilTommi

  playTommi = False
  playBot = False  
  trainRandomTommi = False
  trainEvilTommi = False
  startingHealth = 20

  if input("Play against AI? [Y/N] ").lower() == "y":
    if input("Play against Tommi? [Y/N] ").lower() == "y":
      nameTwo = "Tommi"
      if input("Train Tommi? [Y/N] ").lower() == "y":
        if input("Train against Evil Tommi? [Y/N] ").lower() == "y":
          trainEvilTommi = True
          nameOne = "Evil Tommi"
        else:
          trainRandomTommi = True
      else:
        playTommi = True
    else:
      playBot = True
      nameTwo = "Bot"
    
    if trainEvilTommi != True:
      nameOne = input("Enter player name: ").strip()
  
  else:
    nameOne = input("Enter player one name: ").strip()
    nameTwo = input("Enter player two name: ").strip()
  
  if input("Change HP? [Y/N] ").lower() == "y":
    startingHealth = int(input("Enter starting HP: "))
  playerOneHealth = startingHealth
  playerTwoHealth = startingHealth

setUp()

while True:
  while playerOneHealth > 0 and playerTwoHealth > 0:
    winner = ""

    if trainRandomTommi or trainEvilTommi:
      throwTwo = tommiAttack("Good")
    else:
      throwOne = input("Player One, throw! ").lower()
      clear()

    if playBot:
      throwTwo = throwList[random.randint(0, len(throwList) - 1 )]
    elif playTommi:
      throwTwo = tommiAttack("Good")
    elif trainRandomTommi:
      throwOne = throwList[random.randint(0, len(throwList) - 1 )]
    elif trainEvilTommi:
      throwOne = tommiAttack("Evil")
    else:
      throwTwo = input("Player Two, throw! ").lower()
      clear()

    if throwOne == throwTwo:
      print("Its a draw, both players threw " + throwOne)
      continue

    elif throwOne == "nuke" or throwTwo == "nuke":
      print("Everyone died, way to go")
      nameOne = "Nobody"
      nameTwo = "Nobody"
      break
    
    elif throwOne == "show brain":
      print("Tommi brain:\n" + str(tommiDict))
      print("Evil Tommi brain:\n" + str(evilTommiDict))
      continue

    else: 
      for legalThrow in throwList:
        if throwOne == legalThrow:
          if throwTwo in beatDict[throwOne]:
            winner = "playerOne"
          else:
            winner = "playerTwo"
        

    damage = random.randint(3, 8)
    if winner == "playerOne":
      print(nameOne + " " + dramaticList[random.randint(0, len(dramaticList) - 1)] + " " + nameTwo + "'s " + throwTwo + " with " + throwOne)
      playerTwoHealth -= damage
    elif winner == "playerTwo":
      print(nameTwo + " " + dramaticList[random.randint(0, len(dramaticList) - 1)] + " " + nameOne + "'s " + throwOne + " with " + throwTwo)
      playerOneHealth -= damage
    else:
      print("Do you even know how to play this game?")
    
    if playTommi or trainRandomTommi:
      learn("good")
    elif trainEvilTommi:
      learn("good")
      learn("evil")
    
    print(nameOne + " has " + str(playerOneHealth) + " health" + "\n"  + nameTwo + " has " + str(playerTwoHealth) + " health")
    print("______________________________________________________")

  if playerOneHealth > 0:
    print(nameOne + " Wins!")
  else: print(nameTwo + " Wins!")
  print("______________________________________________________")

  if input("Play again using the same settings? [Y/N] ").lower() == "y":
    playerOneHealth = startingHealth
    playerTwoHealth = startingHealth
    continue
  else: 
    setUp()
    continue
