from itertools import combinations

#This function checks a given 5-card hand to see which poker hand it is.
#The structure of the hand strength tuple is (ranking of the hand type, highest 
#value within the hand, second highest value in the hand), with an integer 
#value used to represent the ranking of each type of hand (with a straight 
#flush being 8 and a high card being 0).
#This can be made more efficient by reducing the number of times a hand needs
#to be checked.
def evaluateHand(hand):
    hand_strength = [0, 0, 0]
    
    #Straights and Flushes are checked first to determine if the player has
    #a straight flush (or royal flush) - the strongest possible hands
    possible_straight = checkStraight(hand)
    possible_flush = checkFlush(hand)
    if possible_straight[0] and possible_flush[0]:
        hand_strength[0] = 8
        hand_strength[1] = possible_straight[1]
        hand_strength[2] = possible_straight[2]
        return tuple(hand_strength)
    
    #The next strongest possible hand is a four of a kind
    possible_four = checkFourOfAKind(hand)
    if possible_four[0]:
        hand_strength = tuple(possible_four)
        return hand_strength
    
    #The next strongest possible hand is a full house (which consists of a
    #three of a kind and a pair).
    possible_full_house = checkFullHouse(hand)
    if possible_full_house[0]:
        hand_strength = tuple(possible_full_house)
        return hand_strength
    
    #The next strongest hand is a flush.
    if possible_flush[0]:
        hand_strength = tuple(possible_flush)
        return hand_strength
    
    #The next strongest hand is a straight.
    if possible_straight[0]:
        hand_strength = tuple(possible_straight)
        return hand_strength
    
    #The next strongest hand is a three of a kind.
    possible_three = checkThreeOfAKind(hand)
    if possible_three[0]:
        hand_strength = tuple(possible_three)
        return hand_strength
    
    #The next strongest hand is a two pair.
    possible_two_pair = checkTwoPair(hand)
    if possible_two_pair[0]:
        hand_strength = tuple(possible_two_pair)
        return hand_strength
    
    #The next strongest hand is a pair
    possible_pair = checkPair(hand)
    if possible_pair[0]:
        hand_strength = tuple(possible_pair)
        return hand_strength
    
    #If no other hand is obtained, the player is left with a high card.
    hand_strength = tuple(checkHighCard(hand))
    return hand_strength

#This function generates all posible hands a player could have and iterates
#over them to identify which is the strongest hand.
#It is a simple implementation and can be improved to be more efficient.
def evaluateAllHands(pocket, community):
    strongest_hand = (0, 0, 0)
    hands_checked = 0
    #Each possible amount of cards used from the pocket (0, 1 or 2) is checked.
    for pHSize in range(0, 3):
        #For a given number of cards used from the pocket, each possible 
        #combination of cards from the pocket that match that number is generated.
        pocket_combinations = combinations(pocket, pHSize)
        #All possible combinations for the remaining cards of the hand are
        #generated from the community cards.
        community_combinations = combinations(community, 5 - pHSize)
        #Each possible combination of pocket cards is iterated over.
        for pComb in pocket_combinations:
            #For a given set of pocket cards used, each possible set of
            #community cards used for the rest of the hand is iterated over.
            #This is inefficient and should be made more readable.
            community_combinations = list(community_combinations)
            for cComb in range(len(community_combinations)):
                #The chosen pocket cards and community cards are combined into
                #a 5-card hand, they are then ordered in descending order of
                #card values. This makes it easier to identify the highest-value
                #card in the hand and also places pairs next to each other.
                hand = sorted(pComb + community_combinations[cComb], reverse=True)
                #The strength of the hand is then determined.
                hand_strength = evaluateHand(hand)
                #If the hand is stronger than the previous strongest hand, it
                #replaces it.
                for i in range(len(hand_strength)):
                    if hand_strength[i] < strongest_hand[i]:
                        break
                    elif hand_strength[i] > strongest_hand[i]:
                        strongest_hand = hand_strength
                        break
                    
                hands_checked += 1
            
    return strongest_hand, hands_checked

def evaluateSubHand(pocket, community, subHandSize):
    return 0


#This function checks if the hand's values form a consecutive sequence, a hand
#known as a 'straight'.
def checkStraight(hand):
    low_ace = False
    for c in range(len(hand)-1):
        #An Ace is represented as 14 in the program, due to it being the 
        #highest-valued card. In a straight, an ace could instead be the lowest
        #card so this must be accounted for.
        if hand[c][0] == 14 and hand[c+1][0] == 5:
            low_ace = True
            continue
        
        if hand[c][0] != (hand[c+1][0] + 1):
            return (0, 0, 0)
    
    if low_ace:
        return (4, 5, 4)
    else:
        #The largest two cards will be the first two as the hand is ordered
        #descendingly.
        return (4, hand[0][0], hand[1][0])

#This function checks if the cards of the hand share the same suit, meaning the
#hand is a 'flush'.
def checkFlush(hand):
    #The suit to match is determined by the first card in the hand.
    suit = hand[0][1]
    for c in hand:
        if c[1] != suit:
            return (0, 0, 0)
    
    #As all cards share the same suit, no card can have a matching value so
    #the highest value card is the first card and the second-highest value is
    #the second card.
    return (5, hand[0][0], hand[1][0])

#This function checks if the hand contains a four of a kind.
def checkFourOfAKind(hand):
    for c in range(len(hand) - 3):
        #As the hand is sorted, cards of a four of a kind will be adjacent.
        if (hand[c][0] == hand[c+1][0] 
            and hand[c][0] == hand[c+2][0]
            and hand[c][0] == hand[c+3][0]):
            #If the first card of the four is not the first, the first card
            #of the hand is second most valuable card.
            if c:
                return (7, hand[c][0], hand[0][0])
            #If the first card of the hand is part of the four, the last card
            #isn't part of the four.
            else:
                return (7, hand[c][0], hand[len(hand)-1][0])
                
    return(0, 0, 0)

#This function checks to see if the hand is a 'full house,' containing a three
#of a kind and a separate pair.
def checkFullHouse(hand):
    triple_value = 0
    pair_value = 0
    
    matches = 0
    distinct_values = 1
    for c in range(len(hand) - 1): 
        if hand[c][0] == hand[c+1][0]:
            matches += 1
            if matches == 3:
                return (0, 0, 0)
        else:
            #If exactly two consecutive comparisons produce a matching value, 
            #then it is a three of a kind.
            if matches == 2:
                triple_value = hand[c][0]
            #If only one comparison produces a matching value, it is a pair.
            elif matches == 1:
                pair_value = hand[c][0]
                
            distinct_values += 1
            matches = 0
    
    #If the total number of different card values in the hand is 2, it is either
    #a full house or a Four of a Kind.
    if distinct_values == 2:
        if triple_value and pair_value == 0:
            pair_value = hand[len(hand)-1][0]
        else:
            triple_value = hand[len(hand)-1][0]
        return(6, triple_value, pair_value)
    
    return(0, 0, 0)

#This function checks to see if the hand contains a three of a kind.
def checkThreeOfAKind(hand):
    for c in range(len(hand) - 2):
        #As the hand is sorted, cards of a three of a kind will be adjacent.
        if hand[c][0] == hand[c+1][0] and hand[c][0] == hand[c+2][0]:
            if c:
                return (3, hand[c][0], hand[0][0])
            else:
                for i in range(len(hand)):
                    if hand[i][0] != hand[c][0]:
                        return (3, hand[c][0], hand[i][0])
          
    return(0, 0, 0)

#This function checks to see if the hand matches a two pair hand.
#A four of a kind hand would also return a two pair hand from this function but
#since a four of a kind will be checked earlier, only distinct two pairs are
#possible when this function is called.
def checkTwoPair(hand):
    first_pair = 0
    second_pair = 0
    
    #The first pair's first card must appear within the first two cards for
    #a valid two pair hand.
    for c in range(len(hand)-3):
        if hand[c][0] == hand[c+1][0]:
            first_pair = hand[c][0]
    
    #The second pair's first card must appear in the last three cards for a 
    #valid two pair hand.
    for c in range(2, len(hand)-1):
        if hand[c][0] == hand[c+1][0]:
            second_pair = hand[c][0]
    
    if first_pair and second_pair:
        return (2, first_pair, second_pair)
    else:
        return(0, 0, 0)

#This function checks to see if the hand contains a pair.
def checkPair(hand):
    for c in range(len(hand) - 1):
        #As the hand is sorted, cards of a pair will be adjacent.
        if hand[c][0] == hand[c+1][0]:
            #If the first card of the pair is not the first card of the hand,
            #the first card of the hand is the second most important card.
            if c:
                return (1, hand[c][0], hand[0][0])
            #Otherwise, the highest non-pair card will be the third card as
            #three of a kind and four of a kinds are already checked.
            else:
                return (1, hand[c][0], hand[2][0])
          
    return(0, 0, 0)

#If no other hand is achieved, the player has a high card so the two highest
#value cards are determined and returned.
def checkHighCard(hand):
    return (0, hand[0][0], hand[1][0])