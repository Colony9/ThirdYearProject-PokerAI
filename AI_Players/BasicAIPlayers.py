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

    def review(self, winner, opp_folded, big_blind):
        return

#This AI player always calls/checks or raises by 1 chip, regardless of the 
#situation or its hand's strength.
class AIplayer_AlwaysCallOrLowRaise(Player):
    def assess(self, r):
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
    
    def choice(self, opponents, wager_value):
        if wager_value > self.chips:
            self.playCall(wager_value)
            return wager_value
        elif opponents[0].last_move is None or opponents[0].last_move == "raise" or self.last_move != "raise":
            self.playRaise(wager_value + 1)
            return wager_value + 1
        
        self.playCall(wager_value)
        return wager_value

    def review(self, winner, opp_folded, big_blind):
        return

#This AI players will always bet all of its chips at the flop.  
class AIplayer_AlwaysAllIn(Player):
    def assess(self, r):
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
        self.community_number = len(r.community_cards)
    
    def choice(self, opponents, wager_value):
        if wager_value >= self.chips or self.community_number == 0:
            self.playCall(wager_value)
            return wager_value
        
        self.playRaise(self.chips)
        return self.chips

    def review(self, winner, opp_folded, big_blind):
        return

#This AI player will always call. However, if it doesn't achieve at least a pair
#from the first three community cards, it will fold.
class AIplayer_FoldIfNoPair(Player):
    def assess(self, r):
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
        self.community_number = len(r.community_cards)
    
    def choice(self, opponents, wager_value):
        if self.hand_strength[0] == 0 and self.community_number > 0 and self.bet < wager_value:
            self.playFold()
            return wager_value
        
        self.playCall(wager_value)
        return wager_value

    def review(self, winner, opp_folded, big_blind):
        return

#This AI player will always call (or raise by 1) up to half of the chips it starts the round with.
#It will fold if it is forced to bet more than half of the chips it had at the 
#start of the round.    
class AIplayer_CallUpToHalf(Player):   
    def assess(self, r):
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
        self.community_number = len(r.community_cards)
        
        if self.community_number == 0:
            self.limit = self.chips / 2
    
    def choice(self, opponents, wager_value):
        if (self.chips - wager_value) < self.limit and self.bet < wager_value:
            self.playFold()
            return wager_value
        elif wager_value > self.chips:
            self.playCall(wager_value)
            return wager_value
        elif ((opponents[0].last_move is None or opponents[0].last_move == "raise" or self.last_move != "raise") 
            and wager_value < (self.chips - self.limit)) :
            self.playRaise(wager_value + 1)
            return wager_value + 1
        
        self.playCall(wager_value)
        return wager_value

    def review(self, winner, opp_folded, big_blind):
        return