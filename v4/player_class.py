#This file contains the Player definition

__metaclass__ = type #use Python 3 classes
from random import shuffle
from random import choice
from copy import deepcopy
from handClass import *
import tv

## This class contains the dynamic information for a player 
#
# status, can have 'stunned' or 'wounded' appended as needed
# init can have 'faceoff', 'have', 'dont have', ['faceoff red']
# cp is a list with the cp's player has. This includes the virtual cp's
# Cards is the card list the player has. 

# temporarily create lists with [ [<card number>, <short term value>],
#                                 [<card number>, <short term value>, etc

class player:

    def __init__(self, name, abilities):
        'constructor. Names the char, sets status information'
        self.char = name
        self.status = ''
        self.init = 'faceoff'
        self.cp = ''
        self.cards = ''
        self.abilities = ''

        
