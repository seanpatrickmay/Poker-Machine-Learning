#!/usr/bin/env python3
from PokerCard import PokerCard

class PokerPlayer:
    def __init__(self, numChips, pos):
        self.numChips = numChips
        self.hand = []
        self.handVisible = False
        self.pos = pos
        self.chipsInPot = 0
        self.won = False

    def takeBet(self, bet):
        if bet > self.numChips:
            holdChips = self.numChips
            self.chipsInPot += holdChips
            self.numChips = 0
            return holdChips
        else:
            self.numChips -= bet
            self.chipsInPot += bet
            return bet
        
    def receiveHand(self, hand):
        self.hand = hand.copy()

    def __str__(self):
        string = str(self.numChips)
        if self.handVisible:
            string += "\nHand: " + str(self.hand[0]) + " " + str(self.hand[1])
        return string
    
    def winsHand(self, pot):
        self.numChips += pot

    def handToString(self):
        return str(self.hand[0]) + str(self.hand[1])

    def action(self, gameState, actionHistory):
        bigBlind = gameState[0]
        pot = gameState[1]
        board = gameState[2]
        folded = gameState[3]
        if not len(actionHistory) == 0:
            prevAction = actionHistory[len(actionHistory) - 1]
        return "fold"
    
    def handToVals(self):
        handValsSorted = sorted([card.value for card in self.hand], reverse = True)
        return [[handValsSorted[0], self.hand[0].suit], [handValsSorted[1], self.hand[1].suit]]
    
    def handToLine(self):
        playerData = self.handToVals()
        playerSuited = playerData[0][1] == playerData[1][1]
        playerLine = playerData[0][0] * playerData[0][0] + playerData[1][0] * 2
        if playerSuited:
            playerLine += 1
        return playerLine