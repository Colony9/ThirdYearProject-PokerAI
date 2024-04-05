import unittest
import sys
sys.path.append('../AI_Players')
import SearchTree, OpponentProfile

class testSearchTree(unittest.TestCase):
    def setUp(self):
        self.base_node = SearchTree.TreeNode("(0, 0)", None, 1.0, 0, 0, 0)
        self.mini_base_node = SearchTree.TreeNode("(0, 0)", None, 1.0, 0, 0, 0)
        self.opp = OpponentProfile.OpponentProfile(1000)
        self.node_count = SearchTree.completeSubTree(self.base_node, 7, 100, self.opp, False, 1)
   
    #This test checks if the search tree is constructed in the correct shape by
    #checking whether the number of nodes within the tree is correct.
    def testNumberOfNodes(self):
        self.assertEqual(len(self.base_node.children), 4)        
        self.assertEqual(self.node_count, 363)
        second_node_count = SearchTree.completeSubTree(self.mini_base_node, 3, 100, self.opp, False, 1)
        self.assertEqual(second_node_count, 63)
    
    #This test checks if a given player node (with no restrictions on what betting
    #moves are permitted), produces the correct the correct number of child nodes
    #to represent its possible actions.
    def testPlayerNodeExpansion(self):
        node = self.base_node.children[1]
        self.assertEqual(len(node.children), 5)
        self.assertEqual(node.children[0].action_route, "all in")
        self.assertEqual(node.children[1].action_route, "raise")
        self.assertEqual(node.children[2].action_route, "raise")
        self.assertEqual(node.children[3].action_route, "call")
        self.assertEqual(node.children[4].action_route, "fold")
    
    #This test checks that, if the opponent goes all in, the only player choices
    #in the tree are to call or fold.
    def testAllInRoute(self):
        self.assertEqual(len(self.base_node.children[0].children), 2)
        self.assertEqual(self.base_node.children[0].children[0].action_route, "call")
        self.assertEqual(self.base_node.children[0].children[1].action_route, "fold")
        self.assertEqual(self.base_node.children[0].children[0].identity, "terminal")
        self.assertEqual(self.base_node.children[0].children[1].identity, "terminal")
    
    #This test checks that the tree keeps expanding to the depth limit if players
    #keep raising, before forcing the AI to either call or fold.
    def testRaiseRoute(self):
        node = self.base_node
        for i in range(7):
            node = node.children[1]
            self.assertEqual(node.action_route, "raise")
            
        self.assertEqual(node.children[0].action_route, "call")
        self.assertEqual(node.children[1].action_route, "fold")
    
    #This test checks that, if the opponent calls, the only option for the AI is 
    #to check. An exception is if the opponent's first move is to check (when 
    #they are the big blind) as the AI should have a free range of actions then.
    def testCallRoute(self):
        self.assertEqual(len(self.base_node.children[2].children), 5)
        self.assertEqual(len(self.base_node.children[2].children[3].children), 1)
        node = self.base_node.children[2].children[3].children[0]
        self.assertEqual(node.action_route, "call")
        self.assertEqual(node.identity, "terminal")
    
    #This test checks that a fold action results in a terminal node.
    def testFoldRoute(self):
        self.assertEqual(self.base_node.children[3].action_route, "fold")
        self.assertEqual(self.base_node.children[3].identity, "terminal")
     
    #This test checks that the 'updateSubTreeOdds' function correctly modifies
    #the odds for both player and opponent nodes' children.
    def testOddsAdjustment(self):
        for i in range(len(self.opp.allIn_rates)):
            self.opp.allIn_rates[i] = 1.0
            self.opp.raise_rates[i] = 0.0
            self.opp.call_rates[i] = 0.0
            self.opp.fold_rates[i] = 0.0
        self.opp.getAllInRate()
        self.opp.getRaiseRate()
        self.opp.getCallRate()
        self.opp.getFoldRate()
        
        SearchTree.completeSubTree(self.mini_base_node, 3, 100, self.opp, False, 1)
        self.mini_base_node.children[1].regret_values = [20, 10, 10, 0, 0]
        SearchTree.updateSubTreeOdds(self.mini_base_node, 100, self.opp, False)
        
        self.assertEqual(self.mini_base_node.children[0].odds, 1.0)
        self.assertEqual(self.mini_base_node.children[1].odds, 0.0)
        self.assertEqual(self.mini_base_node.children[2].odds, 0.0)
        self.assertEqual(self.mini_base_node.children[3].odds, 0.0)
        
        player_node = self.mini_base_node.children[1]
        self.assertEqual(player_node.children[0].odds, 0.5)
        self.assertEqual(player_node.children[1].odds, 0.25)
        self.assertEqual(player_node.children[2].odds, 0.25)
        self.assertEqual(player_node.children[3].odds, 0.0)
        self.assertEqual(player_node.children[4].odds, 0.0)

    #This test checks that the 'updateSubTreeOdds' function correctly recalculates
    #the possible winnings for the AI at each given node, provided an initial
    #starting pot value.
    def testPotPropagation(self):
        SearchTree.completeSubTree(self.mini_base_node, 3, 2000, self.opp, False, 1)
        self.mini_base_node.pot_val = 500
        SearchTree.updateSubTreeOdds(self.mini_base_node, 2000, self.opp, False)
        self.assertEqual(self.mini_base_node.children[0].children[0].pot_val, 1500)
        self.assertEqual(self.mini_base_node.children[1].children[1].children[1].children[0].pot_val, 1300)
        self.assertEqual(self.mini_base_node.children[1].children[2].children[1].children[0].pot_val, 850)

    #This test checks that the values for each node are correctly calculated
    #recursively from their child nodes, weighted by the child node odds.
    #The value of a node should represent the average winnings from reaching node,
    #using the current strategy weightings.
    def testCalculateRoundResults(self):
        SearchTree.completeSubTree(self.mini_base_node, 3, 2000, self.opp, False, 1)
        SearchTree.calculateRoundResults(self.mini_base_node, 1, False)
        self.assertEqual(self.mini_base_node.children[0].value, 500)
        self.assertEqual(self.mini_base_node.children[3].value, 0)
        self.assertEqual(self.mini_base_node.value, 214.53125)
        SearchTree.clearTreeValues(self.mini_base_node)
        SearchTree.calculateRoundResults(self.mini_base_node, 0, False)
        self.assertEqual(self.mini_base_node.children[0].value, -500)
        self.assertEqual(self.mini_base_node.children[3].value, 0)
        self.assertEqual(self.mini_base_node.value, -262.65625)

    #This method is used to recursively search through the tree and determine
    #that each node's value has been set to None.
    def recursiveSearch(self, start_node):
        self.assertEqual(start_node.value, None)
        for child in start_node.children:
            self.recursiveSearch(child)

    #This test checks, using the method 'recursiveSearch', that the 'clearTreeValues'
    #function correctly sets every node's value to None.
    def testClearTreeValues(self):
        SearchTree.calculateRoundResults(self.base_node, 1, False)
        SearchTree.clearTreeValues(self.base_node)
        self.recursiveSearch(self.base_node)


if __name__ == '__main__':
    unittest.main()