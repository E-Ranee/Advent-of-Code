import collections

file = "input.txt"
# file = "test.txt"
# file = "test2.txt"

f = open(file, "r")
data = f.readlines()
f.close()

rows = []
for row in data:
    rows.append(row.strip().split()) # format ['32T3K', '765']

"""Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456"""

game_cards_list = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

def identify_hand_type(hand, bid, wild_jokers = False, game_cards_list = game_cards_list):
    """Takes a string representing a hand of cards and returns a tuple containing the category of hand and an int representing the relative value of the category"""

    # turn string into list
    list_of_cards = [card for card in hand]
    list_of_indices = [game_cards_list.index(card) for card in hand] # returns a list with the scores for each card where lower is better
    bid = int(bid)
    if wild_jokers: 
        list_of_indices = list(map(lambda x : 13 if x == 3 else x, list_of_indices)) # make joker have the lowest score, even if it's a "king"

    counter = collections.Counter(list_of_cards)
    counts = counter.most_common() # format [('3', 2), ('2', 1), ('T', 1), ('K', 1)] 

    if wild_jokers:
        joker_count = counter["J"]
        if joker_count > 0:
            for card_total in counts: # format ("3", 2)
                if card_total[0] == "J":
                    pass
                else:
                    for i in range(joker_count): # replace jokers with whatever the most common non joker card is 
                        list_of_cards.append(card_total[0])
                        list_of_cards.remove("J")
                    break
        counter = collections.Counter(list_of_cards) # recalculate totals with jokers pretending to be another card
        counts = counter.most_common() # format [('3', 2), ('2', 1), ('T', 1), ('K', 1)] 

    # we will count a lower score as better 
    # initial number refers to how good the category of hand is

    if counts[0][1] == 5: # five of a kind
        return [0] + list_of_indices + [bid]
    elif counts[0][1] == 4: # "Four of a kind"
        return [1] + list_of_indices + [bid]
    elif counts[0][1] == 3 and counts[1][1] == 2: # full house (three of a kind / two of a kind)
        return [2] + list_of_indices + [bid]
    elif counts[0][1] == 3: # "Three of a kind"
        return [3] + list_of_indices + [bid]
    elif counts[0][1] == 2 and counts[1][1] == 2: # two of a kind + two of a different kind
        return [4] + list_of_indices + [bid]
    elif counts[0][1] == 2: # one pair
        return [5] + list_of_indices + [bid]
    else: # all different
        return [6] + list_of_indices + [bid]
    
game_cards_list = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

def calculate_part(data, wild_jokers):
    all_scores = []
    for row in data: # format ['32T3K', '765']
        score = identify_hand_type(row[0], row[1], wild_jokers) # returns format ([5, 11, 12, 4, 11, 1, bid])
        all_scores.append(score) # Makes a list that can be easily sorted by type of hand, then how good the hand is within its category

    # sort it by hand category, then value of first card, then value of second card etc
    sorted_list = sorted(all_scores, key=lambda x: (x[0], x[1], x[2], x[3], x[4], x[5]), reverse=True)

    total_winnings = 0
    for index, item in enumerate(sorted_list):
        total_winnings += (index + 1) * item[6]

    return total_winnings

print("Part 1:", calculate_part(rows, False))
print("Part 2:", calculate_part(rows, True))