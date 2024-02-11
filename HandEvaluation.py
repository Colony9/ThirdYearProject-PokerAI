from itertools import combinations

def evaluateHand(hand):
    return (0, 0, 0)

#This function generates all posible hands a player could have and iterates
#over them to identify which is the strongest hand.
#It is a simple implementation and can be improved to be more efficient.
def evaluateAllHands(pocket, community):
    strongestHand = (0, 0, 0)
    hands_checked = 0
    for pHSize in range(0, 3):
        pocket_combinations = combinations(pocket, pHSize)
        community_combinations = combinations(community, 5 - pHSize)
        for pComb in pocket_combinations:
            #
            #This is inefficient and can be made more readable
            community_combinations = list(community_combinations)
            for cComb in range(len(community_combinations)):
                hand = sorted(pComb + community_combinations[cComb])
                handStrength = evaluateHand(hand)
                hands_checked += 1
            
    return strongestHand, hands_checked

def evaluateSubHand(pocket, community, subHandSize):
    return 0


def checkStraight(hand):
    return (0, 0, 0)

def checkFlush(hand):
    return (0, 0, 0)

def checkFourOfAKind(hand):
    return(0, 0, 0)

def checkFullHouse(hand):
    return(0, 0, 0)

def checkThreeOfAKind(hand):
    return (0, 0, 0)

def checkTwoPair(hand):
    return(0, 0, 0)

def checkPair(hand):
    return(0, 0, 0)

def checkHighCard(hand):
    return (0, 0, 0)