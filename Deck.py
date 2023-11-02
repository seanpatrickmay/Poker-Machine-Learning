#!/usr/bin/env python3
import PokerCard
import random

class Deck:
    def __init__(self):
        makeDeck = []
        for value in range(13):
            for suit in range(4):
                makeDeck += [PokerCard.PokerCard(value, suit)]
        random.shuffle(makeDeck)
        self.deck = makeDeck

    def pop(self):
        return self.deck.pop()
    
    def __str__(self):
        listStrCards = []
        for card in self.deck:
            listStrCards += [str(card)]
        return str(listStrCards)