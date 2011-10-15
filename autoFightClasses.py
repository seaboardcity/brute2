#This file contains the Player definition

__metaclass__ = type #use Python 3 classes
from random import shuffle
from random import choice
from autoFightStats import *
from copy import deepcopy
import config

#oppoStatus is a dictionary with the follow key:value pairs:
#     
#for every possible card.panel play:
#    calculate the new value of my hand
#    calculate my new state value
#    myNewHandVal + myNewPosVal = myNewStateVal
#    calculate new value of your hand in response to the card.panel
#    calculate your new state value
#    yourNewHandVal + yourNewPosVal = yourNewStateVal
#    myNewRelVal = myNewStateVal - yourNewStateVal

#as you calculate myNewRevVal record the card.panel combos if 
#it's higher than the old one. The highest one is the card.panel
#to play

## This class contains the dynamic information for a player 
# dhand is a dictionary with cardID as the key and the value is a list
# with each element a list of the panel attributes for that indexed panel    
#

class Player:

    def __init__(self, name, setupOdds, allCards):
        'constructor. Names the char, creates & shuffles deck, deals hand'
        self.best_cpi = []
        self.best_cpi_val = -100
        self.lastPlayWasGreen = False
        self.init = 'faceoff' # faceoff|faceoff red|have|dont have
        self.status = set([])
        self.char = name
        self.hand = []      
        self.setupDeck(charDeck[name])
        self.initialDraw()
        self.odds = setupOdds # 1 for '1to1', 2 for '2to1', 3 for '3to1', etc
        #list of cards stolen during play, when discarded then just dissapear, \
        #they don't go into the discard pile
        self.discard = []
        self.stolenCardList = [] 
        self.cards_played = 0
       
   
    def setupDeck(self,deckList):
        'creates a deck from card list and shuffles it'
        self.deck = deckList[:]
        shuffle(self.deck)     
        
    #Note that this function essentially recreates the deck. This is done
    #because that way we can 'recapture' cards taken by an opponent
    def pickupDiscards(self):
        'sets the deck equal to the original deck size, shuffles the deck, then \
        removes all the cards currently in your hand'
        self.setupDeck(charDeck[self.char])
        print self.char,'pickupDiscards: deck = ', self.deck
        for card in self.hand:
            if card in self.deck:
                self.deck.remove(card)
                
    def add2hand(self,card):
        'Inserts a card into hand. Note, discarding if handsize is too big is \
        done seperately. THIS IS ON PURPOSE'
        self.hand.append(card)
                
    def drawCards(self, N):
        'draw N cards from deck into hand, updates hand. '
        if N > len(self.deck):
            self.pickupDiscards()
        for ii in range(N):
            card = self.deck.pop()
            self.add2hand(card)
            print self.char, 'drew card', card
            
    def checkHandSz(self):
        'Determines if you have too many cards in your hands and if so discards \
        until you have the correct number'
        while len(self.hand) > (self.maxHandSz()+1):
            card = self.pickCard2Discard()
            self.discardCard(card)
            print self.char, 'discard ', card, 'due to excessive hand size'
            
    def initialDraw(self):
        'do the initial draw of the hand'
        self.drawCards(MAX_HAND)
        self.add2hand('v1')
            
    def discardCard(self, card):
        'discard a particular card. the v1 card cannot be discarded'
        if card == 'v1':
            print 'ERROR: ', self.char, 'attempting to discard v1 card'
        else:
            self.hand.remove(card)
            print self.char, 'discarded ',card
            if dbg<=2: print self.char, 'new hand=',self.hand
            
    # looks for all the attributes in attrList to exist in one 
    # panel on a card and returns those card/panel pairs as a 
    # list
    def findAttrInCardPanels(self, attrList, localHand):
        hitPairs=[]
        for card in localHand:
            hits=[0, 0, 0, 0] #how many attr hits on each panel
            for attr in attrList:
                for panelIdx in range(len(allCards[card]['attr'])):
                    if dbg<=0:
                        print self.char, 'findAttrInCardPanesl: looking for', attr, ' in card ', card, 'panel ', panelIdx#debug
                    if allCards[card]['attr'][panelIdx].count(attr) > 0: 
                        hits[panelIdx] += 1
            for panelIdx in range(len(allCards[card]['attr'])):
                if hits[panelIdx] >= len(attrList): 
                    hitPairs.append(card)
                    hitPairs.append(panelIdx)
        return hitPairs    
    
    def findUnqCards(self, attrList, localHand):
        'finds the cards that have attrList. Each card reported once only'
        cardList = []
        cardPanelList = self.findAttrInCardPanels(attrList, localHand)    
        for ii in range(0, len(cardPanelList)/2): 
            cardList.append(cardPanelList[2*ii])
        for element in cardList: 
            if cardList.count(element) > 1: 
                for jj in range(cardList.count(element)-1): 
                    cardList.remove(element)
        return cardList

    #the input lists can have the same elements as each other, but 
    #the final number of pairs assume each element in the pair is unique
    #and             
    def findNumCardPairs(self, attrList0, attrList1, localHand):
        'find pairs of cards that have attrList0 on one card and attrList1 on the other. \
        Return the number of pairs'
        cardList0 = self.findUnqCards(attrList0, localHand)        
        cardList1 = self.findUnqCards(attrList1, localHand)
#        print 'findNumCardPairs: list0', cardList0, ':: list1 ', cardList1
        if len(cardList0) == 0 or len(cardList1) == 0: return 0
        else:
            S0 = set(cardList0)
            S1 = set(cardList1)
            iSet= S0 & S1
            S0diffS1 = S0 - S1
            S1diffS0 = S1 - S0
            numPairs = int(len(iSet)/2)
            if (len(iSet)%2) == 0:         
                numPairs += min(len(S1diffS0), len(S0diffS1))
            else:
                if len(S0diffS1) > len(S1diffS0): 
                    numPairs += len(S1diffS0) + 1
                elif len(S1diffS0) > len(S0diffS1): 
                    numPairs += len(S0diffS1) + 1
                else: numPairs += len(S0diffS1)
            return numPairs
            
    def findCardPairs(self, attrList0, attrList1, localHand):
        'find pairs of cards that have attrList0 on one card and attrList1 on the other. \
        Return the cards.'
        cardPairs = []
        cardList0 = self.findUnqCards(attrList0, localHand)        
        cardList1 = self.findUnqCards(attrList1, localHand)
        listing0 = cardList0[:]
        listing1 = cardList1[:]
        if dbg<=0: print self.char,'findCardPairs: list0', cardList0, ':: list1 ', cardList1
        if len(cardList0) == 0 or len(cardList1) == 0: 
                return []        
        else:
            #remove cards that are on both lists
            for c0 in listing0:
                for c1 in listing1:
                    if c0 == c1:
                        if len(cardList0) > len(cardList1):
                            cardList0.remove(c0)
                        else:
                            cardList1.remove(c1)
            if dbg<=0: print self.char,'pruned cardList0,',cardList0,':: cardList1',cardList1
            listing0 = cardList0[:]
            for c0 in listing0:
                crntVal = 100
                crntPair = []
                for c1 in cardList1:
                    crntPrice = allCards[c0]['price']+allCards[c0]['price']
                    if dbg<2: print self.char,'findCardPairs:',self.char,': for c0/c1 = ',c0,'/',c1,' price =',crntPrice
                    if crntPrice < crntVal:
                        crntPair.append(c0)
                        crntPair.append(c1)
                        crntVal = crntPrice
                if crntVal < 100:
                    cardPairs.extend(crntPair)
                    cardList0.remove(crntPair[0])
                    cardList1.remove(crntPair[1])
            return cardPairs
                
    #
    def reversers_found(self, prosp_hand):
        'returns True if there is at least one reverser (a counter attack pair, a \
        card that gains initiative, or a faceoff card in the prosp_hand'
        if self.findNumCardPairs(['caBlue'], ['counter attack'], prosp_hand) > 0:
            if dbg<=1: print self.char,'reversers_found: found ca pairs'
            return True
        elif self.findUnqCards(['blue', 'gain initiative'], prosp_hand):
            if dbg<=1: print self.char,'reversers_found: found gain initiative'
            return True
        elif self.findUnqCards(['blue', 'start faceoff'], prosp_hand):
            if dbg<=1: print self.char,'reversers_found: found start faceoff'
            return True
        else:
            if dbg<=1: print self.char,'reversers_found: found nothing'
            return False
     
    # Determine the reverser(s) value by first looking at the blue 'gain init' 
    # cards, then the counter-attack pairs, then the 'start faceoff'/attack pairs.
    # As each card(s) are found their removed from the list so they are only
    # used once each
    # The value is altered depending on whether you have/dont have inint (x1/x2)
    # and whether your stunned/unstunned (x1/x2) for ca pairs & faceoff pairs
    # faceoff pairs are only worth half as much as ca pairs
    #
    # l_stat = list of propsective status
    def detRevVal(self,prosp_hand, l_stat):
        'Returns a value for the number of reversers in the prosp_hand.'
        lhand=prosp_hand[:]
        numOfRev = 0
        cardList = self.findUnqCards(['blue', 'gain initiative'], lhand)       
        numOfRev += len(cardList)
        for card in cardList:
            lhand.remove(card)
        cardList = self.findCardPairs(['blue','caBlue'], ['counter attack'], lhand)
        if 'stunned' in l_stat:
            numOfRev += len(cardList)/3.0
        else:
            numOfRev += len(cardList)/2.0
        for card in cardList:
            lhand.remove(card)
        if 'stunned' in l_stat:
            numOfRev += self.findNumCardPairs(['start faceoff'], ['red'], lhand)/6.0
        else:
            numOfRev += self.findNumCardPairs(['start faceoff'], ['red'], lhand)/4.0
        if dbg3 <= 2: print self.char,'detRevVal:',self.char,'return=',numOfRev * INITIATIVE_VAL
        return numOfRev * INITIATIVE_VAL                     
        
    def numOfReversers(self, prosp_hand):
        'returns the number of reversers in the prosp_hand.'
        numOfRev = 0
        numOfRev += self.findNumCardPairs(['caBlue'], ['counter attack'], prosp_hand)
        numOfRev += len(self.findUnqCards(['blue', 'gain initiative'], prosp_hand))
        numOfRev += len(self.findUnqCards(['blue', 'start faceoff'], prosp_hand))
        return numOfRev

        
    def faceoffStr(self, prosp_hand):
        'pass in a prosp_hand list and this will return the faceoff strength\
        as an integer'
                
        
    # l_stat a list of status values
    def prospHandVal(self, newInitiative, prosp_hand, l_stat):
        'looks at a propective hand and tells you the hand value. Not including stun/unstun pairs'
        p_hand_val = 0
        for card in prosp_hand: 
            p_hand_val += allCards[card]['price']
        #add in value of the against*Odds cards
        if self.odds > 1:
            p_hand_val += len(self.findUnqCards(['againstTheOdds'], prosp_hand)) * ALL_ODDS_VAL
        if self.odds > 2:
            p_hand_val += len(self.findUnqCards(['againstAllOdds'], prosp_hand)) * ALL_ODDS_VAL
        #add in the value of reversers
        p_hand_val += self.detRevVal(prosp_hand, l_stat)  
        #add value for having a red
        if self.findUnqCards(['red'], prosp_hand):
            p_hand_val += myPosWt['have a red']
            if newInitiative == 'have': 
                p_hand_val += myPosWt['have a red while on atk']
        #add value for having a blue                
        if self.findUnqCards(['blue'], prosp_hand):
            p_hand_val += myPosWt['have a blue']
            if newInitiative == 'dont have': 
                p_hand_val += myPosWt['have a blue while on def']
        #add value for stun/unstun pairs
        blueStunUnstunPairs = self.findNumCardPairs(['blue','stun'], ['blue','unstun'], prosp_hand)
        if 'stunned' in l_stat:
            p_hand_val += myPosWt['blueStunUnstunPair while stunned']*blueStunUnstunPairs
        else:
            p_hand_val += myPosWt['blueStunUnstunPair']*blueStunUnstunPairs
        #add value for faceoff strength if we're starting a faceoff
        if (my_init == 'faceoff') and not('stunned' in self.status):
            p_hand_val += self.faceoffStr(prosp_hand)
        if dbg3<=2: print self.char,'propsHandVal: p_hand_val=',p_hand_val
        return p_hand_val
        
    # newInitiative = have, dont have, faceoff
    # calculating the hand value is done by:
    # temporarily removing the cpi from the hand
    # summing the price of the cards in the hand
    # determine the new status of the player after applying the card
    # adding in bonuses for: ca pairs; stun/unstun pairs; having a red while 
    #   on attack; having a blue while on defense; having againstTheOdds
    #   againstAllOdds cards in the correct ways
    def myHandValue(self, newInitiative, cpi, play):
        'returns my hand value after making a copy and subracting the \
        playedCard(s). If play=True then the status value effect of the cpi \
        is used for determining the hand value, otherwise not'
        prosp_hand = self.hand[:]     
        if dbg3<=1: 
            print ' '
            print self.char,'myHandValue: cpi = ',cpi
        if len(cpi) > 2:   
            prosp_hand.remove(cpi[0])
            prosp_hand.remove(cpi[2])
        elif len(cpi) > 1:
            prosp_hand.remove(cpi[0])
        if dbg3<=1: print self.char,'in myHandValue prosp_hand =', prosp_hand
        #find msv (My Status Value) if the card is to be played
        if play: msv = self.myStatusValue(newInitiative, cpi, prosp_hand)
        else:
            msv = list(self.status)
            msv.append(0)
        handVal = msv.pop() #pop off the status numerical value, leave status list behind
        handVal += self.prospHandVal(newInitiative, prosp_hand, msv) #add in prospective hand value
        if dbg3<=1: print self.char,'myHandValue: final handVal =', handVal
        return handVal
        
    # cpi_attr is the attributes of the played cpi
    def myStatusValue(self, my_init, cpi, prosp_hand):
        'determine my status value after playing cpi. This includes altering \
        my own status ONLY, not assumed alterations to your status, returns a \
        list in the form:[<stat1>, <stat2>,...<status value>]. Return 0 if cpi \
        is empty.'
        if dbg3<=2: print self.char,'myStatusValue: my_init = ', my_init, ' cpi = ', cpi
        if len(cpi) < 1: return 0
        prospective_hand_sz = len(prosp_hand)-1
        cpi_attr = allCards[cpi[0]]['attr'][cpi[1]]
        if len(cpi) > 2:   
            cpi_attr = cpi_attr + allCards[cpi[2]]['attr'][cpi[3]]
        if dbg3<=2: print self.char,'myStatusValue: cpi_attr =', cpi_attr
        my_status_s = self.status.copy()
        stat_val = 0
        if my_init == 'have': 
            if ('stun' in cpi_attr) or ('stunned' in self.status):
                stat_val += 0.5 * INITIATIVE_VAL
            else:
                stat_val += INITIATIVE_VAL
        elif (my_init == 'faceoff red') and ('red' in cpi_attr) and \
                not('stunned' in cpi_attr):
            stat_val += INITIATIVE_VAL * allCards[cpi[0]]['faceoffVal']/(MAX_FACEOFF+1.0)
            if dbg3<=2: 
                print self.char,'myStatusVale: faceoff red, faceoff value =', \
                INITIATIVE_VAL * allCards[cpi[0]]['faceoffVal']/(MAX_FACEOFF+1.0)
        for attr in cpi_attr:
            if attr == 'stunned':
                my_status_s.add('stunned')
            elif attr == 'wounded':
                my_status_s.add('wounded')
            elif attr == 'unstun':
                if 'stunned' in my_status_s:
                    my_status_s.remove('stunned')
            elif attr == 'unwound':
                if 'wounded' in my_status_s:
                    my_status_s.remove('wounded')
            elif attr == 'draw':
                prospective_hand_sz += 1
                if prospective_hand_sz <= (self.maxHandSz()+1):
                    if self.reversers_found(prosp_hand):
                        stat_val += MEAN_CARD_VAL
                    else:
                        stat_val += MEAN_CARD_VAL*1.1 #it's more useful to draw if you have no reversers         
                else: stat_val += MEAN_CARD_VAL * 0.2 #it's still useful to draw even if will force a discard
        if dbg3<=2: 
            print self.char,'myStatusValue: (1) stat_val=',stat_val
            print self.char,'myStatusValue: my_status_s = ', my_status_s
        for stat in my_status_s:
            if dbg3<=2: print self.char,'myStatusValue: stat in my_status_s = ', stat, \
                  ' my_stat_val[stat] = ', my_stat_val[stat]
            stat_val += my_stat_val[stat]
        msv_return = list(my_status_s)
        msv_return.append(stat_val)
        if dbg3<=2: print self.char,'myStatusValue: msv_return = ', msv_return
        return msv_return        
        
    def detNewInitiative(self, cpi):
        'return initiative based on current intiative and the cpi \
         returns faceoff|faceoff red|have|dont have'
        if len(cpi) < 1:
            newInitiative = self.init
        elif len(cpi) > 2:            
            card=cpi[2]
            pnl=cpi[3]
        else:
            card=cpi[0]
            pnl=cpi[1]
        newInitiative = self.init
        attr = allCards[card]['attr'][pnl]
        if self.init == 'have':
            if 'lose initiative' in attr:
                newInitiative = 'dont have'
        elif self.init == 'dont have':
            if 'gain initiative' in attr:
                newInitiative = 'have'
            if 'start faceoff' in attr:
                newInitiative = 'faceoff'
        else: #doing a faceoff
            if 'red' in attr:
                if 'counter attack' in attr:
                    newInitiative = 'have'
                else:
                    newInitiative = 'faceoff red'
            else:
                newInitiative = 'dont have'
        return newInitiative

    #determines opponents state value
    # newInitiative is what their initiative state will be
    # yourHandSz is how many cards they start with
    # yourStatus is how they start with regards to stun/wound/etc
    # panel is the panel played against them
    #
    #Retern a numerical value of their state value
    def yourStateValue(self, my_init, your_hand_size, your_status, cpi):
        'determine the state value for your opponent'
        cpi_attr = allCards[cpi[0]]['attr'][cpi[1]]
        if len(cpi) > 2:            
            cpi_attr = cpi_attr + allCards[cpi[2]]['attr'][cpi[3]]
#        print 'cpi_attr = ', cpi_attr
        your_status_s = your_status.copy()
        hand_val = yourHandValue[your_hand_size]
        if my_init == 'dont have': 
            hand_val += INITIATIVE_VAL
        elif my_init == 'have':
            if 'red' in cpi_attr:
                hand_val += your_stat_val['must play blue']
                hand_val += your_stat_val['can reverse']
        for attr in cpi_attr:
            if attr == 'stun':
                your_status_s.add('stunned')
            elif attr == 'wound':
                your_status_s.add('wounded')
            elif attr == 'you discard':
                your_status_s.add('you discard')
            elif attr == 'you discard random':
                your_status_s.add('you discard random')
            elif attr == 'you lose card':
                your_status_s.add('you lose card')
            elif attr == 'you lose random card':
                your_status_s.add('you lose random card')
        if dbg<=1: print self.char,'yourStateValue: your status = ', your_status_s
        for stat in your_status_s:
            hand_val += your_stat_val[stat]
        if dbg<=1: print self.char,'yourStateValue: have val = ', hand_val
        return hand_val

    def get_ca(self, cpi):
        'takes in a cpi and looks for a legal counterattack to attach. \
        Returns the cpi with the counterattack in the form \
        [card1,panel1,card2,panel2]'
        ca_list = self.findUnqCards(['counter attack'], self.hand)
#        print 'ca_list', ca_list
        sel_card_val = 1000
        sel_card = None
        for card in ca_list:
#            print 'trying card ', card, 'with cpi0', cpi[0]
            if card != cpi[0]:
                if sel_card_val > allCards[card]['price']:
                    sel_card = card
                    sel_card_val =  allCards[card]['price']
        if sel_card:
            for pnl in range(len(allCards[sel_card]['attr'])):
                if 'counter attack' in allCards[sel_card]['attr'][pnl]:
                    cpi.append(sel_card)
                    cpi.append(pnl)
        return cpi

    # this trys a card             
    def try_card(self, cpi, your_hand_size, your_status):
        'trys a card/index and returns the relative value. \
        Returns False if it cant work'
        newInit = self.detNewInitiative(cpi)
        thisRelPlayVal = self.myHandValue(newInit, cpi, True) - \
            self.yourStateValue(newInit, your_hand_size, your_status, cpi)
        if dbg<=0: print self.char,':try_card: thisRelPlayVal = ', thisRelPlayVal, ' for cpi = ', cpi
        if thisRelPlayVal > self.best_cpi_val:            
            self.best_cpi_val = thisRelPlayVal
            self.best_cpi = cpi

    def try_ca(self, cpi, your_hand_size, your_status):
        'trys the original provide cpi with all possible counterattacks that \
        can be attached. Note that this function assumes the incoming cpi can \
        be played with a counter attack'
        ca_list = self.findUnqCards(['counter attack'], self.hand)
        for ca_card in ca_list:
            if ca_card != cpi[0]:
                ca_cpi=cpi[:]
                ca_cpi.append(ca_card)
                ca_cpi.append(1)
                self.try_card(ca_cpi,your_hand_size,your_status)
                        
    #checks to see if the cpi can be legally played                        
    #cannot play stunned if already stunned
    #cannot play wounded if already wounded
    #cannot play if it will force you below 0 cards
    def legal_play(self, cpi, init):
        'Inputs are cpi and init. Checks that the cpi is a legal play. Returns \
        False if not legal, otherwise return True'
        if dbg<=1: print self.char,'legal_play: is cpi', cpi,' legal with init',init
        restr_l = allCards[cpi[0]]['restr'][cpi[1]]
        if len(cpi) > 2:
            restr_l = restr_l + allCards[cpi[2]]['restr'][cpi[3]]
        attr_l = allCards[cpi[0]]['attr'][cpi[1]]
        if len(cpi) > 2:            
            attr_l = attr_l + allCards[cpi[2]]['attr'][cpi[3]]
        if dbg<=1: print self.char,'legal_play: restr_l =', restr_l
        if dbg<=1: print self.char,'legal_play: attr_l =', attr_l
     #   if (cpi[0]=='v1'):
      #      return False
        if (len(self.hand) < 2) and \
                  (('discard' in attr_l) or ('discard random')) and \
                  not ('draw' in attr_l):
            return False
        if init == 'have':
            if 'blue' in restr_l:
                return False
            if ('green' in restr_l) and self.lastPlayWasGreen:
                    return False
            if ('red' in restr_l) and ('stunned' in self.status):
                    return False
        elif init == 'dont have':
            if ('green' in restr_l) or ('red' in restr_l):
                return False
            if ('red' in restr_l) and ('stunned' in self.status):
                return False
            if ('not stunned' in restr_l) and ('stunned' in self.status):
                return False
            if ('not wounded' in restr_l) and ('wounded' in self.status):
                return False
        elif init == 'faceoff' or init == 'faceoff red':
            if ('red' in restr_l) and ('stunned' in self.status):
                return False  
            if ('not stunned' in restr_l) and ('stunned' in self.status):
                return False                
            if 'green' in restr_l:
                return False
            if 'not in faceoff' in restr_l:
                return False
        if '2to1' in restr_l:
            if self.odds < 2:
                return False
        if '3to1' in restr_l:
            if self.odds < 3:
                return False
        if 'after caBlue' in restr_l:
            if 'caBlue' not in attr_l:
                return False
        if dbg<=1: print self.char,':legal_play: cpi ', cpi, ' init', init, 'is legal'
        return True


    #prints out your hand nicely formatted
    def printHand(self):
        'input nothing, returns nothing'
        print '    ', self.char, 'hand is: '
        for card in self.hand:
            if card != 'v1':
                if len(dCards[card]['panels']) > 1:
                    print card,':',dCards[card]['panels'][0], ',', dCards[card]['panels'][1],dCards[card]['faceoffVal']
                else:
                    print card,':',dCards[card]['panels'][0],dCards[card]['faceoffVal']

    #print out the cpi nicely formatted         
    def print_cpi(self,cpi):
        'input a cpi, returns nothing'
        if len(cpi)<3:
            print 'Play ', cpi[0], '/', dCards[cpi[0]]['panels'][cpi[1]]
        else:
            print 'Play ', cpi[0], '/', dCards[cpi[0]]['panels'][cpi[1]], \
            ': followup is ', cpi[2], '/', dCards[cpi[2]]['panels'][cpi[3]]

    
    # Trys to see if there should be an alternate card pick using a different
    # set of rules. 
    # if you have the init and cannot pick a card, try v1
    # 
    # has few cards left, then play v1/passInitiative3 instead of a normal v1
    #    if (l_cpi[0] == 'v1') and (l_cpi[1] == 0):
    #            num_reds_or_greens = self.findUnqCards(['red'], self.hand)
    #            num_reds_or_greens.append(self.findUnqCards(['green'], self.hand))
    #                (len(self.hand)>4) and (num_reds_or_greens == 0):
    #                if (your_cards_played > 10) and (your_hand_size <6):
    #                    l_cpi = ['v1',2]
    #                if (your_cards_played > 20):
    #                    l_cpi = ['v1',2]
    #                if ('stunned' in your_status):
    #                    l_cpi = ['v1',2]
    def altPickCard(self, std_cpi, your_hand_size, your_status, your_cards_played):
        l_cpi = std_cpi[:]
        if self.init == 'have':
            if 'stunned' in self.status:
                l_cpi = ['v1',1]
            elif (len(self.hand) < 5):
                l_cpi = ['v1',0]
            else:
                l_cpi = ['v1',2]            
        print self.char,':altPickCard, cpi=',std_cpi,':your_hand_size=',\
        your_hand_size,': status=',your_status,': your_cards_played=',\
        your_cards_played
        print 'l_cpi=',l_cpi
        return l_cpi
        

    def detFaceoffStr(self, prosp_hand):
        'input a prospective hand and return how strong the hand is during a faceoff.\
        2.0 is max strength. 0.0 is minimum.'
        recorded_strength = 0
        card_list = self.findUnqCards(['red'], prosp_hand)
        for card in card_list:
            if allCards[card]['faceoffVal'] > 0:
                faceoff_str = 1 + allCards[card]['faceoffVal']/MAX_FACEOFF
                if faceoff_str > recorded_strength:
                    recorded_strength = faceoff_str
         return recorded_strength
        
                               
    
    #returns a number indicating how much playing the cpi will improve 
    #the players position. Note, thats ALL it calculates, it does no worry 
    #about the status of your hand.
    #
    # For the cpi see what effects/changes it will produce, will it stun
    # someone? will it force a discard? If it forces a discard is that an
    # instant win? etc. Then lookup the value of that maneuver from the table.
    def calcCpiPosVal(self, cpi, your_hand_size, your_status, init):
        'Input a cpi and opponents status. Returns an integer indicating how \
        much my relative status will improve by playing the card. Higher is \
        better.'
        cpi_val=0 #initial value for the cpi
        #total cards the defender has to use up. This includes blue defense, discards, etc
        total_cards_defender_loses=0
        #setup the prospective hand with the cpi card removed
        prosp_hand = self.hand[:]
        if len(cpi) > 2:
            attr_list = allCards[cpi[0]]['attr'][cpi[1]] + \
                        allCards[cpi[2]]['attr'][cpi[3]]
            prosp_hand.remove(cpi[0])
            prosp_hand.remove(cpi[2])            
        elif len(cpi) > 1:
            attr_list = allCards[cpi[0]]['attr'][cpi[1]]
            prosp_hand.remove(cpi[0])        

        #use special faceoff calculation
        if init == 'faceoff':
            return 1+allCards[cpi[0]]['faceoffVal']/MAX_FACEOFF

        #calculate value for 'have' and 'dont have' init
        for attr in attr_list:
            if attr == 'stun':
                ca_list = self.findUnqCards(['unstun'], prosp_hand)
                if ca_list:
                    cpi_val += cpiPosConstants['i become stunned with unstun available']
                else:
                    cpi_val += cpiPosConstants['i become stunned without unstun available']
            elif (attr == 'unstun') and ('stunned' in self.status):
                cpi_val += cpiPosConstants[attr]
            elif (attr == 'stun') and not ('stunned' in your_status):
                cpi_val += cpiPosConstants[attr]
            elif (attr == 'unwound') and ('wounded' in self.status):
                cpi_val += cpiPosConstants[attr]
            elif (attr == 'wound') and not ('wounded' in your_status):
                cpi_val += cpiPosConstants[attr]
            elif (attr == 'red'):
                cpi_val += cpiPosConstants['you must defend']
                total_cards_defender_loses += 1
            elif (attr == 'start faceoff'):
                cpi_val += self.detFaceoffStr(prosp_hand)
            else:
                cpi_val += cpiPosConstants['attr']
                if (attr == 'you discard') or (attr == 'you discard random'):
                    total_cards_defender_loses += 1
        if total_cards_defender_loses > your_hand_size:
            cpi_val = cpiPosConstants['instant win']
        elif total_cards_defender_loses = your_hand_size:            
            cpi_val += cpiPosConstants['you have zero cards']
        return cpi_val
        
        
        
    # cpi = Card Panel Index             
    def pickCard(self, your_hand_size, your_status, your_cards_played):
        'Input is "your" hand size, an integer, and "your" status, a set. Picks \
        which card to play, returned as a [card, panel] list, or possibly two \
        card list. Input is an integer and a set'
        self.best_cpi=[False] # final cpi to pick
        self.best_hand_val = -100 #top hand value       
        best_pos_val=-100 #top positon value (looking at the cpi)
        best_pos_cpi_list=[False] #list of top cpi's based their position

        for card in self.hand:
            for ii in range(len(allCards[card]['attr'])):
                cpi = []
                cpi.append(card)
                cpi.append(ii)
                if self.legal_play(cpi, self.init):
                    cpi_pos_val = self.calcCpiPosVal(cpi, your_status, self.init)
                    if cpi_pos_val >= best_pos_val:
                        best_pos_cpi_list.append(cpi)
                        best_pos_val = cpi_pos_val
                    if not('stunned' in self.status):
                        if 'caBlue' in allCards[cpi[0]]['attr'][cpi[1]]:
                            #determine all the possible counter-attacks that
                            #could be use, and try those
                            #TBD
##                            cpi_pos_val = self.calcCpiPosVal(cpi, your_status, self.init)
##                            if cpi_pos_val >= best_pos_val:
##                                best_pos_cpi_list.append(cpi)
##                                best_pos_val = cpi_pos_val

        #TBD
        if not self.best_cpi[0]:
            print 'No card available'
            return [False]
        else:
            self.print_cpi(self.best_cpi)
        print '======================='
        return self.best_cpi

                    
    
        
    #
    def pickCard2Discard(self):
        'look through the cards left in the hand and find best card to discard'
        local_val = -100
        if len(self.hand) < 2:
            return False
        for card in self.hand:
            if card != 'v1':
                cpi=[card,0]
                mhv = self.myHandValue(self.init, cpi, False)
                if mhv > local_val:
                    local_val = mhv
                    local_cpi = cpi
        print self.char,':pickCard2Discard: picked card ', local_cpi[0]
        return local_cpi[0]

    def pickRandomCard(self):
        'picks a random card. Assumes there is enough cards to do it.'
        real_deck = [rc for rc in self.hand if rc != 'v1']
        return choice(real_deck)
                    
    def applyMyCard2Me(self, card, pnl):
        'applys the effects of the card I played to myself. Return False if it \
        cannot be played'
        attr_l = allCards[card]['attr'][pnl]
        for attr in attr_l:
            if attr == 'stunned' or attr == 'wounded':
                self.status.add(attr)
            elif (attr == 'unstun') and ('stunned' in self.status):
                self.status.remove('stunned')
            elif (attr == 'unwound') and ('wounded' in self.status):
                self.status.remove('wounded')
            elif attr == 'draw':
                self.drawCards(1)
            elif attr == 'discard':
                if len(self.hand) < 2:
                    return False
                else:
                    card2discard = self.pickCard2Discard()
                    if not card2discard:
                        return False
                    else :
                        self.discardCard(card2discard)
            elif attr == 'discard random':
                if len(self.hand) < 2:
                    return False
                else:
                    self.discardCard(pickRandomCard)          
        return True
            
    def maxHandSz(self):
        'Returns current max hand size'
        if 'wounded' in self.status:
            return MAX_HAND - WOUNDED_HAND_EFFECT
        else:
            return MAX_HAND
    
    def playCard(self, cpi):
        'Play requested cpi. Only one card in will be played. Function will \
        discard played card and apply all status updates caused by the card \
        that effect *I* except for initiative. This does not effect *You*. \
        Returns False if play is impossible. Extra cards are discarded'
        if not self.applyMyCard2Me(cpi[0], cpi[1]):
            return False
        if dbg4<=2 : print self.char, 'playCard: about to discard ', cpi[0]
        if cpi[0] != 'v1': self.discardCard(cpi[0])
        self.checkHandSz()
        self.cards_played += 1
        return True  
        
    #??            
    def applyYourCard2Me(self,cpi):
        'apply the effects of the cpi you played on me. Return [True] if it \
        worked, [True, <card>] if a card was grabbed. [False] if it failed.'
        for attr in  allCards[cpi[0]]['attr'][cpi[1]]:
            if attr == 'stun': 
                self.status.add('stunned')
            elif attr == 'you discard': 
                if len(self.hand) < 2:
                    return [False]
                else:
                    self.discardCard(self.pickCard2Discard())                
            elif attr == 'you discard random': 
                if len(self.hand) < 2:
                    return [False]
                else:
                    self.discardCard(pickRandomCard)                
            elif attr == 'wound': 
                self.status.add('wounded')
                self.checkHandSz()
            elif attr == 'grab card': 
                if dbg <= 2: print self.char, ':applyYourCard2Me: you are grabbing a card'
                if len(self.hand) < 2:
                    return [False]
                else: 
                    gcard = self.pickRandomCard()
                    self.discardCard(gcard)
                    if dbg <= 2: print self.char, 'I lost card=', gcard
                    return [True, gcard]
        return [True]

        
