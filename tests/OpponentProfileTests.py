import unittest
import sys
sys.path.append('..')
from AI_Players import OpponentProfile

class testOpponentProfile(unittest.TestCase):
    def setUp(self):
        self.opp = OpponentProfile.OpponentProfile()
    
    #This test checks that the profile object is correctly constructed with
    #the correct attributes.
    def testConstruction(self):
        for i in range(11):
            self.assertEqual(self.opp.raise_rates[i], 0.33)
            self.assertEqual(self.opp.fold_rates[i], 0.33)
            self.assertEqual(self.opp.call_rates[i], 0.34)
            self.assertAlmostEqual(self.opp.chip_percentages[i], 0.1 * i)
            self.assertEqual(self.opp.action_count[i], 0)
    
    #This test checks that the get rates functions correctly obtain a line of 
    #best fit, using the horizontal line that the initial rates fit to.
    def testGetRates_BaseRate(self):
        result = self.opp.getRaiseRate()
        self.assertAlmostEqual(result[0], 0)
        self.assertAlmostEqual(result[1], 0)
        self.assertAlmostEqual(result[2], 0.33)
        
        result = self.opp.getFoldRate()
        self.assertAlmostEqual(result[0], 0)
        self.assertAlmostEqual(result[1], 0)
        self.assertAlmostEqual(result[2], 0.33)
        
        result = self.opp.getCallRate()
        self.assertAlmostEqual(result[0], 0)
        self.assertAlmostEqual(result[1], 0)
        self.assertAlmostEqual(result[2], 0.34)
     
    #This test checks that the 'updateRaise' method correctly calculates the
    #new average raise value and also correctly updates the raise_rates at the
    #correct index.
    def testUpdateRaise(self):
        self.opp.updateRaise(1000, 0, 10000)
        self.assertEqual(self.opp.average_raise_value, 1000)
        self.assertEqual(self.opp.raise_rates[0], 1)
        
        self.opp.updateRaise(2000, 0, 10000)
        self.assertEqual(self.opp.average_raise_value, 1500)
        self.assertEqual(self.opp.raise_rates[0], 1)
    
    #This test checks that the update methods correctly calculates the new rates
    #for each possible action, at the correct index. When an action is performed,
    #the rate for the performed action should increase, while other actions
    #should have their rates decrease.
    def testUpdateOdds(self):
        self.opp.updateCall(0, 10000)
        self.opp.updateFold(0, 10000)
        
        self.assertEqual(self.opp.fold_rates[0], 0.5)
        self.assertEqual(self.opp.call_rates[0], 0.5)
        self.assertEqual(self.opp.fold_rates[1], 0.33)
        self.assertEqual(self.opp.call_rates[1], 0.34) 
        
        self.opp.updateCall(0, 10000)
        self.opp.updateCall(0, 10000)
        self.assertEqual(self.opp.fold_rates[0], 0.25)
        self.assertEqual(self.opp.call_rates[0], 0.75)
    
    #This test checks that, when the wager value is greater than the opponent's
    #chips, the rates are modified at the final index.
    def testWagerGreaterThanChips(self):
        self.opp.updateRaise(1, 2000, 1000)
        self.assertEqual(self.opp.raise_rates[10], 1)
        
        self.opp.updateCall(2000, 1000)
        self.assertEqual(self.opp.call_rates[10], 0.5)
        
        self.opp.updateFold(2000, 1000)
        self.assertAlmostEqual(self.opp.fold_rates[10], 1.0 / 3.0)
        
        
if __name__ == '__main__':
    unittest.main()