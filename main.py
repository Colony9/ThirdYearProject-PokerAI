from Game import *
from Deck import *
from HandEvaluation import renderHand
from AI_Players import BasicAIPlayers

def playRound(players):
    round_manager = Round(players, full_deck)
    
    for p in players:
        round_manager.dealPlayer(p, 3)
        p.assess(round_manager)
    print("Your cards: " + renderCards(players[0].pocket))
    #Blind bet rates are set to 50 for the big blind and 25 for the small blind.
    players[0].bet = 50
    players[1].bet = 25
    round_manager.bettingRound()
    round_manager.collectBets()
    
    print("\n------\n")
    round_manager.dealCommunity(3)
    for p in players:
        p.assess(round_manager)
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your best hand is: " + renderHand(players[0].hand_strength) + '\n')
    round_manager.bettingRound()
    round_manager.collectBets()

    print("\n------\n")
    round_manager.dealCommunity(1)
    for p in players:        
        p.assess(round_manager)
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your best hand is: " + renderHand(players[0].hand_strength)  + '\n')
    round_manager.bettingRound()
    round_manager.collectBets()
    
    print("\n------\n")
    round_manager.dealCommunity(1)
    for p in players:
        p.assess(round_manager)
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your best hand is: " + renderHand(players[0].hand_strength) + '\n')
    round_manager.bettingRound()
    round_manager.collectBets()
    
    print("\n------\n")
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your hand is: " + renderHand(players[0].hand_strength) + '\n')
    print(players[1].name + "'s cards: " + renderCards(players[1].pocket))
    print(players[1].name + "'s hand is: " + renderHand(players[1].hand_strength))
    return round_manager.payout()

    

if __name__ == "__main__":
    print("-Lazy Pineapple Hold'em-")
    username = input("Enter your name: ")
    user = humanPlayer(username, 10000)
    opponent_type = int(input("Choose opponent: "))
    match opponent_type:
        case 1:
            opponent = BasicAIPlayers.AIplayer_Random("Random", 10000)
        case 2:
            opponent = BasicAIPlayers.AIplayer_AlwaysCallOrLowRaise("Conservative", 10000)
        case 3:
            opponent = BasicAIPlayers.AIplayer_AlwaysAllIn("All In", 10000)
        case 4:
            opponent = BasicAIPlayers.AIplayer_FoldIfNoPair("Need a pair", 10000)
        case 5:
            opponent = BasicAIPlayers.AIplayer_CallUpToHalf("50% Limit", 10000)
        case _:
            opponent = BasicAIPlayers.AIplayer_AlwaysCall("Always Call", 10000)

    while True:
        start_chips = user.chips
        winner = playRound([user, opponent])
        print(user.name + " chips: " + str(user.chips))
        print(opponent.name + " chips: " + str(opponent.chips) + '\n')
        replay = input("Would you like to play another round? ")
        if (replay.lower())[0] != 'y':
            break
        print("\n------\n\n------\n")