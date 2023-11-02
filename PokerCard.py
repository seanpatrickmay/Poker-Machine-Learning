#!/usr/bin/env python3

class PokerCard:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        string = ""
        if self.value == 8:
            string += "10"
        elif self.value == 9:
            string += " J"
        elif self.value == 10:
            string += " Q"
        elif self.value == 11:
            string += " K"
        elif self.value == 12:
            string += " A"
        else:
            string += " " + str(self.value + 2)
        if self.suit == 0:
            string += "♡"
        elif self.suit == 1:
            string += "♢"
        elif self.suit == 2:
            string += "♠"
        elif self.suit == 3:
            string += "♣"
        return string

    