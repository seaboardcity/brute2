# top level functions
__metaclass__ = type #use Python 3 classes
from random import *
import tv


def setupMainDeck():
    'create the main deck and shuffle it'
    tv.mainDeck = tv.standardDeck[:]
    shuffle(tv.mainDeck)
    


