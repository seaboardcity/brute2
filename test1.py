__metaclass__ = type #use Python 3 classes
from random import *
from autoFightClasses import *   #defines the Player class
from autoFightStats import *   #auto fight setup data
from autoFightTop import *
       
def dd1():
    'Debug setup. sets p[0] to have init and p[1]=dont have, then prints hands'
    p[0].init='have'
    print p[0].char, ' has init'
    p[1].init='dont have'
    p[0].printHand()
    p[1].printHand()
    return True
  
#def stat():
#    'debug. SHows status info'
#    for ii in [0,1]:
#        print '*****************'
#       # print 'caQueued', config.caQueued
#        print p[ii].char, 'status/init=',p[ii].status,'/', p[ii].init
#        p[ii].printHand()
        
#run a simple test    
setup_all_cards() #creates a dictionary of every potential card in the game
pc_list = ['warhawk','panzer','zcrafter']
iterations = 2
config.caQueued = [False] # This is filled with a value [cpi] when a pc has queued up a ca
p=[]
#assign specific chars to each player
p.append(Player('shadow', 1, allCards))
p.append(Player('panzer', 1, allCards))
#dd1()
#handleExchange(p[0], p[1])
battle_results = battle(p[0],p[1],p[0].init,p[1].init,1)
print '****************************'
print 'finished '
print 'showing stats:'
print 'results:',battle_results
print 'cards played::', p[0].char,' played', p[0].cards_played
print p[1].char,' played', p[1].cards_played
print ' '
stat(p[0],p[1])
