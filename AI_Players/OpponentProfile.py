
class OpponentProfile():
    def __init__(self):
        #The 'raise_rate' attribute measures how likely it is that the opponent 
        #will raise, given that the wager value is a certain portion of their chips
        self.raise_rate = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1, 0.1, 0.0, 0.0]
        self.raise_coefficients = [0, 0, 0]
        #The 'fold_rate' attribute measures how likely it is that the opponent
        #will fold, given that the wager value is a certain portion of their chips
        self.fold_rates = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.9]
        self.fold_coefficients = [0, 0, 0]

        #The 'call_rate' attribute measures how likely it is that the opponent
        #will call/check, given that the wager value is a certain portion of their chips
        self.call_rates = [0.8, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.call_coefficients = [0, 0, 0]

        self.chip_percentage = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        self.game_marker = 2

        self.average_raise_value = 100
        self.raise_instances = 1

    def getRaiseRate(self):
        pass
    
    def getFoldRate(self):
        pass
    
    def getCallRate(self):
        pass
