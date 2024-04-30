from OpponentProfile import OpponentProfile

#This class represents a single node within a search tree.
class TreeNode():
    def __init__(self, identity, action_route, odds, pot_value, bet_value, opp_bet_value, parent=None):
        #The identity attribute represents the type of node this is ('Player',
        #'Opponent' or 'Terminal')
        self.identity = identity
        #The action route attribute represents the type of decision ('raise',
        #'call', or 'fold') that is used to reach this node
        self.action_route = action_route
        self.value = None
        #The parent and children attributes denotes which nodes are directly connected to
        #this node by an edge.
        self.parent = parent
        self.children = []

        
        self.odds = odds
        self.regret_values = []
        for i in range(5):
            self.regret_values.append(0)
        #These attributes are used to estimate the winnings/losses at the end
        #of a game.
        self.pot_val = pot_value
        self.bet_val = bet_value
        self.opp_bet = opp_bet_value

    def expandChildren(self, maxChips, opp, big_blind):
        #A terminal node doesn't have any children.
        if self.identity == "terminal":
            return
        elif self.identity == "player":
            #If the opponent went all in, the AI can only choose to call or
            #fold.
            if self.action_route == "all in":
                self.children.append(TreeNode("terminal", "call", 0.5, 
                                              self.pot_val, min(maxChips, opp.max_chips), self.opp_bet, parent=self))
                self.children.append(TreeNode("terminal", "fold", 0.5, 
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))
            #If the opponent raised, or called on the first turn, the range of
            #actions available to the player is unrestricted.
            elif self.action_route == "raise" or self.parent.action_route == None:
                self.children.append(TreeNode("opponent", "all in", 0.2, 
                                              self.pot_val, maxChips, self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "raise", 0.2, 
                                              self.pot_val, min(maxChips, max(self.bet_val, self.opp_bet) + self.pot_val), self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "raise", 0.2, 
                                              self.pot_val, min(maxChips, max(self.bet_val, self.opp_bet) + round(self.pot_val * 0.25)), self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "call", 0.2, 
                                              self.pot_val, max(min(maxChips, self.opp_bet), self.bet_val), self.opp_bet, parent=self))
                self.children.append(TreeNode("terminal", "fold", 0.2, 
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))

            #The AI isn't permitted to re-raise and there is no benefit to 
            #folding over checking so it should always choose to check.
            elif self.action_route == "call":
                self.children.append(TreeNode("terminal", "call", 1.0, 
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))
        elif self.identity == "opponent":
            #The method obtains probabilities for each action at the current 
            #betting value from the 'Opponent Profile' object.
            allIn_rate = opp.getAllInRate(self.bet_val)
            raise_rate = opp.getRaiseRate(self.bet_val)
            call_rate = opp.getCallRate(self.bet_val)
            fold_rate = opp.getFoldRate(self.bet_val)

            if self.action_route == "all in":
                #The probabilities are calculated as a proportion of the total odds
                #for the available legal actions.
                total_rate = call_rate + fold_rate
                #If the AI has never called or folded so far, they are set to
                #equally likely to avoid a division by 0.
                if total_rate == 0:
                    call_odds = 0.5
                    fold_odds = 0.5
                else:
                    call_odds = call_rate / total_rate
                    fold_odds = fold_rate / total_rate
                            
                self.children.append(TreeNode("terminal", "call", call_odds, 
                                              min(self.pot_val + (self.bet_val - self.opp_bet), self.pot_val + (opp.max_chips - self.opp_bet)),
                                              self.bet_val, min(opp.max_chips, self.bet_val), parent=self))
                self.children.append(TreeNode("terminal", "fold", fold_odds,
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))
            #If the AI raised, or called on the first turn, the range of
            #actions available to the opponent is unrestricted from its 
            #four abstracted choices.
            elif self.action_route == "raise" or self.parent.action_route == None:
                self.children.append(TreeNode("player", "all in", allIn_rate,
                                              self.pot_val + (opp.max_chips - self.opp_bet), self.bet_val, opp.max_chips, parent=self))
                self.children.append(TreeNode("player", "raise", raise_rate, 
                                              min(self.pot_val + (opp.max_chips - self.opp_bet), self.pot_val + max((self.bet_val - self.opp_bet), 0) + opp.average_raise_value),
                                              self.bet_val, min(opp.max_chips, max(self.bet_val, self.opp_bet) + opp.average_raise_value), parent=self))
                self.children.append(TreeNode("player", "call", call_rate, 
                                              max(self.pot_val + (min(self.bet_val, opp.max_chips) - self.opp_bet), self.pot_val),
                                              self.bet_val, max(min(opp.max_chips, self.bet_val), self.opp_bet), parent=self))
                self.children.append(TreeNode("terminal", "fold", fold_rate,
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))
                
            #As there is no benefit to folding in this situation, the opponent
            #will check.
            elif self.action_route == "call":
                self.children.append(TreeNode("terminal", "call", 1.0, 
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))
        else:
            #If the AI is the big blind, the root node functions as a 'Player'
            #node with no restrictions.
            if big_blind:
                self.children.append(TreeNode("opponent", "all in", 0.2, 
                                              self.pot_val, maxChips, self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "raise", 0.2, 
                                              self.pot_val, min(maxChips, max(self.bet_val, self.opp_bet) + self.pot_val), self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "raise", 0.2, 
                                              self.pot_val, min(maxChips, max(self.bet_val, self.opp_bet) + round(self.pot_val * 0.25)), self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "call", 0.2, 
                                              self.pot_val, max(min(maxChips, self.opp_bet), self.bet_val), self.opp_bet, parent=self))
                self.children.append(TreeNode("terminal", "fold", 0.2, 
                                             self.pot_val, self.bet_val, self.opp_bet, parent=self))

            #Otherwise, it functions as an 'Opponent' node with no restrictions.
            else:
                allIn_rate = opp.getAllInRate(0)
                raise_rate = opp.getRaiseRate(0)
                call_rate = opp.getCallRate(0)
                fold_rate = opp.getFoldRate(0)
                self.children.append(TreeNode("player", "all in", allIn_rate, 
                                              self.pot_val + (opp.max_chips - self.opp_bet), self.bet_val, opp.max_chips, parent=self))
                self.children.append(TreeNode("player", "raise", raise_rate, 
                                              min(self.pot_val + (opp.max_chips - self.opp_bet), self.pot_val + max((self.bet_val - self.opp_bet), 0) + opp.average_raise_value),
                                              self.bet_val, min(opp.max_chips, max(self.bet_val, self.opp_bet) + opp.average_raise_value), parent=self))
                self.children.append(TreeNode("player", "call", call_rate, 
                                              max(self.pot_val + (min(self.bet_val, opp.max_chips) - self.opp_bet), self.pot_val),
                                              self.bet_val, max(min(opp.max_chips, self.bet_val), self.opp_bet), parent=self))
                self.children.append(TreeNode("terminal", "fold", fold_rate,
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))

    #The value of the parent node is equal to the sum of its child nodes' values 
    #multiplied by their odds
    def backPropagate(self):
        self.value = 0
        for child in self.children:
            self.value += child.odds * child.value
        return

    def readjustOdds(self, opp, big_blind):
        #The od
        if self.identity == "player":
            normalisation_factor = 0
            for regret in self.regret_values:
                normalisation_factor += regret
                
            if normalisation_factor == 0:
                return
            
            for c in range(len(self.children)):
                self.children[c].odds = self.regret_values[c] / normalisation_factor

        #The odds for the children of an opponent are assigned using the appropriate
        #value from the 'Opponent Profile' object, similar to how it is done during
        #construction.
        elif self.identity == "opponent":
            allIn_rate = opp.getAllInRate(self.bet_val)
            raise_rate = opp.getRaiseRate(self.bet_val)
            call_rate = opp.getCallRate(self.bet_val)
            fold_rate = opp.getFoldRate(self.bet_val)
           
            if self.action_route == "all in":
                total_rate = call_rate + fold_rate
                if total_rate == 0:
                    call_odds = 0.5
                    fold_odds = 0.5
                else:
                    call_odds = call_rate / total_rate
                    fold_odds = fold_rate / total_rate

                self.children[0].odds = call_odds
                self.children[1].odds = fold_odds
            elif self.action_route == "raise" or self.parent.action_route == None:
               self.children[0].odds = allIn_rate
               self.children[1].odds = raise_rate
               self.children[2].odds = call_rate
               self.children[3].odds = fold_rate

        elif self.identity != "terminal":
            allIn_rate = opp.getAllInRate(0)
            raise_rate = opp.getRaiseRate(0)
            call_rate = opp.getCallRate(0)
            fold_rate = opp.getFoldRate(0)
            
            self.children[0].odds = allIn_rate
            self.children[1].odds = raise_rate
            self.children[2].odds = call_rate
            self.children[3].odds = fold_rate
            

#This function recursively expands a search tree until it reaches the depth limit.
#Any 'Player' nodes at the bottom of the tree get expanded with only the choices
#to call or fold as that will end the betting round.
def completeSubTree(root_node, depth_limit, maxChips, opp, big_blind, node_count):
    if depth_limit == 0:
        if root_node.identity == "player":
            if root_node.action_route == "all in":
                root_node.children.append(TreeNode("terminal", "call", 0.5, 
                                                   root_node.pot_val, min(maxChips, opp.max_chips),
                                                   root_node.opp_bet, parent=root_node))
                root_node.children.append(TreeNode("terminal", "fold", 0.5, 
                                                   root_node.pot_val, root_node.bet_val, root_node.opp_bet, parent=root_node))
            elif root_node.action_route == "raise":
                root_node.children.append(TreeNode("terminal", "call", 0.5, 
                                                   root_node.pot_val, min(maxChips, root_node.bet_val + opp.average_raise_value), 
                                                   root_node.opp_bet, parent=root_node))
                root_node.children.append(TreeNode("terminal", "fold", 0.5, 
                                                   root_node.pot_val, root_node.bet_val, root_node.opp_bet, parent=root_node))
            else:
                root_node.children.append(TreeNode("terminal", "call", 1.0, 
                                              root_node.pot_val, root_node.bet_val, root_node.opp_bet, parent=root_node))
                

            node_count += 2
        return node_count

    root_node.expandChildren(maxChips, opp, big_blind)
    for child in root_node.children:
        node_count += 1
        node_count = completeSubTree(child, depth_limit - 1, maxChips, opp, big_blind, node_count)
    return node_count

#This function recursively navigates through the tree, updating its odds based 
#on either its 'regret values' or the 'Opponent Profile' object. It also
#updates the pot value and bet value based on the 'Opponent Profile's new 
#average raise value.
def updateSubTreeOdds(root_node, maxChips, opp, big_blind):
    if root_node.identity == "player":
        for child in root_node.children:
            child.pot_val = root_node.pot_val
            child.opp_bet = root_node.opp_bet

        if root_node.action_route == "all in":
            root_node.children[0].bet_val = min(maxChips, opp.max_chips) 
            root_node.children[1].bet_val = root_node.bet_val
        elif root_node.action_route == "raise" or root_node.parent.action_route == None:
            if len(root_node.children) == 2:
                root_node.children[0].bet_val = max(min(maxChips, root_node.opp_bet), root_node.bet_val)
                root_node.children[1].bet_val = root_node.bet_val
            else:
                root_node.children[0].bet_val = maxChips
                root_node.children[1].bet_val = min(maxChips, max(root_node.bet_val, root_node.opp_bet) + root_node.pot_val)
                root_node.children[2].bet_val = min(maxChips, max(root_node.bet_val, root_node.opp_bet) + round(root_node.pot_val * 0.25))
                root_node.children[3].bet_val = max(min(maxChips, root_node.opp_bet), root_node.bet_val)
                root_node.children[4].bet_val = root_node.bet_val
        elif root_node.action_route == "call":
            root_node.children[0].bet_val = root_node.bet_val
    elif root_node.identity == "opponent":
        for child in root_node.children:
            child.bet_val = root_node.bet_val

        if root_node.action_route == "all in":
            root_node.children[0].pot_val = min(root_node.pot_val + (root_node.bet_val - root_node.opp_bet), root_node.pot_val + (opp.max_chips - root_node.opp_bet))
            root_node.children[0].opp_bet = min(opp.max_chips, root_node.bet_val)
            root_node.children[1].pot_val = root_node.pot_val
            root_node.children[1].opp_bet = root_node.opp_bet
        elif root_node.action_route == "raise" or root_node.parent.action_route == None:
            root_node.children[0].pot_val = root_node.pot_val + (opp.max_chips - root_node.opp_bet)
            root_node.children[0].opp_bet = opp.max_chips
            root_node.children[1].pot_val = min(root_node.pot_val + (opp.max_chips - root_node.opp_bet), root_node.pot_val + max((root_node.bet_val - root_node.opp_bet), 0) + opp.average_raise_value)
            root_node.children[1].opp_bet = min(opp.max_chips, max(root_node.bet_val, root_node.opp_bet) + opp.average_raise_value)
            root_node.children[2].pot_val = max(root_node.pot_val + (min(root_node.bet_val, opp.max_chips) - root_node.opp_bet), root_node.pot_val)
            root_node.children[2].opp_bet = max(min(opp.max_chips, root_node.bet_val), root_node.opp_bet)
            root_node.children[3].pot_val = root_node.pot_val
            root_node.children[3].opp_bet = root_node.opp_bet
        elif root_node.action_route == "call":
            root_node.children[0].pot_val = root_node.pot_val
            root_node.children[0].opp_bet = root_node.opp_bet
    elif root_node.identity != "terminal":
        if big_blind:
            for child in root_node.children:
                child.pot_val = root_node.pot_val
                child.opp_bet = root_node.opp_bet
            root_node.children[0].bet_val = maxChips
            root_node.children[1].bet_val = min(maxChips, max(root_node.bet_val, root_node.opp_bet) + root_node.pot_val)
            root_node.children[2].bet_val = min(maxChips, max(root_node.bet_val, root_node.opp_bet) + round(root_node.pot_val * 0.25))
            root_node.children[3].bet_val = max(min(maxChips, root_node.opp_bet), root_node.bet_val)
            root_node.children[4].bet_val = root_node.bet_val           
        else:
            for child in root_node.children:
                child.bet_val = root_node.bet_val
            root_node.children[0].pot_val = root_node.pot_val + (opp.max_chips - root_node.opp_bet)
            root_node.children[0].opp_bet = opp.max_chips
            root_node.children[1].pot_val = min(root_node.pot_val + (opp.max_chips - root_node.opp_bet), root_node.pot_val + max((root_node.bet_val - root_node.opp_bet), 0) + opp.average_raise_value)
            root_node.children[1].opp_bet = min(opp.max_chips, max(root_node.bet_val, root_node.opp_bet) + opp.average_raise_value)
            root_node.children[2].pot_val = max(root_node.pot_val + (min(root_node.bet_val, opp.max_chips) - root_node.opp_bet), root_node.pot_val)
            root_node.children[2].opp_bet = max(min(opp.max_chips, root_node.bet_val), root_node.opp_bet)
            root_node.children[3].pot_val = root_node.pot_val
            root_node.children[3].opp_bet = root_node.opp_bet

    root_node.readjustOdds(opp, big_blind)
    for child in root_node.children:
        updateSubTreeOdds(child, maxChips, opp, big_blind)
    return

#At the end of a round, this function assigns a value to each terminal node 
#(representing how the AI would win/lose if it reached that node) before backpropagating
#it to calculate the average expected winnings at each node.
def calculateRoundResults(root_node, won, big_blind):
    for child in root_node.children:
        calculateRoundResults(child, won, big_blind)

    if root_node.identity == "terminal":
        if root_node.action_route == "fold":
            if root_node.parent.identity == "player":
                root_node.value = -1 * root_node.bet_val
            elif root_node.parent.identity == "opponent":
                root_node.value = root_node.pot_val
            else:
                if big_blind:
                    root_node.value = -1 * root_node.bet_val
                else:
                    root_node.value = root_node.pot_val
        elif won == 1:
            root_node.value = root_node.pot_val
        elif won == 0:
            root_node.value = -1 * root_node.bet_val
        else:
            root_node.value = ((root_node.pot_val + root_node.bet_val) // 2)  - root_node.bet_val
    else:
        root_node.backPropagate()
    return