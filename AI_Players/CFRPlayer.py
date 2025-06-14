import random
import sys
sys.path.append('..')
from Game import Player, Round
from Deck import *
from HandEvaluation import evaluateAllHands, evaluatePocket
from SearchTree import *
from OpponentProfile import OpponentProfile
import time

class AIPlayer_CFR(Player):
    def __init__(self, name, chips, big_blind):
        super().__init__(name, chips)
        self.big_blind = big_blind
        self.hand_trees = []
        self.opponent_profiles_list = [OpponentProfile(10000), OpponentProfile(10000), OpponentProfile(10000), OpponentProfile(10000)]
        self.opponent_profile = self.opponent_profiles_list[0]
        self.round_base_nodes = []
        self.current_node = None
        self.visited_player_nodes = []
        self.base_pot = 0
        self.last_wager = [0, 1, 0, False]

    def assess(self, r):
        #The AI determines the appropriate 'Opponent Profile' object for 
        self.opponent_profile = self.opponent_profiles_list[max(0, len(r.community_cards) - 2)]
        self.base_pot = r.pot
        if self.base_pot == 75:
            self.opponent_profile.max_chips = self.opponent_profiles_list[0].max_chips - 50
        else:
            self.opponent_profile.max_chips = self.opponent_profiles_list[0].max_chips - self.base_pot // 2
        
        #If the game is in the 'Pre-flop' stage, a hand can not be evaluated so
        #a different evaluation method is used.
        if len(r.community_cards) == 0:
            #The strongest set of two cards from the pocket is obtained
            pocket_strength = evaluatePocket(self.pocket)
            for hand in self.hand_trees:
                #If a search tree exists, it is update with previously-learned
                #information.
                if pocket_strength == hand.identity:
                    if self.big_blind:
                        hand.pot_val = self.base_pot + 25
                    else:
                        hand.pot_val = self.base_pot + 50
                    updateSubTreeOdds(hand, self.chips, self.opponent_profile, self.big_blind)
                    self.round_base_nodes.append(hand)
                    self.current_node = hand
                    return

            #If a search tree doesn not currently exist for the set, one is constructed.
            if self.big_blind:
                new_pocket_node = TreeNode(pocket_strength, None, 1.0, 25 + self.base_pot, 50, 25)
                completeSubTree(new_pocket_node, 10, self.chips, self.opponent_profile, True, 1)
            else:
                new_pocket_node = TreeNode(pocket_strength, None, 1.0, 50 + self.base_pot, 25, 50)
                completeSubTree(new_pocket_node, 11, self.chips, self.opponent_profile, False, 1)
            self.hand_trees.append(new_pocket_node)
            self.round_base_nodes.append(new_pocket_node)
            self.current_node = new_pocket_node               
            return

        #A similar behaviour to assessing the preflop is exhibited in later betting,
        #round, only it uses actual formed hands rather than sets of two cards.

        self.hand_strength, _ = evaluateAllHands(self.pocket, r.community_cards)
        hand_name = "(" + str(self.hand_strength[0]) + " "
        if self.hand_strength[1] < 7:
            hand_name += "1 "
        elif self.hand_strength[1] < 11:
            hand_name += "2 "
        else:
            hand_name += "3 "

        hand_name += str(len(r.community_cards)) + ")"

        for hand in self.hand_trees:
            if hand_name == hand.identity:
                hand.pot_val = self.base_pot
                updateSubTreeOdds(hand, self.chips, self.opponent_profile, self.big_blind)
                self.round_base_nodes.append(hand)
                self.current_node = hand
                return

        new_hand_node = TreeNode(hand_name, None, 1.0, self.base_pot, 0, 0)
        if self.big_blind:
            completeSubTree(new_hand_node, 10, self.chips, self.opponent_profile, True, 1)
        else:
            completeSubTree(new_hand_node, 11, self.chips, self.opponent_profile, False, 1)
        self.hand_trees.append(new_hand_node)
        self.round_base_nodes.append(new_hand_node)
        self.current_node = new_hand_node
        return

    def choice(self, opponents, wager_value):
        #The Ai navigates from an 'Opponent' node to a 'Player' node based on
        #the action its opponent just took.
        #It also updates
        if opponents[0].last_move == "raise":
            if wager_value == opponents[0].chips:
                self.opponent_profile.updateAllIn(self.bet, opponents[0].chips)
                self.current_node = self.current_node.children[0]
            else:
                self.opponent_profile.updateRaise(wager_value - self.bet, self.bet, opponents[0].chips)
                self.current_node = self.current_node.children[1]
        if opponents[0].last_move == "call":
            self.opponent_profile.updateCall(self.bet, opponents[0].chips)
            if len(self.current_node.children) != 4:
                self.current_node = self.current_node.children[0]
            else:
                self.current_node = self.current_node.children[2]

        self.visited_player_nodes.append(self.current_node)
        decision_val = random.random()
        raise_high = False
        #The AI then randomly selects a move from its available, legal moves.
        #The odds for a given child node are the odds that the AI will pick that
        #action.
        for child in self.current_node.children:
            if decision_val <= child.odds:
                if child.action_route == "raise":
                    if child.bet_val == self.current_node.children[1].bet_val:
                        raise_high = True
                self.current_node = child
                decision_type = child.action_route
                break
            else:
                decision_val -= child.odds

        if decision_type == "all in":
            wager_value = self.chips
            self.playRaise(self.chips)
        elif decision_type == "raise":
            if raise_high:
                wager_value = min(self.chips, self.base_pot + opponents[0].bet + wager_value)
            else:
                wager_value = min(self.chips, round((self.base_pot + opponents[0].bet) * 0.25) + wager_value)
            self.playRaise(wager_value)
        elif decision_type == "call":
            self.playCall(wager_value)
        else:
            self.playFold()

        self.last_wager = [wager_value, opponents[0].chips, self.opponent_profiles_list.index(self.opponent_profile), self.current_node.identity == "opponent"]

        return wager_value

    def review(self, winner, opp_folded, big_blind):
        if opp_folded:
            self.opponent_profiles_list[self.last_wager[2]].updateFold(self.last_wager[0], self.last_wager[1])
        elif self.last_wager[3]:
            self.opponent_profiles_list[self.last_wager[2]].updateCall(self.last_wager[0], self.last_wager[1])

        win_1 = 0
        if winner[0] is None:
            win_1 = 0.5
        elif winner[0].name == self.name:
            win_1 = 1

        win_2 = 0
        if winner[1] is None:
            win_2 = 0.5
        elif winner[1].name == self.name:
            win_2 = 1

        #if winner[1] != None:
            #if winner[1].name == self.name:
                #self.opponent_profiles_list[0].max_chips -= winner[2]
            #else:
                #self.opponent_profiles_list[0].max_chips += winner[2]

        #At the end of a game, the AI calculates the average expected winnings at each
        #node within the active search trees.
        for c in range(len(self.round_base_nodes)):
            if self.last_wager[2] > c:
                calculateRoundResults(self.round_base_nodes[c], win_2, big_blind)
            else:
                calculateRoundResults(self.round_base_nodes[c], win_1, big_blind)
        #Regrets are only calculated at visited 'Player' nodes as those are
        #the only points where the AI could have made a different decision.
        for node in self.visited_player_nodes:
            if node.identity != "player":
                continue

            #To calculate the added regrets, the AI works out the difference between
            #the value for each child node and the parent node. If the parent node's
            #value is less than the child's value, the difference is added to the parent
            #node's corresponding regret value - use recalclate its odds.
            for c in range(len(node.children)):
                node.regret_values[c] += max(0, node.children[c].value - node.value)
        #The AI then resets its variables for the next game.
        self.last_wager = [0, 1, 0, False]
        self.visited_player_nodes.clear()
        self.round_base_nodes.clear()
        self.base_pot = 0