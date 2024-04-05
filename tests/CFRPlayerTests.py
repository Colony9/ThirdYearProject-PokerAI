import unittest
import sys
sys.path.append('../AI_Players')
import CFRPlayer, SearchTree, OpponentProfile

class testCFRPlayer(unittest.TestCase):
    def setUp(self):
        self.player = CFRPlayer.AIPlayer_CFR("Test", 10000)
        self.round_manager = CFRPlayer.Round([self.player], CFRPlayer.full_deck)
    
    #This test checks if the AI object is constructed correctly
    def testConstruction(self):
        self.assertEqual(self.player.name, "Test")
        self.assertEqual(len(self.player.hand_trees), 0)
        self.assertEqual(len(self.player.round_base_nodes), 0)
        self.assertEqual(self.player.current_node, None)
        self.assertEqual(self.player.base_pot, 0)
        self.assertEqual(len(self.player.opponent_history), 0)

    #This test checks if the AI generates trees for each new hand type it encounters,
    #and that it correctly names the first node of each tree after a combination
    #of two cards in the hand.
    def testGenerateTrees(self):
        self.player.pocket = [(14, 'Spades'), (3, 'Hearts'), (12, 'Clubs')]
        self.player.assess(self.round_manager)
        self.player.pocket.clear()
        self.player.pocket = [(13, 'Spades'), (3, 'Hearts'), (12, 'Clubs')]
        self.player.assess(self.round_manager)
        self.player.pocket.clear()
        self.player.pocket = [(11, 'Spades'), (3, 'Hearts'), (12, 'Clubs')]
        self.player.assess(self.round_manager)
        self.player.pocket.clear()
        
        self.assertEqual(len(self.player.hand_trees), 3)
        self.assertEqual(self.player.hand_trees[0].identity, "((14, 'Spades'), (12, 'Clubs'))")
        self.assertEqual(self.player.hand_trees[1].identity, "((13, 'Spades'), (12, 'Clubs'))")
        self.assertEqual(self.player.hand_trees[2].identity, "((12, 'Clubs'), (11, 'Spades'))")

    #This test checks that if the AI encounters a hand type it has previously
    #encountered, it doesn't create a new tree and it instead updates the previous
    #one.
    def testRepeatTrees(self):
        self.player.pocket = [(14, 'Spades'), (3, 'Hearts'), (12, 'Clubs')]
        self.player.assess(self.round_manager)
        self.player.pocket.clear()
        self.player.pocket = [(4, 'Spades'), (10, 'Spades'), (7, 'Diamonds')]
        self.player.assess(self.round_manager)
        self.player.pocket.clear()
        self.player.pocket = [(14, 'Spades'), (9, 'Diamonds'), (12, 'Clubs')]
        self.player.assess(self.round_manager)
        self.player.pocket.clear()
        
        self.assertEqual(len(self.player.hand_trees), 2)
        self.assertEqual(self.player.hand_trees[0].identity, "((14, 'Spades'), (12, 'Clubs'))")
        self.assertEqual(self.player.hand_trees[1].identity, "(0, 0)")
    
    #This test checks that the AI can make a decision without any errors or
    #crashing.
    def testMakeChoice(self):
        self.round_manager.dealPlayer(self.player, 3)
        self.player.assess(self.round_manager)
        opp = CFRPlayer.AIPlayer_CFR("Dummy", 10000)
        opp.last_move = "raise"
        self.player.choice([opp], 100)
    
if __name__ == '__main__':
    unittest.main()