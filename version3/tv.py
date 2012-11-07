# pseudo-global variables

#contains an array of the cards in the main deck
#this is contstructed from the dCards dictionary keys
mainDeck=[] 

#contains an array of the cards discarded, built up during play
discardDeck=[]

maxHandSz=7

#1to1
#2to1
#3to1
odds=''

#dCards is a dictionary with keys = card ID and the values are a list of panel IDs
dCards = {
     '01' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' : 1.0},
     '02' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' : 2.0},
     '03' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' : 3.0},
     '04' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' :  4.0},
     '05' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' :  5.0},
     '06' : {'panels' : ['attack', 'disengage'],'faceoffVal' :  6.0},
     '07' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' : 7.0},
     '08' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' : 8.0},
     '09' : {'panels' : ['attack', 'disengage'],'faceoffVal' : 9.0},
     '10' : {'panels' : ['attack', 'disengage'],'faceoffVal' : 10.0},
     '11' : {'panels' : ['attack', 'megaAttack'],'faceoffVal' :  11.0},
     '12' : {'panels' : ['attack', 'megaAttack'],'faceoffVal' : 12.0},
     '13' : {'panels' : ['attack', 'escape'],'faceoffVal' : 13.0},
     '14' : {'panels' : ['attack', 'escape'],'faceoffVal' : 14.0},
     '15' : {'panels' : ['attack', 'escape'],'faceoffVal' : 15.0},
     '16' : {'panels' : ['attack', 'escape'],'faceoffVal' : 16.0},
     '17' : {'panels' : ['attack', 'reversal'],'faceoffVal' : 17.0},
     '18' : {'panels' : ['attack', 'reversal'],'faceoffVal' : 18.0},
     '19' : {'panels' : ['attack', 'stunningAttack'],'faceoffVal' : 19.0},
     '20' : {'panels' : ['attack', 'stunningAttack'],'faceoffVal' : 20.0},
     '21' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' : 21.0},
     '22' : {'panles' : ['wounded', 'killingAttack'],'faceoffVal' : 0.0},
     '23' : {'panels' : ['attack', 'wounded'],'faceoffVal' : 22.0},
     '24' : {'panels' : ['attack', 'megaAttack'],'faceoffVal' : 23.0},
     '25' : {'panels' : ['attack', 'megaAttack'],'faceoffVal' : 24.0},
     '26' : {'panels' : ['defend', 'killingAttack'],'faceoffVal' : 0},
     '27' : {'panels' : ['defend', 'unusualAttack'],'faceoffVal' : 0},
     '28' : {'panels' : ['defend', 'unusualAttack'],'faceoffVal' : 0},
     '29' : {'panels' : ['defend', 'unusualAttack'],'faceoffVal' : 0},
     '30' : {'panels' : ['defend', 'unusualAttack'],'faceoffVal' : 0},
     '31' : {'panels' : ['defend', 'megaDefend'],'faceoffVal' : 0},
     '32' : {'panels' : ['defend', 'megaDefend'],'faceoffVal' : 0},
     '33' : {'panels' : ['defend', 'counterAttack'],'faceoffVal' : 0},
     '34' : {'panels' : ['recover'],'faceoffVal' : 0},
     '35' : {'panels' : ['defend', 'counterAttack'],'faceoffVal' :  0},
     '36' : {'panels' : ['defend', 'megaDefend'],'faceoffVal' : 0},
     '37' : {'panels' : ['defend', 'megaDefend'],'faceoffVal' : 0},
     '38' : {'panels' : ['defend', 'againstTheOdds'],'faceoffVal' : 0},
     '39' : {'panels' : ['defend', 'againstTheOdds'],'faceoffVal' : 0},
     '40' : {'panels' : ['defend', 'againstAllOdds'],'faceoffVal' : 0},
     '41' : {'panels' : ['defend', 'againstAllOdds'],'faceoffVal' : 0},
     '42' : {'panels' : ['wounded', 'feint'],'faceoffVal' : 0},
     '43' : {'panels' : ['wounded', 'feint'],'faceoffVal' : 0},
     '44' : {'panels' : ['wounded'],'faceoffVal' : 0},
     '45' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' : 25.0},
     '46' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' : 26.0},
     '47' : {'panels' : ['stunned', 'uncannyRecovery'],'faceoffVal' : 0},
     '48' : {'panels' : ['stunned'],'faceoffVal' : 0},
     '49' : {'panels' : ['stunned'],'faceoffVal' : 0},
     '50' : {'panels' : ['stunned'],'faceoffVal' : 0},
     '51' : {'panels' : ['disengage', 'uncannyRecovery'],'faceoffVal' : 0},
     '52' : {'panels' : ['disengage'],'faceoffVal' :  0},
}

#dPanels is a disctionary with keys = paned IDs and the values are a dictionary with
#all the panel characteristics
#
# ATTRIBUTES
# things the card does (note, by default the terms are about 'i' not 'you'): 
#    stunned
#    you are stunned, 
#    unstunned, 
#    start faceoff, 
#    caBlue    -- this means it can be used to trigger a counter-attack
#    counter attack
#    gain initiative, 
#    lose initiative, 
#    draw, 
#    grab card, 
#    discard, 
#    discard random,
#    you discard
#    you discard random
#    wounded
#    unwounded
#    you are wounded

#
# RESTRICTIONS
# for 'restr' you must have the entire list matching to use the card
# not stunned
# not wounded
# prev card not green
# 2to1
# 3to1
# not in faceoff
# 'few cards'

dPanels = {'defend' : {'attr':['caBlue'],
                      'color':['blue'],
                      'restr':[],
                      'value':1.0},
           'reversal' : {'attr':['gain initiative'],
                      'color':['blue'],
                       'restr':[],
                       'value':2.0},
           'megaDefend' : {'attr':['draw','caBlue'],
                      'color':['blue'],
                       'restr':[],
                       'value':2.0},
           'megaDodge' : {'attr':['gain initiative'],
                      'color':['blue'],
                       'restr':[],
                       'value':2.0},
          'stunned' : {'attr':['draw', 'draw', 'stunned'],
                      'color':['blue'],
                       'restr':['not stunned'],
                       'value':1.0,
          'recover' : {'attr':['unstun'],
                      'color':['blue'],
                       'restr':[], 
                       'value':1.5},                    
          'wounded' : {'attr':['draw','wounded'],
                      'color':['blue'],
                       'restr':['not wounded'],
                       'value':1.0},                    
          'disengage' : {'attr':['start faceoff'],
                         'color':['blue'],
                         'restr':['not in faceoff'],
                         'value':1.0},        
          #Note that a counterAttack is a low value by itself but gains point
          #value for a caPair
          'counterAttack' : {'attr':['gain initiative','draw','counter attack'],
                             'color':['red'],
                             'restr':['not stunned', 'after caBlue'], 
                             'value':1.5},       
          'attack' : {'attr':['draw'],
                      'color':['red'],
                      'restr':['not stunned'],
                      'value':1.0},
          'catchABreath1' : {'attr':['lose initiative','draw', 'draw', 'draw'],
                             'color':['green'],
                             'restr':['prev card not green'], 
                             'value':1.0},            
          'catchABreath2' : {'attr':['draw','unstun'],
                             'color':['green'],
                             'restr':['prev card not green'],
                             'value':0.0},
          'inACorner' : {'attr':['draw','draw','draw'],
                              'color':['blue'],
                              'restr':['2to1','few cards'],
                             'value':0.0},
          'againstTheOdds' : {'attr':['draw','draw','draw'],
                              'color':['blue'],
                              'restr':['2to1'],
                             'value':0.0},
          'againstAllOdds' : {'attr':['draw','draw','draw'],
                              'color':['blue'],
                              'restr':['blue', '3to1'],
                             'value':0.0},
          'inflictWound' : {'attr':['draw','you are wounded'],
                            'color':['red'],
                            'restr':[],
                            'value':1.5},    
          'inflictStun' : {'attr':['draw','you are stunned'],
                           'color':['red'],
                           'restr':[],
                           'value':2.5},     
          'unusualStun' : {'attr':['draw','you are stunned'],
                           'color':['green'], 'restr': ['prev card not green'], 'value':2.5},
          'damageShield' : {'attr':['you discard'],
                            'color':['blue'], 'restr': [], 'value':1.5},
          'grabCard' : {'attr':['grab card'],
                        'color':['green'],
                        'restr':['prev card not green'],
                        'value':1.5},     
          'inflictDiscard' : {'attr':['draw','you discard'],
                              'color':['green'],
                              'restr':['prev card not green'],
                              'value':1.1},             
          'passInitiative1' : {'attr': ['draw','draw','lose initiative','discard'],
                               'color':['green'],
                               'restr': [],
                               'value':0.0},
          'passInitiative2' : {'attr': ['unstun', 'lose initiative'],
                               'color':['green'],
                               'restr': [],
                               'value':0.0}
            }

