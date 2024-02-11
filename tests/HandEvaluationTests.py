import unittest
import sys
sys.path.append('..')
from HandEvaluation import *

class testHandEvaluator(unittest.TestCase):
    def setUp(self):
        self.pocket = []
        self.community = []
    
    #This test checks that, when dealing with all 5 community cards, the correct 
    #number of possible hands are checked (46).
    def testNumHandsChecked_FullCommunity(self):
        self.pocket = [(2, "Diamonds"), (9, "Spades"), (12, "Diamonds")]
        self.community = [(2, "Spades"), (5, "Hearts"), (3, "Clubs"), (7, "Diamonds"), (14, "Spades")]
        _, num_hands_evaluated = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(num_hands_evaluated, 46)
    
if __name__ == '__main__':
    unittest.main()
