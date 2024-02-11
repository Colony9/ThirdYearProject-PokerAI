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
      
    #This test checks that a 'Pair' hand is correctly determined.
    def testPair(self):
        self.pocket = [(2, "Diamonds"), (9, "Spades"), (12, "Diamonds")]
        self.community = [(2, "Spades"), (5, "Hearts"), (3, "Clubs"), (7, "Diamonds"), (14, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (1, 2, 14))
    
    #This test checks that a 'Two Pair' hand is correctly determined.
    def testTwoPair(self):
        self.pocket = [(2, "Diamonds"), (7, "Spades"), (12, "Diamonds")]
        self.community = [(2, "Spades"), (5, "Hearts"), (3, "Clubs"), (7, "Diamonds"), (14, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (2, 7, 2))
    
    #This test checks that a 'Three of a Kind' hand is correctly determined.
    def testThreeOfAKind(self):
        self.pocket = [(2, "Diamonds"), (7, "Spades"), (2, "Diamonds")]
        self.community = [(2, "Spades"), (5, "Hearts"), (3, "Clubs"), (7, "Diamonds"), (14, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (3, 2, 14))
    
    #This test checks that a 'Straight' hand is correctly determined.
    def testStraight(self):
        self.pocket = [(2, "Diamonds"), (7, "Spades"), (4, "Diamonds")]
        self.community = [(6, "Spades"), (5, "Hearts"), (3, "Clubs"), (7, "Diamonds"), (10, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (4, 7, 6))
    
    #This test checks that a 'Straight' hand is correctly determined, if an Ace
    #is used for the value '1' rather than outranking all other cards. The
    #strongest card in the hand should have the value '5'.
    def testStraight_LowAce(self):
        self.pocket = [(2, "Diamonds"), (11, "Spades"), (4, "Diamonds")]
        self.community = [(11, "Spades"), (5, "Hearts"), (3, "Clubs"), (9, "Diamonds"), (14, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (4, 5, 4))
    
    #This test checks that a 'Flush' hand is correctly determined.
    def testFlush(self):
        self.pocket = [(2, "Diamonds"), (7, "Spades"), (12, "Diamonds")]
        self.community = [(2, "Spades"), (5, "Diamonds"), (3, "Clubs"), (7, "Diamonds"), (14, "Diamonds")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (5, 14, 12))
    
    #This test checks that a 'Full House' hand is correctly determined.
    def testFullHouse(self):
        self.pocket = [(2, "Diamonds"), (4, "Spades"), (2, "Hearts")]
        self.community = [(2, "Spades"), (3, "Hearts"), (3, "Clubs"), (7, "Diamonds"), (14, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (6, 2, 3))
    
    #This test checks that a 'Four of a Kind' hand does not appear as a 'Full
    #House' hand when evaluated.
    def testFullHouse_FourOfAKind(self):
        self.hand = [(14, "Diamonds"), (14, "Hearts"), (14, "Clubs"), (14, "Spades"), (7, "Diamonds")]
        testHand = checkFullHouse(self.hand)
        self.assertEqual(testHand, (0, 0, 0))
    
    #This test checks that a 'Four of a Kind' hand is correctly determined.
    def testFourOfAKind(self):
        self.pocket = [(14, "Diamonds"), (7, "Spades"), (12, "Diamonds")]
        self.community = [(2, "Spades"), (14, "Hearts"), (14, "Clubs"), (7, "Diamonds"), (14, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (7, 14, 12))
    
    #This test checks that a 'Straight Flush' hand is correctly determined.
    def testStraightFlush(self):
        self.pocket = [(5, "Diamonds"), (7, "Spades"), (4, "Diamonds")]
        self.community = [(2, "Spades"), (3, "Diamonds"), (6, "Diamonds"), (7, "Diamonds"), (14, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (8, 7, 6)) 
        
    #This test checks that the strongest cards for a 'High Card' hand are 
    #correctly determined.
    def testHighCard(self):
        self.pocket = [(11, "Diamonds"), (9, "Spades"), (12, "Diamonds")]
        self.community = [(2, "Spades"), (5, "Hearts"), (3, "Clubs"), (7, "Diamonds"), (14, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (0, 14, 12))
    
    #This test checks that no more than 2 pocket cards are included in a hand.
    #If all three pocket cards were included in the hand, it would evaluate as
    #a 'Four of a Kind'.
    def testMaxTwoPockets(self):
        self.pocket = [(2, "Diamonds"), (2, "Spades"), (2, "Clubs")]
        self.community = [(2, "Spades"), (5, "Hearts"), (3, "Clubs"), (7, "Diamonds"), (14, "Spades")]
        testHand, _ = evaluateAllHands(self.pocket, self.community)
        self.assertEqual(testHand, (3, 2, 14))
    
if __name__ == '__main__':
    unittest.main()
