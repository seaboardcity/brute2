#This file contains the function for handling decks

__metaclass__ = type #use Python 3 classes
from random import *
from random import shuffle
from autoFightStats import *   #auto fight setup data
import config



class deck:
    
    def __init__(self):
        'constructor. creates an empty hand'
        self.cards = []
        
    def addCard(self, card):
        'add a card to the deck'
        self.cards.append(card);
        
    def shuffleDeck(self):
        'shuffles the deck'
        shuffle(self.deck)
        
    
#

