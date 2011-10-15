__metaclass__ = type #use Python 3 classes
dbg = 4
dbg2 = 4
dbg3 = 0 #hand value determination
dbg4 = 4 #draw/discard cards
dbg5 = 4 #handle_ca debug

# Other hand constans
SEC_PANEL_WT = 0.3 #how much to weight the value of the 2nd panel
FACEOFF_WT = 0.02 #how much to weight the faceoff value of the card
MEAN_CARD_VAL = 1.2 #mean value of a card, mi
ALL_ODDS_VAL = 1.5 #the value of having that card/panel in the right odds
INITIATIVE_VAL = 4.0
MAX_FACEOFF = 12.0
MAX_HAND = 7
WOUNDED_HAND_EFFECT = 1 #how much is hand size reduced


##+ BLUE cards
##+++ Standard
##Dodge This card acts as a defense.
##Stunned: I cannot play this card if I am stunned. This card acts as a defense. In addition I am
##  Stunned and I draw 2 cards.
##Recover: This card acts as a defense and I am no longer Stunned.
##Wounded: I cannot play this card if I am already Wounded this fight. This card acts as a defense.
##  In addition I draw 1 card and my maximum hand size is reduced to 5 for the rest of this fight.
##Disengage: This card acts as a defense and a new Face-Off immediately occurs after playing this card.
##  I cannot play this during a Face-Off.
##Against the Odds: I can only play this card if I started the fight outnumbered.
##  This card acts as a defense, I gain the initiative, and I draw 3 cards.
##Against All Odds: I can only play this card if I started the fight outnumbered more than 2-1.
##  This card acts as a defense and I draw 3 cards.
##Lucky Break: I can only play this card if I have less than 4 cards. This card acts as a defense and I draw 2 cards.

##+ RED cards
##+++ Standard 
##Attack: You must play a BLUE card to defend. I draw a card and retain the initiative.
##Counter-Attack: This card is only played immediately after I play a BLUE card other than Disengage.
##  I gain the initiative, you must play a BLUE card to defend and I draw a card.

##+ Standard GREEN card
##Catch a Breath: I can either: lose the initiative and draw 3 cards OR
##  recover from being Stunned (if I am stunned), draw 1 card and retain the initiative.

#DATA STRUCTURES

#dCards is a dictionary with keys = card ID and the values are a list of panel IDs
dCards = {
     'sc1' : {'panels' : ['attack', 'recover'],'faceoffVal' : MAX_FACEOFF},
     'sc2' : {'panels' : ['attack', 'wounded'],'faceoffVal' : 11.0},
     'sc3' : {'panels' : ['attack', 'disengage'],'faceoffVal' : 10.0},
     'sc4' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' :  9.0},
     'sc5' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' :  8.0},
     'sc6' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' :  7.0},
     'sc7' : {'panels' : ['attack'],'faceoffVal' : 6.0},
     'sc8' : {'panels' : ['attack', 'catchABreath1', 'catchABreath2'],'faceoffVal' : 5.0},
     'sc9' : {'panels' : ['attack'],'faceoffVal' : 4.0},
     'sc10' : {'panels' : ['attack', 'againstAllOdds'],'faceoffVal' : 3.0},
     'sc11' : {'panels' : ['attack'],'faceoffVal' :  2.0},
     'sc12' : {'panels' : ['attack'],'faceoffVal' : 1.0},
     'sc13' : {'panels' : ['dodge', 'counterAttack'],'faceoffVal' : 0},
     'sc14' : {'panels' : ['dodge', 'wounded'],'faceoffVal' : 0},
     'sc15' : {'panels' : ['dodge', 'disengage'],'faceoffVal' : 0},
     'sc16' : {'panels' : ['dodge', 'recover'],'faceoffVal' :  0},
     'sc17' : {'panels' : ['dodge', 'wounded'],'faceoffVal' : 0},
     'sc18' : {'panels' : ['dodge', 'disengage'],'faceoffVal' : 0},
     'sc19' : {'panels' : ['dodge', 'recover'],'faceoffVal' : 0},
     'sc20' : {'panels' : ['dodge', 'wounded'],'faceoffVal' : 0},
     'sc21' : {'panels' : ['disengage', 'againstTheOdds'],'faceoffVal' : 0},
     'sc22' : {'panels' : ['disengage'],'faceoffVal' :  0},
     'sc23' : {'panels' : ['stunned', 'catchABreath1', 'catchABreath2'],'faceoffVal' :  0},
     'sc24' : {'panels' : ['stunned'],'faceoffVal' :  0},
     'sc25' : {'panels' : ['wounded'],'faceoffVal' :  0},
     'sc26' : {'panels' : ['recover'],'faceoffVal' :  0},
     'sc27' : {'panels' : ['ultraDodge'],'faceoffVal' : 0},
     'sc28' : {'panels' : ['attack'],'faceoffVal' : 4.0},
     'v1' : {'panels' : ['passInitiative1', 'passInitiative2', 'passInitiative3'],'faceoffVal' : 0},
     'shadow 1' : {'panels' : ['inflictWound'],'faceoffVal' : 2.0},
     'logos 11' : {'panels' : ['attack', 'grabCard'],'faceoffVal' : 0}}

#dPanels is a disctionary with keys = paned IDs and the values are a dictionary with
#all the panel characteristics
#
# ATTRIBUTES
#things the card does: 
#    blue, 
#    red, 
#    green, 
#    stunned, 
#    stun, 
#    unstun, 
#    start faceoff, 
#    caBlue
#    gain initiative, 
#    lose initiative, 
#    draw, 
#    grab card, 
#    discard, 
#    discard random,
#    you discard
#    you discard random
#    wound
#    unwound
#Note that the same attribute could be on the list multiple times, for example
# 'draw', 'draw' would means you draw twice.__debug__
#
# RESTRICTIONS
#things that prevent you from playing the card: 
#
#  blue
# red
# green
# not stunned
# not wounded
# prev card not green
# 2to1
# 3to1
# not in faceoff
#When the panel is looked at to determine if you can play it, iterate through the restrictions 
#list to seeif you can meet all the requirement. Ex, I'm checking to see if I can play attack. 
#  Can I play 'red'? Am i 'not stunned'? If both are true then you're good
#
#caBlue means it's a blue card that can be used for a counterattack
#
 #passInitiative1/2 are synthetic card/panel values that passed
          #up to the main control when you have the initiative and don't
          #play a card and instead pass initiative to your opponent.
          # They are given no value so to 'play' them costs nothing
dPanels = {'dodge' : {'attr':['blue','caBlue'],
                       'restr':['blue'],
                       'value':1.0},
           'ultraDodge' : {'attr':['blue', 'gain initiative'],
                       'restr':['blue'],
                       'value':1.0},
          'stunned' : {'attr':['blue','draw', 'draw', 'stunned'],
                       'restr':['blue', 'not stunned'],
                       'value':0.5},
          'recover' : {'attr':['blue','unstun'],
                       'restr':['blue'], 
                       'value':2.0},                    
          'wounded' : {'attr':['blue','draw','wounded'],
                       'restr':['blue', 'not wounded'],
                       'value':1.0},                    
          'disengage' : {'attr':['blue','start faceoff'],
                         'restr':['blue', 'not in faceoff'],
                         'value':1.0},        
          #Note that a counterAttack is a low value by itself but gains point
          #value for a caPair
          'counterAttack' : {'attr':['red','gain initiative','draw','counter attack'],
                             'restr':['red', 'not stunned', 'after caBlue'], 
                             'value':1.5},       
          'attack' : {'attr':['red','draw'],
                     'restr':['red'],
                     'value':1.0},
          'catchABreath1' : {'attr':['green','lose initiative','draw', 'draw', 'draw'],
                             'restr':['green', 'prev card not green'], 
                             'value':1.0},            
          'catchABreath2' : {'attr':['green','draw','unstun'],
                             'restr':['green', 'prev card not green'],
                             'value':0.0},
          'againstTheOdds' : {'attr':['blue','draw','draw','draw'],
                              'restr':['blue', '2to1'],
                             'value':0.0},
          'againstAllOdds' : {'attr':['blue','draw','draw','draw'],
                              'restr':['blue', '3to1'],
                             'value':0.0},
          'inflictWound' : {'attr':['red','draw','wound'],
                            'restr':['red'],
                            'value':1.5},    
          'inflictStun' : {'attr':['red','draw','stun'],
                            'restr':['red'],
                            'value':2.5},     
          'grabCard' : {'attr':['green','grab card'],
                            'restr':['green', 'prev card not green'],
                            'value':2.0},     
          'inflictDiscard' : {'attr':['green','draw','you discard'],
                            'restr':['green', 'prev card not green'],
                            'value':1.5},             
          'passInitiative1' : {'attr': ['green', 'draw', 'lose initiative'],
                               'restr': ['green'],
                               'value':0.0},
          'passInitiative2' : {'attr': ['green', 'unstun', 'lose initiative'],
                               'restr': ['green'],
                               'value':0.0},
          'passInitiative3' : {'attr': ['green', 'discard', 'discard', \
                              'discard', 'draw', 'draw','draw','lose initiative'],
                               'restr': ['green'],
                               'value':0.0}
            }

#A dictionary containing the cards of each chars deck
charDeck = {'panzer':['sc1', 'sc2', 'sc3', 'sc4',
            'sc5', 'sc6', 'sc7', 'sc8',
            'sc9', 'sc10', 'sc11', 'sc12',
            'sc13', 'sc14', 'sc15', 'sc16',
            'sc17', 'sc18', 'sc19', 'sc20',
            'sc21', 'sc22', 'sc23', 'sc24',
            'sc25', 'sc26', 'sc27', 'sc28'],
            'logos':['sc1', 'sc2', 'sc3', 'sc4',
            'sc5', 'sc6', 'sc7', 'sc8',
            'sc9', 'sc10', 'logos 11', 'sc12',
            'sc13', 'sc14', 'sc15', 'sc16',
            'sc17', 'sc18', 'sc19', 'sc20',
            'sc21', 'sc22', 'sc23', 'sc24',
            'sc25', 'sc26', 'sc27', 'sc28'],
            'shadow':['sc1', 'sc2', 'sc3', 'sc4',
            'sc5', 'sc6', 'sc7', 'sc8',
            'sc9', 'sc10', 'sc11', 'sc12',
            'sc13', 'sc14', 'sc15', 'sc16',
            'sc17', 'sc18', 'sc19', 'sc20',
            'sc21', 'sc22', 'sc23', 'sc24',
            'sc25', 'sc26', 'sc27', 'sc28'],
            'warhawk':['sc1', 'sc2', 'sc3', 'sc4',
            'sc5', 'sc6', 'sc7', 'sc8',
            'sc9', 'sc10', 'sc11', 'sc12',
            'sc13', 'sc14', 'sc15', 'sc16',
            'sc17', 'sc18', 'sc19', 'sc20',
            'sc21', 'sc22', 'sc23', 'sc24',
            'sc25', 'sc26', 'sc27', 'sc28'],
            'zcrafter':['sc1', 'sc2', 'sc3', 'sc4',
            'sc5', 'sc6', 'sc7', 'sc8',
            'sc9', 'sc10', 'sc11', 'sc12',
            'sc13', 'sc14', 'sc15', 'sc16',
            'sc17', 'sc18', 'sc19', 'sc20',
            'sc21', 'sc22', 'sc23', 'sc24',
            'sc25', 'sc26', 'sc27', 'sc28'],
            'virtual':['v1']}

# Constants for controlling the weighting of position values
myPosWt = {'have a red':0.0,
           'have a blue':0.5,
           'have a blue while on def':1,
           'have a red while on atk':0.0,
           'blueStunUnstunPair':1,
           'blueStunUnstunPair while stunned':0.8,
           'caPair':[1,2,2.5,2.6],
           'caPair while stunned':[0.5,1,1.25,1.3],
           'number of reversers':[3,5,6.5,7,7.1,7.2,7.3,7.4]
           }
           


my_stat_val = {'stunned' : -3, #should I have a better version of this?
               'wounded' : -1.7} #should I have a better version of this?
#               'discard' : -0.66 * MEAN_CARD_VAL,
#               'lose card' : -0.66 * MEAN_CARD_VAL,
#               'discard random' : -MEAN_CARD_VAL,
#               'lose card random' : -MEAN_CARD_VAL} }


# Constants connecting status to numerical values for opponents hand           
your_stat_val = {'stunned' : -3,
                 'wounded' : -1.5,
                 'must play blue' : -1.1,
                 'can reverse' : 0.5,
                 'you discard' : -0.66 * MEAN_CARD_VAL,
                 'you lose card' : -0.66 * MEAN_CARD_VAL,
                 'you discard random' : -MEAN_CARD_VAL,
                 'you lose card random' : -MEAN_CARD_VAL}           


# a dictionary that contains all the card information, this is what is
# called when the drawCards function is used, it copies from here
# To find all the card information, iterate through all charDeck
# and add the card names to a set. This will eliminate redundancies. Then
# iterate over that list to create allCards. That should have every card
# in it.
#
# allCards format:
#  {'sc1' : {'price':1.3, 'restr': [['blue'], ['blue', 'unwounde']], 'draw': [0,1], 
#  'attr':[['blue', 'caBlue'], ['blue', 'draw', 'wounded']], 'faceoffVal':0},
#   'sc2'.....}    

allCards = {}

def setup_all_cards():
    'create the allCards dictionary'
    print 'Creating the allCards dictionary'
    allCardsSet=set()
    for char in charDeck.keys():
        allCardsSet.update(charDeck[char])
    print 'allCardsSet', allCardsSet  
    allCardsList=list(allCardsSet)
    print 'allCardsList', allCardsList
    for card in allCardsList: 
        add_card_data(card)

def add_card_data(card):
    'return card data '
    panels = dCards[card]['panels']
    panelList=[]
    attrList=[]
    restrList=[]
    for panel in panels: #make lists
        panelList.append(panel)    
        attrList.append(dPanels[panel]['attr'])
        restrList.append(dPanels[panel]['restr'])
    foo={}
    foo['attr'] = attrList
    foo['restr'] = restrList
    foo['faceoffVal'] = dCards[card]['faceoffVal']
    foo['price'] = calc_card_price(card)
    allCards[card]=foo
    
    
def calc_card_price(card):
    'create a dictionary with values indicating the card values for my deck' 
#    print 'calt_card_price: card = ',card          
    panelPriceList = []
    for panel in dCards[card]['panels']:
        foundVal = dPanels[panel]['value']
        if foundVal >= 0: panelPriceList.append(foundVal)
#    print 'calc_card_price: panelPriceList = ', panelPriceList
    if len(panelPriceList) > 1:
        cardPrice = max(panelPriceList) + SEC_PANEL_WT * min(panelPriceList)
    else: cardPrice = panelPriceList[0]
    if dCards[card]['faceoffVal'] > 0:
        cardPrice += dCards[card]['faceoffVal'] * FACEOFF_WT
    return cardPrice
            

#constants for determining the value of opponents cards. Note the
#non-linear droppoff as the number of cards increases
yourHandValue = { 0: 1,
                 1: 2.5,
                  2: 4,
                  3: 5.2,
                  4: 6.4,
                  5: 7.6,
                  6: 8.8,
                  7: 9.8}
                  
#Constants for determining cpi positional value
#These only kick in if relavent (ie, they can actually effect you)
cpiPosContants = {'i become stunned without unstun available' : -2.0,
                  'i become stunned with unstun available' : -1.0,
                  'you become stunned' : 2.0,
                  'i become unstunned' : 2.0
                  'i become wounded' : -1.0,
                  'you become wounded' : 1.0,
                  'i become unwounded' : 1.0
                  'i must discard' : -0.8,
                  'you must discard' : 1.0,
                  'you must discard random' : 1.0,
                  'instant win' : 100.0,
                  'you have no cards left' : 3.0,
                  'you must defend' : 1.0
                  }           
                  

