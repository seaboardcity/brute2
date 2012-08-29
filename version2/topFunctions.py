# top level functions
__metaclass__ = type #use Python 3 classes
from random import *
import tv


def setupDecks():
    'create the main deck and shuffle it'
    tv.mainDeck = tv.standardDeck[:]
    shuffle(tv.mainDeck)
    tv.discardDeck = []
    
    
    


