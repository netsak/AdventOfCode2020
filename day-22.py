#!/usr/bin/env python
from collections import deque


def load_players(filename):
    ret = list()
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith("Player"):
                ret.append(deque())
            elif line != "\n":
                ret[-1].insert(0, int(line))
        return ret


def play_game(players):
    while True:
        for i,p in enumerate(players):
            print(f"Player {i}'s deck: {p}")
        cards = [p.pop() for p in players]
        for i,c in enumerate(cards):
            print(f"Player {i} plays: {c}")
        if cards[0] > cards[1]:
            print("Player 1 wins the round!")
            players[0].insert(0, cards[0])
            players[0].insert(0, cards[1])
        else:
            print("Player 2 wins the round!")
            players[1].insert(0, cards[1])
            players[1].insert(0, cards[0])
        if any(len(p) == 0 for p in players):
            if cards[0] > cards[1]:
                return players[0]
            else:
                return players[1]


def get_score(deck):
    score = sum((i+1)*v for i,v in enumerate(deck))
    print(f"The winner's score is {score}")
    return score


if __name__ == "__main__":
    print("======================================= Part 1 - Example 1 =========================================")
    players = load_players("data/day-22-example1.txt")
    # print(players)
    assert players == [deque([1, 3, 6, 2, 9]), deque([10, 7, 4, 8, 5])]
    winner = play_game(players)
    # print(winner)
    assert winner == deque([1, 7, 4, 9, 5, 8, 6, 10, 2, 3])
    score = get_score(winner)
    assert score == 306
    # print("======================================= Part 2 - Example 1 =========================================")
    print("======================================= Part 1 - Real Puzzle =======================================")
    players = load_players("data/day-22.txt")
    winner = play_game(players)
    score = get_score(winner)
    assert score == 32815
    # print("======================================= Part 2 - Real Puzzle =======================================")    
