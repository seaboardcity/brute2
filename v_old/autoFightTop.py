#This file contains all the top-level functions

__metaclass__ = type #use Python 3 classes
from random import *
from autoFightClasses import *   #defines the Player class
from autoFightStats import *   #auto fight setup data
import config

#global caQueued

#setup_all_cards() #creates a dictionary of every potential card in the game
#


#if '1on1' fight:
#    for pc0 in pc_list:
#        for pc1 in pc_list:
#            if pc0 != pc1:
#              for ii in range(iterations):
#                  p=[]
#                  p.append(Player(pc0,'1to1', allCards)) #player 0
#                  p.append(Player(pc1,'1to1', allCards))
#                  fight_result = fight(pc0, pc1, pc2, pc3, fight_odds))
#                  fight_report.append(pc0)
#                  fight_report.append(pc1)
#                  if fight_odds == '2to1':
#                      fight_report.append(pc2)
#                  elif fight_odds == '3to1':
#                      fight_report.append(pc2)
#                      fight_report.append(pc3)
#                  fight_report.append(fight_result)
#                  fight_report.append('::')
                  
def isRed(cpi):
    'looks at a cpi and determines if it is red. The cpi is for 1 card only'   
    if dbg<=1: print 'top:isRed: cpi', cpi[0], ' ', cpi[1]       
    if 'red' in allCards[cpi[0]]['attr'][cpi[1]]: return True
    else: return False
        
def isBlue(cpi):
    'looks at a cpi and determines if it is blue. The cpi is for 1 card only'   
    if dbg<=1: print 'top:isBlue: cpi', cpi[0], ' ', cpi[1]       
    if 'blue' in allCards[cpi[0]]['attr'][cpi[1]]: return True
    else: return False
        
def isGreen(cpi):
    'looks at a cpi and determines if it is green. The cpi is for 1 card only'   
    if dbg<=1: print 'top:isGreen: cpi', cpi[0], ' ', cpi[1]       
    if 'green' in allCards[cpi[0]]['attr'][cpi[1]]: return True
    else: return False
               
def amStunned(ch):
    'Checks to see if the character is stunned'
    if 'stunned' in ch.status: return True
    else: return False
        
def battle(pc0, pc1, pc0init, pc1init, odds):
    'Input the two character pointers, their initiative, and the odds. runs a \
    fight between two chars until one char loses or the minor char gains\
    initiative in a fight where the odds are greater than 1. The return values\
    are ["lost", <char name>], or ["tag"]. Returns [False] is something broke.'
    print 'caQueued=', config.caQueued
    minor = pc0
    major = pc1
    minor.init = pc0init
    major.init = pc1init    
    minor_init_prev = 'have'
    number_of_rounds = 0
    while True:
        number_of_rounds += 1
        print ' '
        print 'Inside battle, starting another round'
        if minor.init == 'faceoff':
            if major.init != 'faceoff':
                print 'ERROR: one char has faceoff and the other does not'
            outcome = handle_faceoff(minor, major)
        elif minor.init == 'have':
            if config.caQueued[0]:
                outcome = handleCA(minor, major)
            else:
                outcome = handleExchange(minor, major)
        else: #major has the init
            if config.caQueued[0]:
                outcome = handleCA(major, minor)
            else:
                outcome = handleExchange(major, minor)
                
        if not outcome[0]: #look for a loss
            if len(outcome)<2: 
                print 'fightRound: ERROR ERROR. Outcome =',outcome
                return outcome
            else:
                print '***************************************************'
                print 'ending battle between',minor.char,' and',major.char
                print 'number of rounds =',number_of_rounds
                return ['lost', outcome[1]]
        elif (odds > 1) and (minor.init!='dont have' and minor_init_prev=='dont have'):
            print '***************************************************'
            print 'tagging out between',minor.char,' and',major.char
            print 'number of rounds =',number_of_rounds
            return ['tag']
        minor_init_prev = minor.init
        if number_of_rounds > 300: 
            print 'ERROR: emergency stop due to 200 rounds'
            return ['lost', both]
        #stat(minor, major)
            
def stat(p0, p1):
    'debug. SHows status info'
    cc=[]
    cc.append(p0)
    cc.append(p1)
    for ii in [0,1]:
        print '****STATUS INFO*************'
       # print 'caQueued', config.caQueued
        print cc[ii].char, 'status=',cc[ii].status
        print 'init=',cc[ii].init
        cc[ii].printHand()  
#
# 
def applyOneCard(player, target, cpi):
    'Inputs are (player of the card, target of card, cpi). Apply the cpi to the\
     target. Return [False, charName] if the target cant meet the requirements.\
     Return [True] if it can.'
    result = target.applyYourCard2Me(cpi[:2])    
    if (not result[0]):
        return [False, target.char]
    else:
        if len(result) > 1: #a card was grabbed
            if dbg<=2: print 'applyOneCard: result =:',result
            player.add2hand(result[1])
        if dbg<=2: 
            print player.char, 'hand =', player.hand
            print target.char, 'hand =', target.hand
        return [True]
    
#
def applyBothCards(minor, major, minor_cpi, major_cpi):
    'apply both cards with each card applied to the other character. If a \
    character cant meet the requirments then return [False, charName], return \
    [False, both] if they both failed (this is a tie). Return [True] if it \
    worked.'
    minor_result = minor.applyYourCard2Me(major_cpi[:2])
    major_result = major.applyYourCard2Me(minor_cpi[:2])
    if (not minor_result[0]) and (not major_result[0]):
        return [False, 'both']
    elif (not minor_result[0]):
        return [False, minor.char]
    elif (not major_result[0]):
        return [False, major.char]
    else:
        if len(minor_result) > 1:
            if dbg<=2: 
                print 'applyBothCards: minor_result being: ',minor_result
            major.add2hand(minor_result[1])
        if len(major_result) > 1:
            if dbg<=2: 
                print 'applyBothCards: major_result being: ',major_result
            minor.add2hand(major_result[1])
        if dbg<=2: 
            print minor.char, 'hand =', minor.hand
            print major.char, 'hand =', major.hand
        minor.checkHandSz()
        major.checkHandSz()
        return [True]
 
    
def handle_faceoff(minor, major):
    'handle a faceoff between two chars, returns [True] if succesful or \
    [False, <char name>] if char has lost. Returning both names mean they \
    both lost at the same time, thus a tie has occurred and they both draw \
    again and go to faceoff.'
    global caQueued
    print '*************************'
    print 'Starting handle_faceoff'
    if dbg<=2:
        print minor.char,'hand=',minor.hand
        print major.char, 'hand =', major.hand
    minor_cpi = minor.pickCard(len(major.hand)-1, major.status, major.cards_played)
    major_cpi = major.pickCard(len(minor.hand)-1, minor.status, minor.cards_played)
    if not minor_cpi[0] and not major_cpi[0]:
        print 'Neither player has a card to play, both draw and try again'
        minor.drawCards(1)
        major.drawCards(1)        
        return [True]
    elif not minor_cpi[0]:
        print minor.char, ' has no card for a faceoff'
        return [False, minor.char]
    elif not major_cpi[0]:
        print major.char, ' has no card for a faceoff'
        return [False, major.char]
    else:
        print 'executing a faceoff'
        minor.playCard(minor_cpi[:2])
        major.playCard(major_cpi[:2])  
        both_results = applyBothCards(minor, major, minor_cpi, major_cpi)
        if not both_results[0]:
            return both_results
        if isRed(minor_cpi[:2]) and isRed(major_cpi[:2]):        
            if allCards[minor_cpi[0]]['faceoffVal'] > \
               allCards[major_cpi[0]]['faceoffVal']:         
                minor.init = 'have'; major.init = 'dont have'
            elif allCards[minor_cpi[0]]['faceoffVal'] < \
                 allCards[major_cpi[0]]['faceoffVal']:
                minor.init = 'dont have'; major.init = 'have'
            else: print 'a tie on faceoff'
        elif isBlue(minor_cpi[:2]) and isBlue(major_cpi[:2]):  
            minor.drawCards(1); major.drawCards(1)
        elif isBlue(minor_cpi[:2]): #minor is blue, major is red
            if (len(minor_cpi) > 2) and not amStunned(minor):
                config.caQueued = minor_cpi[2:]
                minor.init = 'have'; major.init = 'dont have'
            else:
                minor.init = 'dont have'; major.init = 'have'
        else: #minor is red, major is blue
            if (len(major_cpi) > 2) and not amStunned(major):
                config.caQueued = major_cpi[2:]
                minor.init = 'dont have'; major.init = 'have'
            else:
                minor.init = 'have'; major.init = 'dont have'
        print 'Faceoff done, new init values:', minor.char,'=',minor.init,' ::', \
               major.char,'=',major.init
        return [True]


    
# assigns the caP to equal the Player that is doing the counterattack
# defP equals the Player that is defending against the counterattack                    
# atkP equals the player with init
def handleCA(minor, major):
    'handles a counterattack between two chars, returns [True] if succesful or \
    [False, <char name>] if a char has lost. Returning both names mean they \
    both lost at the same time, thus a tie has occurred and they both draw \
    again and go to faceoff.' 
    #global caQueued                   
    print '*************************'
    print 'Starting handleCA'
    #print minor.char,'hand=',minor.hand
    #print major.char, 'hand =', major.hand
        
    if (minor.init == 'have') & (major.init == 'dont have'):
        caP = minor
        defP = major
    elif (minor.init == 'dont have') & (major.init == 'have'):
        caP = major
        defP = minor
    else:
        print 'handleCA: ERROR ERROR, initiative messed up'
        return [False]         
    
    caP_cpi = config.caQueued
    result = handleRedBlueEx(caP, defP, caP_cpi)
      
    print 'handleCA done'
    print 'new init values:', caP.char,'=',caP.init,' ::', defP.char,'=',defP.init
    return result    


# assigns the atkP to equal the Player that has the init.
# defP equals the Player that is defending.
# Note that the attacker can play a green card  
# Note that attacker cannot fail to play a card as v1 is always available            
def handleExchange(minor, major):
    'handles a normal excange between two chars, returns [True] if succesful or \
    [False, <char name>] if a char has lost. Returning both names mean they \
    both lost at the same time, thus a tie has occurred and they both draw \
    again and go to faceoff. Return [False] by itself means the program broke.' 
    #global caQueued                   
    print '*************************'
    print 'Starting handleExchange'
#    print minor.char,'hand=',minor.hand
#    print major.char, 'hand =', major.hand
        
    if (minor.init == 'have') & (major.init == 'dont have'):
        atkP = minor
        defP = major
    elif (minor.init == 'dont have') & (major.init == 'have'):
        atkP = major
        defP = minor
    else:
        print 'handleCA: ERROR ERROR, initiative messed up'
        return [False]         
    
    atkP_cpi = atkP.pickCard(len(defP.hand)-1, defP.status, defP.cards_played)
    if not atkP_cpi[0]: 
        print atkP.char,' has not card to pick'
        return [False, atkP.char]
    if isGreen(atkP_cpi):
        atkP.playCard(atkP_cpi)
        def_results = applyOneCard(atkP, defP, atkP_cpi)
        if not def_results[0]:
            print defP.char, ' cannot continue'
            return [False, defP.char]   
        results = detExchangeInit(atkP, atkP_cpi, defP, [])
        return results
    else:
         results = handleRedBlueEx(atkP, defP, atkP_cpi)
      
    print 'handleExchange done'
    print 'new init values:',atkP.char,'=',atkP.init,'::',defP.char,'=',defP.init
    return results    
    
# 
def handleRedBlueEx(redP, blueP, redP_cpi):
    'redP & blueP are pointers to the red & blue players. The redP_cpi is the\
    card to be played by the redP. This card is always red. Both cards are \
    played and the results applied. Return [True] if everything went okay. \
    Return [False, str(char name)] if a character has to quit.'
    #global caQueued 
    if dbg5<=3: print 'handleRedBlueEx, inputs = ', redP.char, blueP.char, \
        redP_cpi
    redP.playCard(redP_cpi[:2])
    blue_results = applyOneCard(redP, blueP, redP_cpi)
    if not blue_results[0]:
         print blueP.char, ' cannot continue'
         return [False, blueP.char]   
    blueP_cpi = blueP.pickCard(len(redP.hand)-1, redP.status, redP.cards_played)
    if not blueP_cpi[0]:
            print blueP.char, ' has no card to defend with'
            return [False, blueP.char]
    blueP.playCard(blueP_cpi[:2])  
    red_results = applyOneCard(redP, blueP, redP_cpi)
    if not red_results[0]:
         print redP.char, ' cannot continue'
         return [False, redP.char]   
    if isRed(redP_cpi[:2]) and isBlue(blueP_cpi[:2]):
        results = detExchangeInit(redP, redP_cpi[:2], blueP, blueP_cpi)
        if dbg<=2:
            print 'handleRedBlueEx: red/blue cpi=',redP_cpi,'/',blueP_cpi
            print 'new init for red/blue=', redP.init, '/', blueP.init
        return results
    else:
       print 'handleRedBlueEx: ERROR ERROR, card selection messed up. cards are', \
       blueP_cpi, redP_cpi
       return [False]   
       
#    
def detExchangeInit(atkP, atkP_cpi, defP, defP_cpi):
    'pass in the attacker/cpi and defender/cpi as part of an exchange and\
    determine the resulting init. Returns [False] if there was a problem, [True] \
    if okay'     
    #global caQueued            
    if (len(defP_cpi) > 2):
        if amStunned(defP):
            print 'detExchangeInit: ERROR ERROR:',defP.char,'attempting CA while\
            stunned. cpi=',defP_cpi,':: caQueued=',config.caQueued
            return [False]
        else:
            config.caQueued = defP_cpi[2:]
            defP.init = 'have'; atkP.init = 'dont have' 
            results = [True]
    else:
        config.caQueued = [False]
        if isGreen(atkP_cpi):
            newAtkInit = atkP.detNewInitiative(atkP_cpi)            
            if newAtkInit == 'have':
                atkP.init = 'have'
                defP.init = 'dont have'
            elif newAtkInit == 'dont have':
                atkP.init = 'dont have'
                defP.init = 'have'
            else: 
                atkP.init = 'faceoff'
                defP.init = 'faceoff'
            results = [True]
        else: #the attacker is Red
            defP.init = defP.detNewInitiative(defP_cpi)   
            if defP.init == 'have': atkP.init = 'dont have'
            elif defP.init == 'faceoff': atkP.init = 'faceoff'
            elif defP.init == 'dont have': atkP.init = 'have'
            else: 
                print 'detExchangeInit: ERROR ERROR. atkP.init=',atkP.init,\
                ' defP.init=',defP.init
                return [False]
            results = [True]
    if dbg<=2: print 'detExchangeInit: new atk/def init =', atkP.init, defP.init
    return results
 
    
        
    


#

