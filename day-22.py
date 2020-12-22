#!/usr/bin/env python
from collections import deque
from copy import deepcopy


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
        winner, looser = (0,1) if cards[0] > cards[1] else (1,0)
        print(f"Player {winner+1} wins the round!")
        players[winner].insert(0, cards[winner])
        players[winner].insert(0, cards[looser])
        if any(len(p) == 0 for p in players):
            return players[winner], winner+1


def get_score(deck):
    score = sum((i+1)*v for i,v in enumerate(deck))
    print(f"The winner's score is {score}")
    return score


def play_game_recursive(players, level=0):
    previous = set()
    while True:
        for i,p in enumerate(players):
            print(f"Player {i+1}'s deck: {p}")
        configuration = tuple(tuple(c for c in p) for p in players)
        if configuration in previous:
            return None, 1
        previous.add(configuration)
        cards = [p.pop() for p in players]
        if cards[0]<=len(players[0]) and len(players[1])>=cards[1]:
            print("Playing a sub-game to determine the winner...")
            new_deck = deepcopy(players)
            while len(new_deck[0]) > cards[0]:
                new_deck[0].popleft()
            while len(new_deck[1]) > cards[1]:
                new_deck[1].popleft()
            regular, winner = play_game_recursive(new_deck, level+1)
            print(f"Sub-came won by player {winner}: {regular}")
            winner = winner - 1
            looser = 0 if winner == 1 else 1
        else:
            winner, looser = (0,1) if cards[0] > cards[1] else (1,0)
        print(f"Player {winner+1} wins the round!")
        players[winner].insert(0, cards[winner])
        players[winner].insert(0, cards[looser])
        if any(len(p) == 0 for p in players):
            return players[winner], winner+1


if __name__ == "__main__":
    print("======================================= Part 1 - Example 1 =========================================")
    players = load_players("data/day-22-example1.txt")
    assert players == [deque([1, 3, 6, 2, 9]), deque([10, 7, 4, 8, 5])]
    deck, winner = play_game(players)
    assert winner == 2
    assert deck == deque([1, 7, 4, 9, 5, 8, 6, 10, 2, 3])
    score = get_score(deck)
    assert score == 306
    print("======================================= Part 2 - Example 1 =========================================")
    players = load_players("data/day-22-example1.txt")
    deck, winner = play_game_recursive(players)
    assert winner == 2
    assert deck == deque([3, 9, 8, 10, 1, 4, 2, 6, 5, 7])
    score = get_score(deck)
    assert score == 291
    print("======================================= Part 1 - Real Puzzle =======================================")
    players = load_players("data/day-22.txt")
    deck, winner = play_game(players)
    assert winner == 2
    score = get_score(deck)
    assert score == 32815
    print("======================================= Part 2 - Real Puzzle =======================================")    
    players = load_players("data/day-22.txt")
    deck, winner = play_game_recursive(players)
    score = get_score(deck)
    assert score > 4674
    assert score > 5541
    assert score == 30695
    assert winner == 2

