#This file contains the Player definition

__metaclass__ = type #use Python 3 classes
from random import shuffle
from random import choice
from copy import deepcopy
from handClass import *
import tv

## This class contains the dynamic information for a player 
#
# status, can have 'stunned' or 'wounded' appended

class pl:

    def __init__(self, name, abilities):
        'constructor. Names the char, sets status information'
        self.char = name
        self.status = ''


        
