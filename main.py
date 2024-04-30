from Game import *
from Deck import *
from HandEvaluation import renderHand
import sys
sys.path.append('AI_Players')
import BasicAIPlayers, CFRPlayer
from OpponentProfile import OpponentProfile

#This function performs with a full game of Poker with the players it is passed
#as an argument.
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

#This function performs a full game of Poker, but without the print statements
#to speed up the training process for the CFR AI.
def trainRound(players):
    round_manager = Round(players, full_deck)
    start_chips = []
    
    for p in players:
        start_chips.append(p.chips)
        round_manager.dealPlayer(p, 3)
        p.assess(round_manager)
    players[0].bet = 50
    players[1].bet = 25
    round_manager.bettingRound()
    round_manager.collectBets()

    round_manager.dealCommunity(3)
    for p in players:
        p.assess(round_manager)
    round_manager.bettingRound()
    round_manager.collectBets()

    round_manager.dealCommunity(1)
    for p in players:        
        p.assess(round_manager)
    round_manager.bettingRound()
    round_manager.collectBets()
    
    round_manager.dealCommunity(1)
    for p in players:
        p.assess(round_manager)
    round_manager.bettingRound()
    round_manager.collectBets()

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

def pretrainCFR(CFR_AI):
    rounds = 0
    training_dummy = CFRPlayer.AIPlayer_CFR("Dummy", 10000, CFR_AI.big_blind == False)
    while True:
        start_chips = CFR_AI.chips
        print("round: " + str(rounds + 1))
        if CFR_AI.big_blind:
            winner = trainRound([CFR_AI, training_dummy])
        else:
            winner = trainRound([training_dummy, CFR_AI])
        print(CFR_AI.name + " chips: " + str(CFR_AI.chips))
        print(training_dummy.name + " chips: " + str(training_dummy.chips) + '\n')
        rounds += 1
        CFR_AI.chips = 10000
        training_dummy.chips = 10000
        if rounds == 10000:
            break


if __name__ == "__main__":
    CFR = False
    print("-Lazy Pineapple Hold'em-")
    username = input("Enter your name: ")
    user = humanPlayer(username, 10000)
    #pretrain_decision = input("Would you like to pre-train yourself?")
    #if len(pretrain_decision) > 0:
        #if (pretrain_decision.lower())[0] == "y":
            #pretrainCFR(user)

    while True:
        try:
            opponent_type = int(input("Choose opponent: "))
            break
        except:
            print("Invalid option")
    if opponent_type == 1:
        opponent = BasicAIPlayers.AIplayer_Random("COM #1", 10000)
    elif opponent_type == 2:
        opponent = BasicAIPlayers.AIplayer_AlwaysCallOrLowRaise("COM #2", 10000)
    elif opponent_type == 3:
        opponent = BasicAIPlayers.AIplayer_AlwaysAllIn("COM #3", 10000)
    elif opponent_type == 4:
        opponent = BasicAIPlayers.AIplayer_FoldIfNoPair("COM #4", 10000)
    elif opponent_type == 5:
        opponent = BasicAIPlayers.AIplayer_CallUpToHalf("COM #5", 10000)
    else:
        CFR = True
        opponent = CFRPlayer.AIPlayer_CFR("COM #6", 10000, False)
        pretrain_decision = input("Would you like to pre-train your opponent?")
        if len(pretrain_decision) > 0:
            if (pretrain_decision.lower())[0] == "y":
                pretrainCFR(opponent)
                opponent.opponent_profiles_list = [OpponentProfile(10000), OpponentProfile(10000), OpponentProfile(10000), OpponentProfile(10000)]
                opponent.opponent_profile = opponent.opponent_profiles_list[0]

    rounds = 0
    #rounds_won = 0
    #rounds_tied = 0
    #chips_won = 0
    while True:
        #start_chips = user.chips
        print("round: " + str(rounds + 1))
        winner = playRound([user, opponent])
        print(user.name + " chips: " + str(user.chips))
        print(opponent.name + " chips: " + str(opponent.chips) + '\n')
        #if winner is not None:
            #if winner.name == user.name:
                #rounds_won += 1
        #else:
            #rounds_tied += 1
        #chips_won += user.chips - start_chips
        rounds += 1
        #if rounds == 5:
            #print("Rounds won: " + str(rounds_won) + "/10000")
            #print("Rounds tied: " + str(rounds_tied) + "/10000")
            #print("Chips won: " + str(chips_won))
            #break
        #user.chips = 10000
        #opponent.chips = 10000
        replay = input("Would you like to play another round? ")
        if len(replay) == 0:
           break
        elif (replay.lower())[0] != 'y':
            break
        print("\n------\n\n------\n")