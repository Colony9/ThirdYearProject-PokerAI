
class TreeNode():
    def __init__(self, identity, action_route, odds, pot_value, parent=None):
        self.identity = identity
        self.action_route = action_route
        self.value = None
        self.parent = parent
        self.children = []

        self.odds = None
        self.regret_values = [0, 0, 0, 0, 0]
        self.pot_val = pot_value

    def expandChildren(self):
        pass

    def backPropagate(self):
        if self.identity == "player":
            self.calculateRegret()
        if self.identity == "opponent":
            self.value
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

    def readjustOdds(self):
        if self.identity == "player":
            normalisation_factor = 0
            for regret in self.regret_values:
                normalisation_factor += regret
            
            for c in range(len(self.children)):
                self.children[c].odds = self.regret_values[c] / normalisation_factor

        elif self.identity == "opponent":
            pass

def completeSubTree(root_node, depth_limit):
    pass