# pseudo-global variables

mainDeck=[]
discardDeck=[]
maxHandSz=7

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

