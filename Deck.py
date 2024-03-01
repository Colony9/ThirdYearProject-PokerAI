#Jacks are represented by the number 11, Queens by 12, Kings by 13 and Aces by 14.
full_deck = []
for suit in ["Spades", "Clubs", "Diamonds", "Hearts"]:
    for val in range(2,15):
        full_deck.append((val, suit))

card_values = {
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "Jack",
        12: "Queen",
        13: "King",
        14: "Ace"
    }

#This function provides a human-readable string output of a list of cards
def renderCards(cards):
    output = ""
    for c in cards:
        output += card_values[c[0]] + " of " + c[1] + ", "
    
    output = output[:-2]
    return output