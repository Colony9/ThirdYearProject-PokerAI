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

    #The following tests test the 'evaluatePocket' function used for the CFR AI

    #A pocket with no discernable growth into a strong hand should be rejected
    #and not played.
    def testWeakPocket(self):
        self.pocket = [(3, 'Hearts'), (7, 'Clubs'), (2, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "(0, 0)")

    #A matching pair (of significant enough value) should be returned.
    def testPocketPair(self):
        self.pocket = [(6, 'Hearts'), (12, 'Clubs'), (12, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "((12, 'Diamonds'), (12, 'Clubs'))")

    #A pair of the lowest value (2), shouldn't be considered due to it being too
    #weak compared to other possible pockets.
    def testWeakPair(self):
        self.pocket = [(2, 'Hearts'), (2, 'Clubs'), (12, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "(0, 0)")

    #A set of two cards with equal suits and consecutive values should be accepted.
    def testSuitedAdjacency(self):
        self.pocket = [(9, 'Hearts'), (8, 'Hearts'), (2, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "((9, 'Hearts'), (8, 'Hearts'))")

    #If the consecutive values are too small, the combination shouldn't be accepted.
    def testWeakSuitedAdjacency(self):
        self.pocket = [(2, 'Hearts'), (3, 'Diamonds'), (4, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "(0, 0)")

    #If both cards share a suit, and one card is an ace, the combination should
    #be accepted.
    def testSuitedAce(self):
        self.pocket = [(2, 'Spades'),  (7, 'Diamonds'), (14, 'Spades')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "((14, 'Spades'), (2, 'Spades'))")

    #If both cards share a suit, and one card is a king while the other has a
    #value of at least 8, the combination should be accepted.
    def testValidSuitedKing(self):
        self.pocket = [(2, 'Spades'),  (8, 'Diamonds'), (13, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "((13, 'Diamonds'), (8, 'Diamonds'))")

    #If both cards share a suit, and one card is a king while the other has a
    #value of less than 8, the combination shouldn't be accepted.
    def testInvalidSuitedKing(self):
        self.pocket = [(2, 'Spades'),  (7, 'Diamonds'), (13, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "(0, 0)")

    #If both cards share a suit, and one card is a queen while the other has a
    #value of at least 9, the combination should be accepted.
    def testValidSuitedQueen(self):
        self.pocket = [(2, 'Spades'),  (9, 'Diamonds'), (12, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "((12, 'Diamonds'), (9, 'Diamonds'))")

    #If both cards share a suit, and one card is a queen while the other has a
    #value of less than 9, the combination shouldn't be accepted.
    def testInvalidSuitedQueen(self):
        self.pocket = [(2, 'Spades'),  (8, 'Diamonds'), (12, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "(0, 0)")

    #If both cards share a suit, and one card is a jack while the other has a
    #value of at least 9, the combination should be accepted.
    def testValidSuitedJack(self):
        self.pocket = [(2, 'Spades'),  (9, 'Diamonds'), (11, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "((11, 'Diamonds'), (9, 'Diamonds'))")

    #If both cards share a suit, and one card is a jack while the other has a
    #value of less than 9, the combination shouldn't be accepted.
    def testInvalidSuitedJack(self):
        self.pocket = [(2, 'Spades'),  (8, 'Diamonds'), (11, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "(0, 0)")

    #If a combination of two cards don't share either a suit or value, it
    #should only be accepted if either both cards have values greater than or
    #equal to a jack, or one card is an ace while the other is a 10.
    def testValidUnsuitedPocket(self):
        self.pocket = [(2, 'Spades'),  (11, 'Clubs'), (13, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "((13, 'Diamonds'), (11, 'Clubs'))")
        self.pocket = [(2, 'Spades'),  (10, 'Clubs'), (14, 'Hearts')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "((14, 'Hearts'), (10, 'Clubs'))")

    #If all three combinations in a pocket fail to meet the requirements of the
    #above test, it should be rejected.
    def testInvalidUnsuitedPocket(self):
        self.pocket = [(2, 'Spades'),  (6, 'Clubs'), (4, 'Diamonds')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "(0, 0)")
        self.pocket = [(2, 'Spades'),  (10, 'Clubs'), (13, 'Hearts')]
        result = evaluatePocket(self.pocket)
        self.assertEqual(result, "(0, 0)")


if __name__ == '__main__':
    unittest.main()
