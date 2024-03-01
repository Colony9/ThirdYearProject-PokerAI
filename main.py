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
    round_manager.bettingRound()
    round_manager.collectBets()
    
    print("\n\n\n\n\n")
    round_manager.dealCommunity(3)
    for p in players:
        print(p.name)
        p.assess(round_manager)
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your best hand is: " + renderHand(players[0].hand_strength) + '\n')
    round_manager.bettingRound()
    round_manager.collectBets()

    print("\n\n\n\n\n")
    round_manager.dealCommunity(1)
    for p in players:
        
        p.assess(round_manager)
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your best hand is: " + renderHand(players[0].hand_strength)  + '\n')
    round_manager.bettingRound()
    round_manager.collectBets()
    
    print("\n\n\n\n\n")
    round_manager.dealCommunity(1)
    for p in players:
        p.assess(round_manager)
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your best hand is: " + renderHand(players[0].hand_strength) + '\n')
    round_manager.bettingRound()
    round_manager.collectBets()
    
    print("\n\n\n\n\n")
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your hand is: " + renderHand(players[0].hand_strength) + '\n')
    print(players[1].name + "'s cards: " + renderCards(players[1].pocket))
    print(players[1].name + "'s hand is: " + renderHand(players[1].hand_strength))
    round_manager.payout()
    

if __name__ == "__main__":
    print("-Lazy Pineapple Hold'em-")
    username = input("Enter your name: ")
    user = humanPlayer(username, 1000)
    opponent_type = int(input("Choose opponent: "))
    match opponent_type:
        case 1:
            opponent = BasicAIPlayers.AIplayer_Random("Dummy", 1000)
        case 2:
            opponent = BasicAIPlayers.AIplayer_AlwaysCall("Dummy", 1000)
        case 3:
            opponent = BasicAIPlayers.AIplayer_AlwaysAllIn("Dummy", 1000)
        case 4:
            opponent = BasicAIPlayers.AIplayer_FoldIfNoPair("Dummy", 1000)
        case 5:
            opponent = BasicAIPlayers.AIplayer_CallUpToHalf("Dummy", 1000)
        case _:
            opponent = BasicAIPlayers.AIplayer_AlwaysCall("Dummy", 1000)

    while True:
        playRound([user, opponent])
        replay = input("Would you like to play another round? ")
        if (replay.lower())[0] != 'y':
            break