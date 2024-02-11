import unittest
import sys
sys.path.append('..')
from Game import Player, Round
from Deck import full_deck

class testRound(unittest.TestCase):
    
    def setUp(self):
        self.player1 = Player("First Player", 500)
        self.player2 = Player("Second Player", 1000)
        self.round = Round([self.player1, self.player2], full_deck)
    
    #This test checks that the 'dealPlayer' method correctly assigns cards from
    #the deck to the player's pocket and moves the 'deck_top' marker forward by
    #the correct amount.
    def testDealPlayer(self):
        self.round.dealPlayer(self.player1, 3)
        self.assertEqual(len(self.player1.pocket), 3)
        self.assertEqual(self.round.deck_top, 3)
        
        self.round.dealPlayer(self.player2, 3)
        self.assertEqual(len(self.player2.pocket), 3)
        self.assertEqual(self.round.deck_top, 6)
    
    #This test checks that the community cards can be dealt correctly, similar
    #to the pocket cards.
    def testDealCommunity(self):
        self.round.dealCommunity(3)
        self.assertEqual(len(self.round.community_cards), 3)
        self.assertEqual(self.round.deck_top, 3)
        
        self.round.dealCommunity(1)
        self.assertEqual(len(self.round.community_cards), 4)
        self.assertEqual(self.round.deck_top, 4)
        self.round.dealCommunity(1)
        
        self.assertEqual(len(self.round.community_cards), 5)
        self.assertEqual(self.round.deck_top, 5)
    
    #This test checks that the dealing methods will return without doing
    #anything if given a negative number of cards to deal.
    def testDealNegative(self):
        self.round.dealPlayer(self.player1, -2)
        self.assertEqual(len(self.player1.pocket), 0)
        self.assertEqual(self.round.deck_top, 0)
        
        self.round.dealCommunity(-2)
        self.assertEqual(len(self.round.community_cards), 0)
        self.assertEqual(self.round.deck_top, 0)
    
    #This test simulates a simple betting round before collecting the bets,
    #determining whether the pot's value is calculated correctly and that
    #chips are successfully deducted from the players.
    def testCollectBets(self):
        self.player1.playRaise(200)
        self.player2.playCall(200)
        self.player1.playCall(200)
        
        self.round.collectBets()
        self.assertEqual(self.round.pot, 400)
        self.assertEqual(self.player1.chips, 300)
        self.assertEqual(self.player2.chips, 800)
    
    #This test checks that the 'collectBets' method treats a negative-value bet
    #as equal to 0.
    def testCollectBetsNegative(self):
        self.player1.bet = -100
        self.player2.bet = 100
        self.round.collectBets()
        self.assertEqual(self.round.pot, 100)
    
    #This test checks that the 'payout' method correctly adds the pot's value
    #to the winning player's chips before setting the pot to 0.
    def testPayout(self):
        self.round.pot = 400
        self.player1.hand_strength = (8,7,6)
        self.player2.hand_strength = (1,3,7)
        self.round.payout()
        self.assertEqual(self.player1.chips, 900)
        self.assertEqual(self.round.pot, 0)

if __name__ == '__main__':
    unittest.main()
    
        