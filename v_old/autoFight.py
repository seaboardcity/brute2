__metaclass__ = type #use Python 3 classes
from random import *
from autoFightClasses import *   #defines the Player class
from autoFightStats import *   #auto fight setup data



setup_all_cards() #creates a dictionary of every potential card in the game
p=[]
#assign specific chars to each player
p.append(Player('shadow',1, allCards))
p.append(Player('panzer',1, allCards))



#

