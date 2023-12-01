f = open(f"input.txt", "r")
data = f.readlines()
f.close()

# a = rock = x
# b = paper = y
# c = scissors = z

actions = {
    "A": "rock",
    "B": "paper",
    "C": "scissors"
}

decoded_actions = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors"
}

actions.update(decoded_actions)

# score = shape + result
# 1 = rock, 2 = paper, 3 = scissors
# 0 = loss, 3 = draw, 6 = win

score_rules = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}

def RPS_results(player1, player2):
    p1 = actions[player1]
    p2 = actions[player2]

    player1_score = score_rules[p1]
    player2_score = score_rules[p2]

    if p1 == p2:
        # tie
        player1_score += 3
        player2_score += 3
    elif p1 == "rock" and p2 == "paper":
        # print("p2 wins")
        player1_score += 0
        player2_score += 6
    elif p1 == "paper" and p2 == "scissors":
        # print("p2 wins")
        player1_score += 0
        player2_score += 6
    elif p1 == "scissors" and p2 == "rock":
        # print("p2 wins")
        player1_score += 0
        player2_score += 6
    else:
        # print("p1 wins")
        player1_score += 6
        player2_score += 0

    return player1_score, player2_score

def optimal_move(player1, goal_result):
    decoded_actions = {
        "X": "lose",
        "Y": "tie",
        "Z": "win"
    }

    goal = decoded_actions[goal_result]

    if goal == "tie":
        return player1, player1

    # paper > rock > scissors > paper
    # B > A > C > B
    win = "BACBAC"
    index = win.index(player1)

    if goal == "win":
        player2 = win[index-1]
    else:
        player2 = win[index+1]

    return player1, player2


opponent_total = 0
your_total = 0

for match in data:
    opponent_move = match[0]
    your_move = match[2]
    win_goal = match[2]
    opponent_move, your_move = optimal_move(opponent_move, win_goal)

    opponent_score, your_score = RPS_results(opponent_move, your_move)

    opponent_total += opponent_score
    your_total += your_score

print(your_total)
print(opponent_total)