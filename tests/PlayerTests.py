import unittest
import sys
sys.path.append('..')
from Game import Player


class testPlayer(unittest.TestCase):
    
    def setUp(self):
        self.player = Player("The Tester", 500)
    
    #This test checks that each attribute of the player is assigned correctly.
    def testConstruction(self):
        self.assertEqual(self.player.name, "The Tester")
        self.assertEqual(self.player.chips, 500)
        self.assertEqual(self.player.bet, 0)
        self.assertFalse(self.player.folded)
    
    #This test checks that the call method assigns the player's bet correctly.
    def testBasicCall(self):
        self.player.playCall(100)
        self.assertEqual(self.player.bet, 100)

    #This test checks that the call method assigns correctly, unaffected by
    #previous player choices.
    def testSuccessiveCall(self):
        self.player.playCall(100)
        self.assertEqual(self.player.bet, 100)
        self.player.playCall(200)
        self.assertEqual(self.player.bet, 200)
    
    #This test checks that a call made with a wager greater than the player's
    #current chips results in them going all in - with the correct bet value.
    def testAllInCall(self):
        self.player.playCall(1000)
        self.assertEqual(self.player.bet, self.player.chips)
    
    #This test checks that the raise methods assigns the player's bet correctly.
    def testBasicRaise(self):
        self.player.playRaise(200)
        self.assertEqual(self.player.bet, 200)
    
    #This test checks that the raise methods assigns (rather than adds) 
    #correctly when performed after a previous raise.
    def testSuccessiveRaise(self):
        self.player.playRaise(100)
        self.assertEqual(self.player.bet, 100)
        self.player.playRaise(200)
        self.assertEqual(self.player.bet, 200)
    
    #This test checks that a raise greater than the player's chips correctly
    #results in them going all in.
    def testAllInRaise(self):
        self.player.playRaise(1000)
        self.assertEqual(self.player.bet, self.player.chips)
    
    #This test checks that the fold methods correctly assigns the player's
    #'folded' status as true.
    def testFold(self):
        self.player.playFold()
        self.assertTrue(self.player.folded)

        
if __name__ == '__main__':
    unittest.main()
