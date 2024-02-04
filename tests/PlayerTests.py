import unittest
import sys
sys.path.append('..')
from Game import Player


class testPlayer(unittest.TestCase):
    
    def setUp(self):
        self.player = Player("The Tester", 500)
    
    def testConstruction(self):
        self.assertEqual(self.player.name, "The Tester")
        self.assertEqual(self.player.chips, 500)
        self.assertEqual(self.player.bet, 0)
        self.assertFalse(self.player.folded)
    
    def testBasicCall(self):
        self.player.playCall(100)
        self.assertEqual(self.player.bet, 100)

    def testSuccessiveCall(self):
        self.player.playCall(100)
        self.assertEqual(self.player.bet, 100)
        self.player.playCall(200)
        self.assertEqual(self.player.bet, 200)
    
    def testAllInCall(self):
        self.player.playCall(1000)
        self.assertEqual(self.player.bet, 500)
    
    def testBasicRaise(self):
        self.player.playRaise(200)
        self.assertEqual(self.player.bet, 200)
    
    def testSuccessiveRaise(self):
        self.player.playRaise(100)
        self.assertEqual(self.player.bet, 100)
        self.player.playRaise(200)
        self.assertEqual(self.player.bet, 200)
    
    def testAllInRaise(self):
        self.player.playRaise(1000)
        self.assertEqual(self.player.bet, 500)
    
    def testFold(self):
        self.player.playFold()
        self.assertTrue(self.player.folded)

        
if __name__ == '__main__':
    unittest.main()
