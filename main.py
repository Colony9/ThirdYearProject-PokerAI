from Game import *
from Deck import *
from HandEvaluation import *

def playRound(players):
    round_manager = Round(players, full_deck)
    
    round_manager.dealPlayer(players[0], 3)
    round_manager.dealPlayer(players[1], 3)
    print("Your cards: " + renderCards(players[0].pocket))
    round_manager.bettingRound()
    round_manager.collectBets()
    
    round_manager.dealCommunity(3)
    players[0].hand_strength, _ = evaluateAllHands(players[0].pocket, 
                                               round_manager.community_cards)    
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your best hand is: " + renderHand(players[0].hand_strength) + '\n')
    round_manager.bettingRound()
    round_manager.collectBets()
    
    round_manager.dealCommunity(1)
    players[0].hand_strength, _ = evaluateAllHands(players[0].pocket, 
                                               round_manager.community_cards)
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your best hand is: " + renderHand(players[0].hand_strength)  + '\n')
    round_manager.bettingRound()
    round_manager.collectBets()
    
    round_manager.dealCommunity(1)
    players[0].hand_strength, _ = evaluateAllHands(players[0].pocket, 
                                               round_manager.community_cards)
    print("Community cards: " + renderCards(round_manager.community_cards))
    print("Your cards: " + renderCards(players[0].pocket))
    print("Your best hand is: " + renderHand(players[0].hand_strength) + '\n')
    round_manager.bettingRound()
    round_manager.collectBets()
    
    players[1].hand_strength, _ = evaluateAllHands(players[1].pocket, 
                                               round_manager.community_cards)
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
    opponent = humanPlayer("Dummy", 1000)
    playRound([user, opponent])