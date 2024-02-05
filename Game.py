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
        self.called = False
    
    #If a player calls, their wager is set to the current betting value or
    #nothing changes in the event of a 'check'.
    #Invalid values for calls will be handled in the betting round itself.
    def playCall(self, value):
        self.called = True
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

#This class represents a human player and takes user inputs for decisions,
#unlike AI.
class humanPlayer(Player):
    def choice(self, wager_value):
        while True:
            #A user is input is taken and split into 2 to determine their move.
            decision = input("What is your move? ").split(None, 2)
            move = decision[0].lower()
            #If the user inputs "bet", this is corrected to "raise"
            if move == "bet":
                move = "raise"
            
            match move:
                #If the user's move was to fold, the fold method is called.
                case "fold":
                    self.playFold()
                    break
                #If the user's move was to call, the call method is called.
                case "call":
                    self.playCall(wager_value)
                    break
                #If the user's move was to check, it is first checked whether
                #they can check before executing the call method with their
                #current bet.
                case "check":
                    if self.bet != wager_value and self.bet != self.chips:
                        print("Invalid: Can not currently 'check'")
                        continue
                    
                    self.playCall(self.bet)
                    break
                #If the user's move was to raise, it is checked whether they can
                #and if their raising value is valid.
                case "raise":
                    #The second part of the user's input is cast to an integer.
                    #If this fails, the user has not inputted a valid wager and
                    #is rejected.
                    try:
                        wager = int(decision[1])
                    except:
                        print("Error: Invalid wager value")
                        continue
                    
                    #If the user has attempted to raise to a value lower than
                    #the highest opponent bet, it is invalid and rejected.
                    if wager <= wager_value:
                        print("Error: Wager too low")
                        continue
                    #If the user has fewer chips than needed to exceed the
                    #wager value, they are forced to call by going all in.
                    elif wager_value > self.chips:
                        self.playCall(wager_value)
                        break
                    
                    #The 'playRaise' method is called with the user's wager
                    #and the new wager is returned to be the new wager value
                    #that other players must match.
                    self.playRaise(wager)
                    wager_value = wager
                    break
                #If the user inputs something else, it is invalid and rejected.
                case _:
                    print("Unknown: " + "\'" + str(move) + "\' is not a valid choice")
        
        return wager_value
        

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

    #Between the dealing of cards, players engage in a round of betting,
    #facilitated by this method
    def bettingRound(self, players):
        #The initial wager of each round is 0, allowing any raise value or check.
        wager_value = 0
        #The number of folded players is tracked so that the round ends if only
        #1 player hasn't folded.
        num_folded = 0
        for p in players:
            if p.folded:
                num_folded += 1

        #The betting round endlessly iterates between players until 1 of 2
        #possible conditions is met.
        while True:
            for p in players:
                #If a player is folded, their turn is skipped.
                if p.folded:
                    continue
                
                #The number of players whose last move was 'call' is calculated.
                num_called = 0
                for i in players:
                    if i.called:
                        num_called += 1
                
                #If either all but one players have folded or all players have
                #called, the round ends.
                if (num_folded == len(players) - 1 or 
                    num_called == len(players)):
                    return
                
                #The current player makes their move, based on the current
                #wager value.
                wager_value = p.choice(wager_value)
                #If the current player folds, this is tracked.
                if p.folded:
                    num_folded += 1
                    
                    

if __name__ == "__main__":
    a = humanPlayer("A", 500)
    b = humanPlayer("B", 500)
    r = Round()
    r.bettingRound([a, b])
    print(a.bet)
        
        