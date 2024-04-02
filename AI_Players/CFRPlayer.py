import random
import sys
sys.path.append('..')
from Game import Player, Round
from Deck import *
from HandEvaluation import evaluateAllHands, evaluatePocket
from SearchTree import *
from OpponentProfile import OpponentProfile

class AIPlayer_CFR(Player):
    def __init__(self, name, chips):
        super().__init__(name, chips)
        self.base_node = TreeNode("base", None, 1.0, 0, 0, 0)
        self.opponent_profile = OpponentProfile(10000)
    
    def assess(self, r):
        if len(r.community_cards) == 0:
            pocket_strength = evaluatePocket(self.pocket)
            if pocket_strength == "0":
                self.hand_strength = [0, 0, 0]
                return
            else:
                for hand in self.base_node.children:
                    if pocket_strength == hand.identity:
                        updateSubTreeOdds(hand, self.opponent_profile)
                        self.round_base_node = hand
                        return
                    
                new_pocket_node = TreeNode(pocket_strength, None, 1.0, 0, 0, 0, parent=self.base_node)
                self.base_node.children.append(new_pocket_node)
                self.round_base_node = completeSubTree(new_pocket_node, 7, self.chips, self.opponent_profile, 1)
                return
            
        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
        hand_name = "(" + str(self.hand_strength[0]) + " "
        if self.hand_strength[1] < 7:
            hand_name += "1 "
        elif self.hand_strength[1] < 11:
            hand_name += "2 "
        else:
            hand_name += "3 "
        
        hand_name += str(len(r.community_cards)) + ")"
        
        for hand in self.base_node.children:
            if hand_name == hand.identity:
                updateSubTreeOdds(hand, self.opponent_profile)
                self.round_base_node = hand
                return
        
        new_hand_node = TreeNode(hand_name, None, 1.0, 0, 0, 0)
        self.base_node.children.append(new_hand_node)
        self.round_base_node = completeSubTree(new_hand_node, 7, self.chips, self.opponent_profile, 1)
        return
    
    def choice(self, opponents, wager_value):
        pass
    
    def review(self):
        pass
    
if __name__ == "__main__":
    test_CFR = AIPlayer_CFR("Test", 10000)
    round_manager = Round([test_CFR], full_deck)
    for i in range(3):
        test_CFR.pocket = []
        round_manager.dealPlayer(test_CFR, 3)
        test_CFR.assess(round_manager)
    
    for hand in test_CFR.base_node.children:
        print(hand.identity)
        print(hand.children)