from Game import *
from Deck import *
from HandEvaluation import renderHand
import sys
sys.path.append('AI_Players')
import BasicAIPlayers, CFRPlayer

def playRound(players):
    round_manager = Round(players, full_deck)
    start_chips = []
    
    for p in players:
        start_chips.append(p.chips)
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
    winner = [round_manager.determineWinningHand(), round_manager.payout(), 0]
    winner[2] = max(players[0].chips - start_chips[0], players[1].chips - start_chips[1])
    players[0].review(winner, players[1].folded, True)
    players[1].review(winner, players[0].folded, False)

    for p in players:
        p.hand_strength = [0, 0, 0]
        p.folded = False
        p.no_more_bets = False
        p.pocket.clear()

    return winner[1]

def CFR_output(CFR_AI):
    hand_tree_list = []
    for tree in CFR_AI.hand_trees:
        hand_tree_list.append(tree.identity)
    print("Hand Trees: " + str(hand_tree_list))
    for opp in CFR_AI.opponent_profiles_list:
        print(CFR_AI.opponent_profiles_list.index(opp))
        print("Opponent Max Chips: " + str(opp.max_chips))
        print("Opponent Average Raise: " + str(opp.average_raise_value))
        print("Opponent all in rates: " + str(opp.allIn_rates))
        print("Opponent raise rates: " + str(opp.raise_rates))
        print("Opponent call rates: " + str(opp.call_rates))
        print("Opponent fold rates: " + str(opp.fold_rates))

if __name__ == "__main__":
    CFR = False
    print("-Lazy Pineapple Hold'em-")
    username = input("Enter your name: ")
    user = humanPlayer(username, 10000)
    while True:
        try:
            opponent_type = int(input("Choose opponent: "))
            break
        except:
            print("Invalid option")
    match opponent_type:
        case 1:
            opponent = BasicAIPlayers.AIplayer_Random("COM #1", 10000)
        case 2:
            opponent = BasicAIPlayers.AIplayer_AlwaysCallOrLowRaise("COM #2", 10000)
        case 3:
            opponent = BasicAIPlayers.AIplayer_AlwaysAllIn("COM #3", 10000)
        case 4:
            opponent = BasicAIPlayers.AIplayer_FoldIfNoPair("COM #4", 10000)
        case 5:
            opponent = BasicAIPlayers.AIplayer_CallUpToHalf("COM #5", 10000)
        case 6:
            CFR = True
            opponent = CFRPlayer.AIPlayer_CFR("COM #6", 10000)
        case _:
            CFR = True
            opponent = CFRPlayer.AIPlayer_CFR("COM #6", 10000)

    #rounds = 0
    #rounds_won = 0
    #rounds_tied = 0
    #chips_won = 0
    while True:
        start_chips = user.chips
        winner = playRound([user, opponent])
        print(user.name + " chips: " + str(user.chips))
        print(opponent.name + " chips: " + str(opponent.chips) + '\n')
        #if winner is not None:
            #if winner.name == user.name:
                #rounds_won += 1
        #else:
            #rounds_tied += 1
        #chips_won += user.chips - start_chips
        #rounds += 1
        #if rounds == 10000:
            #print("Rounds won: " + str(rounds_won))
            #print("Rounds tied: " + str(rounds_tied))
            #print("Chips won: " + str(chips_won))
            #break
        #user.chips = 10000
        #opponent.chips = 10000
        replay = input("Would you like to play another round? ")
        if len(replay) == 0:
            CFR_output(opponent)
            break
        elif (replay.lower())[0] != 'y':
            CFR_output(opponent)
            break
        print("\n------\n\n------\n")