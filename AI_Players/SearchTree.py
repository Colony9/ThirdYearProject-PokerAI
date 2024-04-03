from OpponentProfile import OpponentProfile

class TreeNode():
    def __init__(self, identity, action_route, odds, pot_value, bet_value, opp_bet_value, parent=None):
        self.identity = identity
        self.action_route = action_route
        self.value = None
        self.parent = parent
        self.children = []

        self.odds = odds
        self.regret_values = []
        for i in range(5):
            self.regret_values.append(0)
        self.pot_val = pot_value
        self.bet_val = bet_value
        self.opp_bet = opp_bet_value

    def expandChildren(self, maxChips, opp, big_blind):
        if self.identity == "terminal" or self.identity == "base":
            return
        elif self.identity == "player":
            if self.action_route == "all in":
                self.children.append(TreeNode("terminal", "call", 0.5, 
                                              self.pot_val, min(maxChips, opp.max_chips), self.opp_bet, parent=self))
                self.children.append(TreeNode("terminal", "fold", 0.5, 
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))
            elif self.action_route == "raise" or self.parent.action_route == None:
                self.children.append(TreeNode("opponent", "all in", 0.2, 
                                              self.pot_val, maxChips, self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "raise", 0.2, 
                                              self.pot_val, min(maxChips, self.bet_val + self.pot_val), self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "raise", 0.2, 
                                              self.pot_val, min(maxChips, self.bet_val + round(self.pot_val * 0.25)), self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "call", 0.2, 
                                              self.pot_val, max(min(maxChips, self.opp_bet), self.bet_val), self.opp_bet, parent=self))
                self.children.append(TreeNode("terminal", "fold", 0.2, 
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))

            elif self.action_route == "call":
                #The AI isn't permitted to re-raise and there is no benefit to 
                #folding over checking.
                self.children.append(TreeNode("terminal", "call", 1.0, 
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))
        elif self.identity == "opponent":
            if self.bet_val > opp.max_chips:
                wager = opp.max_chips
            else:
                wager = self.bet_val

            allIn_rate = (opp.allIn_coefficients[0] * (wager ** 2)) + (opp.allIn_coefficients[1] * wager) + opp.allIn_coefficients[2]
            raise_rate = (opp.raise_coefficients[0] * (wager ** 2)) + (opp.raise_coefficients[1] * wager) + opp.raise_coefficients[2]
            call_rate = (opp.call_coefficients[0] * (wager** 2)) + (opp.call_coefficients[1] * wager) + opp.call_coefficients[2]
            fold_rate = (opp.fold_coefficients[0] * (wager ** 2)) + (opp.fold_coefficients[1] * wager) + opp.fold_coefficients[2]

            if self.action_route == "all in":
                total_rate = call_rate + fold_rate
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
            elif self.action_route == "raise" or self.parent.action_route == None:
                total_rate = allIn_rate + raise_rate + call_rate + fold_rate

                self.children.append(TreeNode("player", "all in", allIn_rate / total_rate, 
                                              self.pot_val + (opp.max_chips - self.opp_bet), self.bet_val, opp.max_chips, parent=self))
                self.children.append(TreeNode("player", "raise", raise_rate / total_rate, 
                                              min(self.pot_val + (opp.max_chips - self.opp_bet), self.pot_val + opp.average_raise_value),
                                              self.bet_val, min(opp.max_chips, self.opp_bet + opp.average_raise_value), parent=self))
                self.children.append(TreeNode("player", "call", call_rate / total_rate, 
                                              max(min(self.pot_val + (self.bet_val - self.opp_bet), self.pot_val + (opp.max_chips - self.opp_bet)), self.pot_val),
                                              self.bet_val, max(min(opp.max_chips, self.bet_val), self.opp_bet), parent=self))
                self.children.append(TreeNode("terminal", "fold", fold_rate / total_rate,
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))

                
            elif self.action_route == "call":
                self.children.append(TreeNode("terminal", "call", 1.0, 
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))
        else:
            if big_blind:
                self.children.append(TreeNode("opponent", "all in", 0.2, 
                                              self.pot_val, maxChips, self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "raise", 0.2, 
                                              self.pot_val, min(maxChips, self.bet_val + self.pot_val), self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "raise", 0.2, 
                                              self.pot_val, min(maxChips, self.bet_val + round(self.pot_val * 0.25)), self.opp_bet, parent=self))
                self.children.append(TreeNode("opponent", "call", 0.2, 
                                              self.pot_val, min(maxChips, self.bet_val + opp.average_raise_value), self.opp_bet, parent=self))
                self.children.append(TreeNode("terminal", "fold", 0.2, 
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))
            else:
                allIn_rate = opp.allIn_coefficients[2]
                raise_rate = opp.raise_coefficients[2]
                call_rate = opp.call_coefficients[2]
                fold_rate = opp.fold_coefficients[2]

                total_rate = allIn_rate + raise_rate + call_rate + fold_rate

                self.children.append(TreeNode("player", "all in", allIn_rate / total_rate, 
                                              self.pot_val + (opp.max_chips - self.opp_bet), self.bet_val, opp.max_chips, parent=self))
                self.children.append(TreeNode("player", "raise", raise_rate / total_rate, 
                                              min(self.pot_val + (opp.max_chips - self.opp_bet), self.pot_val + opp.average_raise_value),
                                              self.bet_val, min(opp.max_chips, self.opp_bet + opp.average_raise_value), parent=self))
                self.children.append(TreeNode("player", "call", call_rate / total_rate, 
                                              max(min(self.pot_val + (self.bet_val - self.opp_bet), self.pot_val + (opp.max_chips - self.opp_bet)), self.pot_val),
                                              self.bet_val, max(min(opp.max_chips, self.bet_val), self.opp_bet), parent=self))
                self.children.append(TreeNode("terminal", "fold", fold_rate / total_rate,
                                              self.pot_val, self.bet_val, self.opp_bet, parent=self))

    def backPropagate(self):
        if self.identity == "player":
            self.calculateRegret()
        if self.identity == "opponent":
            self.value = 0
            for child in self.children:
                self.value += child.odds * child.value
        return


    def calculateRegret(self):
        if self.identity != "player":
            return

        regret_sum = 0
        for child in self.children:
            regret_sum += child.odds * child.value

        self.value = regret_sum
        for c in range(len(self.children)):
            self.regret_values[c] += max(0, self.children[c].value - self.value)
        return

    def readjustOdds(self, opp):
        if self.identity == "player":
            normalisation_factor = 0
            for regret in self.regret_values:
                normalisation_factor += regret
                
            if normalisation_factor == 0:
                return
            
            for c in range(len(self.children)):
                self.children[c].odds = self.regret_values[c] / normalisation_factor

        elif self.identity == "opponent":
            pass


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
        print(depth_limit)
        print(child.identity + " " + child.action_route + " " + str(child.odds)+ " " + str(child.pot_val) + " " + str(child.bet_val))
        node_count = completeSubTree(child, depth_limit - 1, maxChips, opp, big_blind, node_count)
    return node_count

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
                root_node.children[1].bet_val = min(maxChips, root_node.bet_val + root_node.pot_val)
                root_node.children[2].bet_val = min(maxChips, root_node.bet_val + round(root_node.pot_val * 0.25))
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
            root_node.children[1].pot_val = min(root_node.pot_val + (opp.max_chips - root_node.opp_bet), root_node.pot_val + opp.average_raise_value)
            root_node.children[1].opp_bet = min(opp.max_chips, root_node.opp_bet + opp.average_raise_value)
            root_node.children[2].pot_val = max(min(root_node.pot_val + (root_node.bet_val - root_node.opp_bet), root_node.pot_val + (opp.max_chips - root_node.opp_bet)), root_node.pot_val)
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
            root_node.children[1].bet_val = min(maxChips, root_node.bet_val + root_node.pot_val)
            root_node.children[2].bet_val = min(maxChips, root_node.bet_val + round(root_node.pot_val * 0.25))
            root_node.children[3].bet_val = max(min(maxChips, root_node.opp_bet), root_node.bet_val)
            root_node.children[4].bet_val = root_node.bet_val           
        else:
            for child in root_node.children:
                child.bet_val = root_node.bet_val
            root_node.children[0].pot_val = root_node.pot_val + (opp.max_chips - root_node.opp_bet)
            root_node.children[0].opp_bet = opp.max_chips
            root_node.children[1].pot_val = min(root_node.pot_val + (opp.max_chips - root_node.opp_bet), root_node.pot_val + opp.average_raise_value)
            root_node.children[1].opp_bet = min(opp.max_chips, root_node.opp_bet + opp.average_raise_value)
            root_node.children[2].pot_val = max(min(root_node.pot_val + (root_node.bet_val - root_node.opp_bet), root_node.pot_val + (opp.max_chips - root_node.opp_bet)), root_node.pot_val)
            root_node.children[2].opp_bet = max(min(opp.max_chips, root_node.bet_val), root_node.opp_bet)
            root_node.children[3].pot_val = root_node.pot_val
            root_node.children[3].opp_bet = root_node.opp_bet

    root_node.readjustOdds(opp)
    print(root_node.identity + " " + str(root_node.action_route) + " " + str(root_node.odds)+ " " + str(root_node.pot_val) + " " + str(root_node.bet_val))
    for child in root_node.children:
        updateSubTreeOdds(child, maxChips, opp, big_blind)
    return

if __name__ == "__main__":
    base_node = TreeNode("(1 1 1)", None, 1.0, 50, 25, 50)
    opp = OpponentProfile(100)
    node_count = completeSubTree(base_node, 3, 100, opp, False, 1)
    base_node.pot_val = 60
    updateSubTreeOdds(base_node, 100, opp, False)
    print(node_count)