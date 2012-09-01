# pseudo-global variables

#contains an array of the cards in the main deck
#this is contstructed from the dCards dictionary keys
mainDeck=[] 

#contains an array of the cards discarded, built up during play
discardDeck=[]

maxHandSz=7

<<<<<<< HEAD
standardDeck = ['01','02','03','04','05','06','07','08',
                '09','10','11','12','13','14','15','16',
                '17','18','19','20','21','22','23','24',
                '25','26','27','28','29','30','31','32',
                '33','34','35','36','37','38','39','40',
                '41','42','43','44','45','46','47','48',
                '49','50','51','52','53','54']

#dCards is a dictionary with keys = card ID and the values are a list of panel IDs
dCards = {
     '01' : {'panels' : ['attack', 'recover'],'faceoffVal' : 12.0},
=======
#1to1
#2to1
#3to1
odds=''

#dCards is a dictionary with keys = card ID and the values are a list of panel IDs
# copied from the old design
dCards = {
     '01' : {'panels' : ['attack', 'recover'],'faceoffVal' : 12},
>>>>>>> 69ba06c956a841a9fce2655e596a61e977ffc853
     '02' : {'panels' : ['attack', 'wounded'],'faceoffVal' : 11.0},
     '03' : {'panels' : ['attack', 'disengage'],'faceoffVal' : 10.0},
     '04' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' :  9.0},
     '05' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' :  8.0},
     '06' : {'panels' : ['attack', 'counterAttack'],'faceoffVal' :  7.0},
     '07' : {'panels' : ['attack'],'faceoffVal' : 6.0},
     '08' : {'panels' : ['attack', 'catchABreath1', 'catchABreath2'],'faceoffVal' : 5.0},
     '09' : {'panels' : ['attack'],'faceoffVal' : 4.0},
     '10' : {'panels' : ['attack', 'againstAllOdds'],'faceoffVal' : 3.0},
     '11' : {'panels' : ['attack'],'faceoffVal' :  2.0},
     '12' : {'panels' : ['attack'],'faceoffVal' : 1.0},
     '13' : {'panels' : ['dodge', 'counterAttack'],'faceoffVal' : 0},
     '14' : {'panels' : ['dodge', 'wounded'],'faceoffVal' : 0},
     '15' : {'panels' : ['dodge', 'disengage'],'faceoffVal' : 0},
     '16' : {'panels' : ['dodge', 'recover'],'faceoffVal' :  0},
     '17' : {'panels' : ['dodge', 'wounded'],'faceoffVal' : 0},
     '18' : {'panels' : ['dodge', 'disengage'],'faceoffVal' : 0},
     '19' : {'panels' : ['dodge', 'recover'],'faceoffVal' : 0},
     '20' : {'panels' : ['dodge', 'wounded'],'faceoffVal' : 0},
     '21' : {'panels' : ['disengage', 'againstTheOdds'],'faceoffVal' : 0},
     '22' : {'panels' : ['disengage'],'faceoffVal' :  0},
     '23' : {'panels' : ['stunned', 'catchABreath1', 'catchABreath2'],'faceoffVal' :  0},
     '24' : {'panels' : ['stunned'],'faceoffVal' :  0},
     '25' : {'panels' : ['wounded'],'faceoffVal' :  0},
     '26' : {'panels' : ['recover'],'faceoffVal' :  0},
     '27' : {'panels' : ['ultraDodge'],'faceoffVal' : 0},
     '28' : {'panels' : ['attack'],'faceoffVal' : 4.0}}

<<<<<<< HEAD
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
=======
# information about each panel
#
# ATTRIBUTES
# things the card does: 
#    stunned
#    you are stunned, 
>>>>>>> 69ba06c956a841a9fce2655e596a61e977ffc853
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
<<<<<<< HEAD
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
=======
#    wounded
#    unwound
#    you are wounded
#
# RESTRICTIONS
# for 'restr' you must have the entire list matching to use the card
>>>>>>> 69ba06c956a841a9fce2655e596a61e977ffc853
# not stunned
# not wounded
# prev card not green
# 2to1
# 3to1
# not in faceoff
<<<<<<< HEAD
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

=======
# 'few cards'

dPanels = {'dodge' : {'attr':['caBlue'],
                      'color':['blue'],
                      'restr':[],
                      'value':1.0},
           'reversal' : {'attr':['gain initiative'],
                      'color':['blue'],
                       'restr':[],
                       'value':1.0},
           'ultraDodge' : {'attr':['draw'],
                      'color':['blue'],
                       'restr':[],
                       'value':1.0},
           'megaDodge' : {'attr':['draw'],
                      'color':['blue'],
                       'restr':[],
                       'value':1.0},
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


# A dictionary of cards indicating what panels they have and the faceoff value
#dCards = {
#    '01' : {'panels' : ['01A', '01B'], 'faceoffVal' : 12.0}, 
#    '02' : {['02A']}, 
#    '03' : {['03A', '03B']}, 
#    '04' : {['04A']}, 
#    '05' : {['05A']}, 
#    '06' : {['06A']}, 
#    '07' : {['07A']}, 
#    '08' : {['08A']}, 
#    '09' : {['09A']}, 
#    '10' : {['10A']}, 
#    '11' : {['11A']}, 
#    '12' : {['12A']}, 
#    '13' : {['13A']}, 
#    '14' : {['14A']}, 
#    '15' : {['15A']}, 
#    '16' : {['16A']}, 
#    '17' : {['17A']}, 
#    '18' : {['18A']}, 
#    '19' : {['19A']}, 
#    '20' : {['20A']}, 
#    '21' : {['21A']}, 
#    '22' : {['22A']}, 
#    '23' : {['23A']}, 
#    '24' : {['24A']}, 
#    '25' : {['25A']}, 
#    '26' : {['26A']}, 
#    '27' : {['27A']}, 
#    '28' : {['28A']}, 
#    '29' : {['29A']}, 
#    '30' : {['30A']}, 
#    '31' : {['31A']}, 
#    '32' : {['32A']}, 
#    '33' : {['33A']}, 
#    '34' : {['34A']}, 
#    '35' : {['35A']}, 
#    '36' : {['36A']}, 
#    '37' : {['37A']}, 
#    '38' : {['38A']}, 
#    '39' : {['39A']}, 
#    '40' : {['40A']}, 
#    '41' : {['41A']}, 
#    '42' : {['42A']}, 
#    '43' : {['43A']}, 
#    '44' : {['44A']}, 
#    '45' : {['45A']}, 
#    '46' : {['46A']}, 
#    '47' : {['47A']}, 
#    '48' : {['48A']}, 
#    '49' : {['49A']}, 
#    '50' : {['50A']}, 
#    '51' : {['51A']}, 
#    '52' : {['52A']}, 
#    '53' : {['53A']}, 
#    '54' : {['54A']}
#}


# card numbers in a standard deck
#standardDeck = ['01','02','03','04','05','06','07','08',
#                '09','10','11','12','13','14','15','16',
#                '17','18','19','20','21','22','23','24',
#                '25','26','27','28','29','30','31','32',
#                '33','34','35','36','37','38','39','40',
#                '41','42','43','44','45','46','47','48',
#                '49','50','51','52','53','54']

>>>>>>> 69ba06c956a841a9fce2655e596a61e977ffc853
