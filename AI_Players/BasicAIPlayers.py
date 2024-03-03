import random
import sys
sys.path.append('..')
from Game import Player
from HandEvaluation import evaluateAllHands

#This AI player makes its decisions completely at random - making it the hardest
#to read.
class AIplayer_Random(Player):
    def assess(self, r):
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
    
    def choice(self, opponents, wager_value):
        decision_num = random.randint(1, 21)
        #The AI player only has a 5% chance of folding, to reduce the odds of
        #unneccessarily folding early on.
        if decision_num <= 2 and self.bet != wager_value:
            self.playFold()
        elif decision_num > 11 and self.last_move != "raise" and wager_value < self.chips:
            #If the AI decides to raise, the amount it raises to is a random
            #value in the valid range of wager_value to all of its chips
            raise_value = random.randint(wager_value, self.chips + 1)
            self.playRaise(raise_value)
            return raise_value
        else:
            self.playCall(wager_value)
        
        return wager_value

#This AI player always calls/checks, regardless of the situation or its hand's
#strength.
class AIplayer_AlwaysCall(Player):
    def assess(self, r):
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
    
    def choice(self, opponents, wager_value):
        self.playCall(wager_value)
        return wager_value

#This AI players will always bet all of its chips at the first opportunity it gets.  
class AIplayer_AlwaysAllIn(Player):
    def assess(self, r):
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
    
    def choice(self, opponents, wager_value):
        if wager_value >= self.chips:
            self.playCall(wager_value)
            return wager_value
        
        self.playRaise(self.chips)
        return self.chips

#This AI player will always call. However, if it doesn't achieve at least a pair
#from the first three community cards, it will fold.
class AIplayer_FoldIfNoPair(Player):
    def assess(self, r):
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
        self.community_number = len(r.community_cards)
    
    def choice(self, opponents, wager_value):
        if self.hand_strength[0] == 0 and self.community_number > 0:
            self.playFold()
            return wager_value
        
        self.playCall(wager_value)
        return wager_value

#This AI player will always call up to half of the chips it starts the round with.
#It will fold if it is forced to bet more than half of the chips it had at the 
#start of the round.    
class AIplayer_CallUpToHalf(Player):   
    def assess(self, r):
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
        self.community_number = len(r.community_cards)
        
        if self.community_number == 0:
            self.limit = self.chips / 2
    
    def choice(self, opponents, wager_value):
        if ((self.chips + self.bet) - wager_value) < self.limit:
            self.playFold()
            return wager_value
        
        self.playCall(wager_value)
        return wager_value
