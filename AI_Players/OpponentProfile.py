class OpponentProfile():
    def __init__(self, max_chips):
        #The 'raise_rate' attribute measures how likely it is that the opponent 
        #will raise, given that the wager value is a certain portion of their chips
        self.allIn_rates = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
        
        #The 'raise_rate' attribute measures how likely it is that the opponent 
        #will raise, given that the wager value is a certain portion of their chips
        self.raise_rates = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
        #The 'fold_rate' attribute measures how likely it is that the opponent
        #will fold, given that the wager value is a certain portion of their chips
        self.fold_rates = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]

        #The 'call_rate' attribute measures how likely it is that the opponent
        #will call/check, given that the wager value is a certain portion of their chips
        self.call_rates = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]

        #The 'chip_percentage' value stores a list of percentages of the opponent's
        #chips to use to construct lines of best fit.
        self.chip_percentages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        #The 'action_count' attribute measures how many decisions the opponent
        #has made for each chip percentage value.
        self.action_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.average_raise_value = 100
        self.raise_instances = 0

        self.max_chips = max_chips

    #This function creates a quadratic line of best fit to estimate the opponents
    #odds of raising, dependent on the percentage of their chips they are required
    #to wager to call.
    def getAllInRate(self, wager):
        if wager > self.max_chips:
            action_threshold = 10
        else:
            action_threshold = int(round(wager / self.max_chips, 1) / 0.1)

        return self.allIn_rates[action_threshold]

    #This function creates a quadratic line of best fit to estimate the opponents
    #odds of raising, dependent on the percentage of their chips they are required
    #to wager to call.
    def getRaiseRate(self, wager):
        if wager > self.max_chips:
            action_threshold = 10
        else:
            action_threshold = int(round(wager / self.max_chips, 1) / 0.1)

        return self.raise_rates[action_threshold]

    #This function creates a quadratic line of best fit to estimate the opponents
    #odds of folding, dependent on the percentage of their chips they are required
    #to wager to call.
    def getFoldRate(self, wager):
        if wager > self.max_chips:
            action_threshold = 10
        else:
            action_threshold = int(round(wager / self.max_chips, 1) / 0.1)

        return self.fold_rates[action_threshold]

    #This function creates a quadratic line of best fit to estimate the opponents
    #odds of calling, dependent on the percentage of their chips they are required
    #to wager to call.
    def getCallRate(self, wager):
        if wager > self.max_chips:
            action_threshold = 10
        else:
            action_threshold = int(round(wager / self.max_chips, 1) / 0.1)

        return self.call_rates[action_threshold]

    #If the opponent calls, this function updates the rates attributes to reflect
    #the new decision made.
    def updateAllIn(self, wager, chips):
        #If the wager value exceeds the amount of chips they have, it is no
        #different from having to bet all of their chips.
        if wager > chips:
            action_threshold = 10
        else:
            action_threshold = int(round(wager / chips, 1) / 0.1)

        self.allIn_rates[action_threshold] = ((self.allIn_rates[action_threshold] * self.action_count[action_threshold]) + 1) / (self.action_count[action_threshold] + 1)
        self.raise_rates[action_threshold] = (self.raise_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.fold_rates[action_threshold] = (self.fold_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.call_rates[action_threshold] = (self.call_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.action_count[action_threshold] += 1

    #If the opponent raises, this function recalculates the average value they 
    #raise by as well as updating the rates attributes to reflect the new decision
    #made.
    def updateRaise(self, new_raise, wager, chips):
        self.average_raise_value = int(((self.average_raise_value * self.raise_instances) + new_raise) / (self.raise_instances + 1))
        self.raise_instances += 1

        #If the wager value exceeds the amount of chips they have, it is no
        #different from having to bet all of their chips.
        if wager > chips:
            action_threshold = 10
        else:
            action_threshold = int(round(wager / chips, 1) / 0.1)
        
        self.allIn_rates[action_threshold] = (self.allIn_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.raise_rates[action_threshold] = ((self.raise_rates[action_threshold] * self.action_count[action_threshold]) + 1) / (self.action_count[action_threshold] + 1)
        self.fold_rates[action_threshold] = (self.fold_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.call_rates[action_threshold] = (self.call_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.action_count[action_threshold] += 1     

    #If the opponent folds, this function updates the rates attributes to reflect
    #the new decision made.
    def updateFold(self, wager, chips):
        #If the wager value exceeds the amount of chips they have, it is no
        #different from having to bet all of their chips.
        if wager > chips:
            action_threshold = 10
        else:
            action_threshold = int(round(wager / chips, 1) / 0.1)

        self.allIn_rates[action_threshold] = (self.allIn_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.raise_rates[action_threshold] = (self.raise_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.fold_rates[action_threshold] = ((self.fold_rates[action_threshold] * self.action_count[action_threshold]) + 1) / (self.action_count[action_threshold] + 1)
        self.call_rates[action_threshold] = (self.call_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.action_count[action_threshold] += 1   

    #If the opponent calls, this function updates the rates attributes to reflect
    #the new decision made.
    def updateCall(self, wager, chips):
        #If the wager value exceeds the amount of chips they have, it is no
        #different from having to bet all of their chips.
        if wager > chips:
            action_threshold = 10
        else:
            action_threshold = int(round(wager / chips, 1) / 0.1)

        self.allIn_rates[action_threshold] = (self.allIn_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.raise_rates[action_threshold] = (self.raise_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.fold_rates[action_threshold] = (self.fold_rates[action_threshold] * self.action_count[action_threshold]) / (self.action_count[action_threshold] + 1)
        self.call_rates[action_threshold] = ((self.call_rates[action_threshold] * self.action_count[action_threshold]) + 1) / (self.action_count[action_threshold] + 1)
        self.action_count[action_threshold] += 1
    