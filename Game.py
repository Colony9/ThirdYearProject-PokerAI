class Player():
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.pocket = []
        self.bet = 0
        self.hand_strength = [0, 0, 0]
        self.folded = False
    
    def playCall(self, value):
        if value == 0:
            print(self.name + " checks")
            return

        if value >= self.chips:
            print(self.name + " goes all in")
            self.bet = self.chips
        else:
            print(self.name + " calls")
            self.bet = value
    
    def playRaise(self, value):       
        if value >= self.chips:
            print(self.name + " goes all in")
            self.bet = self.chips
        else:
            print(self.name + " raises " + str(value))
            self.bet = value

    def playFold(self):
        print(self.name + " folds")
        self.folded = True
        return