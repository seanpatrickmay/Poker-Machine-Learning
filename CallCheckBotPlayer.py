#!/usr/bin/env python3

from PokerPlayer import PokerPlayer
from collections import Counter
from itertools import groupby
from itertools import combinations

class CallCheckBotPlayer(PokerPlayer):
    def __init__(self, numChips, pos):
        super().__init__(numChips, pos)
        #GAME STATES:
        #0,   1,    2,    3
        #Pre, Flop, Turn, River
        self.gameStage = 0
        self.firstAction = True
        self.handVals = []
        self.handValsCounter = []
        self.handAndBoard = []
        self.handAndBoardVals = []
        self.handAndBoardValsCounter = []
        self.players = []
        self.denom = 0

    def action(self, gameState, actionHistory):
        #print("Getting action from checkBot at", self.positionToString(self.pos))
        #print("Hand is:", str(self.hand[0]), str(self.hand[1]))
        bigBlind = int(gameState[0])
        board = gameState[2]
        players = gameState[4]
        self.players = players.copy()
        currentBet = 0
        if (len(board)) == 0:
            self.gameStage = 0
        if len(board) == 3:
            self.gameStage = 1
        elif len(board) == 4:
            self.gameStage = 2
        elif len(board) == 5:
            self.gameStage = 3
        lastAction = "nothing"
        if self.gameStage == 0:
            currentBet = bigBlind
        if len(actionHistory) != 0:
            lastAction = actionHistory[len(actionHistory) - 1][1]
            currentBet = actionHistory[len(actionHistory) - 1][2]
        #print("The current bet is:", currentBet)
        #print("The last action was:", lastAction)
        
        #PREFLOP
        if (self.gameStage == 0):
            #IF FIRST TO ACT
            if lastAction == "nothing":
                #print("calling pre-flop")
                return ("call")
            #SECOND TO ACT
            elif lastAction == "bet":
                #3-BET WITH POCKET PAIR
                #print("Calling", str(currentBet), "preflop")
                return "call"
            elif lastAction == "call":
                #print("Checking it down preflop")
                return "check"

        #POST FLOP
        if self.gameStage != 0:
            #IF FIRST TO ACT
            if lastAction == "nothing":
                #IF HAND IS BETTER THAN NOTHING
                #print("Checking first to act post flop")
                return "check"
            #CHECKED TO
            elif lastAction == "check":
                #print("Checking it down post flop")
                return "check"
            #BET TO
            elif lastAction == "bet":
                #print("Calling", currentBet, "post flop")
                return "call"
            
    def name(self):
        return "CheckBot"
    
    def positionToString(self, position):
        if position == 0:
                return "Button"
        if len(self.players) == 2:
            if position == 1:
                return "Big Blind"
        else:
            if position == 1:
                return "Small Blind"
            if position == 2:
                return "Big Blind"
            if position == len(self.playersInHand) - 1:
                return "Cut Off"
            if position == len(self.playersInHand) - 2:
                return "HiJack"
            if position == len(self.playersInHand) - 3:
                return "LoJack"
            if position == len(self.playersInHand) - 4:
                return "UTG"
            if position == len(self.playersInHand) - 5:
                return "UTG + 1"
            if position == len(self.playersInHand) - 6:
                return "UTG + 2"