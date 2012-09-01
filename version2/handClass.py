
class Hand:

    def __init__(self, num):
        'constructor. Draws an initial hand as panels'
        self.panels = []
        self.initialDraw()
   
    def add2hand(self, card):
        'Inserts a card into hand. The card is converted into panels as it goes\
        in Note, discard if handsize is too big is done seperately. THIS IS ON PURPOSE'
        
                  
    def drawCards(self, N):
        'draw N cards from main deck into hand and update the hand. Cards are\
        removed from mainDeck and panels go into self.panels'
 
    def handSz(self):
        'returns the hand size. Virtual cards are ignored'
        
    def checkHandSz(self):
        'Determines if you have too many cards in your hands and if so discards \
        until you have the correct number'
        while handSz() > tv.maxHandSz:
            card = self.pickCard2Discard()
            self.discardCard(card)
            print self.char, 'discard ', card, 'due to excessive hand size'
            
    def initialDraw(self):
        'do the initial draw of the hand and add in virtual cards'
        self.drawCards(tv.maxHandSz)
        self.add2hand('99A')
            
    def discardCard(self, card):
        'discard a particular card. the v1 card cannot be discarded'

    def panel2card(self,l_panel):
        'returns the card associated with l_panel'
        
    def card2panels(self,l_card):
        'returns a list of panels associated with l_card'
        
