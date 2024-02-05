#The Player class represents both human and AI players, containing methods 
#representing each choice available for them.
class Player():
    #Each player contains a name, a number of chips, pocket cards, 
    #their current wager, a record of their hand strength, and whether they've 
    #folded.
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.pocket = []
        self.bet = 0
        self.hand_strength = [0, 0, 0]
        self.folded = False
    
    #If a player calls, their wager is set to the current betting value or
    #nothing changes in the event of a 'check'.
    #Invalid values for calls will be handled in the betting round itself.
    def playCall(self, value):
        if value == self.bet:
            print(self.name + " checks")
            return

        if value >= self.chips:
            print(self.name + " goes all in")
            self.bet = self.chips
        else:
            print(self.name + " calls")
            self.bet = value
        return
    
    #If a player raises, their wager is set to the value they raised to.
    #Invalid values for raises will be handled in the betting round itself.
    def playRaise(self, value):       
        if value >= self.chips:
            print(self.name + " goes all in")
            self.bet = self.chips
        else:
            print(self.name + " raises to " + str(value))
            self.bet = value
        return

    #If a player folds, their wager does not change and they are marked as 
    #having folded.
    def playFold(self):
        print(self.name + " folds")
        self.folded = True
        return

#The Round class represents aspects of a game of poker that are not directly
#related to any specific player, such as the community cards and the pot.
class Round():
    #The Round class contains the shuffled deck, a pseudo-pointer for the top 
    #of the deck, the value of the current pot, and the community cards.
    def __init__(self):
        self.deck = []
        self.deck_top = 0
        self.pot = 0
        self.community_cards = []
    
    #At the start of a game, the round class will deal the pocket cards to
    #each player.
    def dealPlayer(self, player, numCards):
        if numCards < 1:
            return
        
        for i in range(0, numCards):
            player.pocket.append(self.deck[self.deck_top + i])
            
        self.deck_top += numCards
        return
    
    #Between betting rounds, community cards will be dealt to the table.
    #Differing numbers of cards will be dealt at different times.
    def dealCommunity(self, numCards):
        if numCards < 1:
            return
        
        for i in range(0, numCards):
            self.community_cards.append(self.deck_top + i)
        
        self.deck_top += numCards
        return

    #After each round of betting, the players' wagers will be removed from 
    #their chips and added to the pot.
    def collectBets(self, players):
        for p in players:
            if p.bet < 0:
                p.bet = 0
            self.pot += p.bet
            p.chips -= p.bet
            p.bet = 0

        return
    
    #At the end of the game, the winning player has the pot's chips added to
    #their own.
    def payout(self, player):
        player.chips += self.pot
        self.pot = 0
        return
                    
        
        