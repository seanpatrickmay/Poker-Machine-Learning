#!/usr/bin/env python3

from PokerPlayer import PokerPlayer
from collections import Counter
from itertools import groupby
from itertools import combinations

class BadRobotPokerPlayer(PokerPlayer):
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
        print("Getting action from badRobot at", self.positionToString(self.pos))
        #print("Hand is:", str(self.hand[0]), str(self.hand[1]))
        self.handVals = sorted([card.value for card in self.hand], reverse = True)
        self.handValsCounter = Counter(self.handVals)
        bigBlind = int(gameState[0])
        pot = int(gameState[1])
        board = gameState[2]
        folded = gameState[3]
        players = gameState[4]
        self.players = players.copy()
        currentBet = 0
        selfChipsInAction = 0
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
        print("The current bet is:", currentBet)
        print("The last action was:", lastAction)
        
        #PREFLOP
        if (self.gameStage == 0):
            #IF FIRST TO ACT
            if lastAction == "nothing":
                #IF HAND HAS HIGH CARD OR POCKET PAIR
                if self.handHasPairOrHighCard():
                    print("Betting", str(bigBlind * 3))
                    return "bet " + str(bigBlind * 3)
                else:
                    print("Folding preflop")
                    return "fold"
            #SECOND TO ACT
            elif lastAction == "bet":
                #3-BET WITH POCKET PAIR
                if 2 in self.handValsCounter.values():
                    print("3-Betting", str(3 * currentBet))
                    return "bet " + str(3 * currentBet)
                elif self.handHasPairOrHighCard():
                    print("Calling", str(currentBet), "preflop")
                    return "call"
                else:
                    print("Folding to a raise preflop")
                    return "fold"
            elif lastAction == "call":
                if self.handHasPairOrHighCard():
                    print("Raising", str(3 * bigBlind), "against a limper")
                    return "bet " + str(3 * bigBlind)
                else:
                    print("Checking it down preflop")
                    return "check"

        #POST FLOP
        if self.gameStage == 1:
            self.handAndBoard = self.hand + board
            self.handAndBoardVals = sorted([card.value for card in self.handAndBoard], reverse = True)
            self.handAndBoardValsCounter = Counter(self.handAndBoardVals)
            handDenom = self.getBestHandDemonination()[0]
            self.denom = handDenom
            #IF FIRST TO ACT
            if lastAction == "nothing":
                #IF HAND IS BETTER THAN NOTHING
                if handDenom > 1 or 12 in self.handVals:
                    print("Betting", str(pot//2), "post flop")
                    return "bet " + str(pot//2)
                else:
                    print("Checking first to act post flop")
                    return "check"
            #CHECKED TO
            elif lastAction == "check":
                if handDenom > 1 or 12 in self.handVals or 11 in self.handVals:
                    print("Betting", str(pot//2), "post flop")
                    return "bet " + str(pot//2)
                else:
                    print("Checking it down post flop")
                    return "check"
            #BET TO
            elif lastAction == "bet":
                if handDenom > 2:
                    print("Re-Raising", str(currentBet * 3), "post flop")
                    return "bet " + str(currentBet * 3)
                if handDenom > 1 or 12 in self.handVals:
                    print("Calling", currentBet, "post flop")
                    return "call"
                else:
                    print("Folding to a bet post flop")
                    return "fold"

        #TURN
        if self.gameStage == 2:
            self.handAndBoard = self.hand + board
            self.handAndBoardVals = sorted([card.value for card in self.handAndBoard], reverse = True)
            self.handAndBoardValsCounter = Counter(self.handAndBoardVals)
            handDenom = self.getBestHandDemonination()[0]
            self.denom = handDenom
            #IF FIRST TO ACT
            if lastAction == "nothing":
                #IF HAND IS BETTER THAN NOTHING
                if handDenom > 2:
                    print("Betting", str(pot//2), "on the turn")
                    return "bet " + str(pot//2)
                else:
                    print("Checking first to act on the turn")
                    return "check"
            #CHECKED TO
            elif lastAction == "check":
                if handDenom > 1:
                    print("Betting", str(pot//2), "on the turn")
                    return "bet " + str(pot//2)
                else:
                    print("Checking down the turn")
                    return "check"
            #BET TO
            elif lastAction == "bet":
                if handDenom > 2:
                    print("Re-Raising", str(currentBet * 3), "turn")
                    return "bet " + str(currentBet * 3)
                if handDenom > 1 or 12 in self.handVals:
                    print("Calling", currentBet, "turn")
                    return "call"
                else:
                    print("Folding to a turn bet")
                    return "fold"

        #RIVER
        if self.gameStage == 3:
            self.handAndBoard = self.hand + board
            self.handAndBoardVals = sorted([card.value for card in self.handAndBoard], reverse = True)
            self.handAndBoardValsCounter = Counter(self.handAndBoardVals)
            handDenom = self.getBestHandDemonination()[0]
            self.denom = handDenom
            #IF FIRST TO ACT
            if lastAction == "nothing":
                #IF HAND IS BETTER THAN NOTHING
                if handDenom > 2:
                    print("Betting", str(pot//2), "on the river")
                    return "bet " + str(pot//2)
                else:
                    print("Checking first to act on the river")
                    return "check"
            #CHECKED TO
            elif lastAction == "check":
                if handDenom > 1:
                    print("Betting", str(pot//2), "on the river")
                    return "bet " + str(pot//2)
                else:
                    print("Checking it down to showdown")
                    return "check"
            #BET TO
            elif lastAction == "bet":
                if handDenom > 3:
                    print("Re-Raising", str(currentBet * 3), "on the river")
                    return "bet " + str(currentBet * 3)
                if handDenom > 1:
                    print("Calling", currentBet, "on the river")
                    return "call"
                else:
                    print("Folding to a bet on the river")
                    return "fold"
    
    def handHasPairOrHighCard(self):
        return 12 in self.handVals or 11 in self.handVals or 10 in self.handVals or 2 in self.handValsCounter.values()
    
    def name(self):
        return "BadRobot"
    
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
    
    def getBestHandDemonination(self):
        possibleHands = combinations(self.handAndBoard, 5)
        bestHand = []
        bestDemonination = 0
        for unsortedHand in possibleHands:
            thisHand = list(unsortedHand)
            thisHand.sort(key = lambda x: x.value, reverse=True)
            handValues = sorted([card.value for card in thisHand])
            valueCounter = Counter(handValues)
            valueCounterCounter = Counter(valueCounter.values())
            handSuits = sorted([card.suit for card in thisHand])
            suitCounter = Counter(handSuits)
            #High Card
            denomination = 1
            #Pair
            if 2 in valueCounter.values():
                denomination = 2
                #Two Pair
                if 2 in valueCounterCounter.values():
                    denomination = 3
            #Set/Trips
            if 3 in valueCounter.values():
                denomination = 4
                #Full House
                if 2 in valueCounter.values():
                    denomination = 7
            #Straight
            valueRuns = groupby
            straight = False
            for key, grouper in groupby(enumerate(handValues), lambda x : x[0] - x[1]):
                myVal = []
                for group in grouper:
                    myVal.append(group)
                if len(myVal) == 5:
                    if 5 > denomination:
                        denomination = 5
                        #Straight Flush
                        if 5 in suitCounter.values():
                            denomination = 9
            #Flush
            if 5 in suitCounter.values():
                if 6 > denomination:
                    denomination = 6
            #Quads
            if 4 in valueCounter.values():
                if 8 > denomination:
                    denomination = 8
            if denomination > bestDemonination:
                bestDemonination = denomination
                bestHand = thisHand
            elif denomination == bestDemonination:
                compareVal = self.compareSameDenomHands(thisHand, bestHand, denomination)
                if compareVal > 0:
                    bestHand = thisHand
        return [bestDemonination, bestHand]

    # 0 for tie, 1 for hand1, -1 for hand2    
    def compareSameDenomHands(self, hand1, hand2, denom):
        hand1Values = sorted([card.value for card in hand1], reverse = True)
        hand2Values = sorted([card.value for card in hand2], reverse = True)
        hand1ValCounter = Counter(hand1Values)
        hand2ValCounter = Counter(hand2Values)
        revHand1ValCounter = {v: k for k, v in hand1ValCounter.items()}
        revHand2ValCounter = {v: k for k, v in hand2ValCounter.items()}
        #High Card
        if denom == 1:
            return self.compareHighCards(hand1, hand2)
        #Pair
        elif denom == 2:
            return self.comparePairs(hand1, hand2)
        #Two Pair
        elif denom == 3:
            return self.compareTwoPairs(hand1, hand2)
        elif denom == 4:
            return self.compareTrips(hand1, hand2)
        elif denom == 5:
            return self.compareStraights(hand1, hand2)
        elif denom == 6:
            return self.compareHighCards(hand1, hand2)
        elif denom == 7:
            return self.compareFullHouses(hand1, hand2)
        elif denom == 8:
            return self.compareQuads(hand1, hand2)
        elif denom == 9:
            return self.compareFlush(hand1, hand2)
        
    def compareHighCards(self, hand1, hand2):
        for card in range(5):
            if hand1[card].value > hand2[card].value:
                return 1
            elif hand1[card].value < hand2[card].value:
                return -1
        return 0
    
    def compareFlush(self, hand1, hand2):
        for card in range(5):
            print("card1val", hand1[card].value)
            print("card2val", hand2[card].value)
            if hand1[card].value > hand2[card].value:
                return 1
            elif hand1[card].value < hand2[card].value:
                return -1
        return 0
    
    def comparePairs(self, hand1, hand2):
        hand1Values = sorted([card.value for card in hand1], reverse = True)
        hand2Values = sorted([card.value for card in hand2], reverse = True)
        hand1ValCounter = Counter(hand1Values)
        hand2ValCounter = Counter(hand2Values)
        revHand1ValCounter = {v: k for k, v in hand1ValCounter.items()}
        revHand2ValCounter = {v: k for k, v in hand2ValCounter.items()}
        if revHand1ValCounter.get(2) > revHand2ValCounter.get(2):
            return 1
        elif revHand1ValCounter.get(2) < revHand2ValCounter.get(2):
            return -1
        return self.compareHighCards(hand1, hand2)
    
    def compareTwoPairs(self, hand1, hand2):
        hand1Values = sorted([card.value for card in hand1], reverse = True)
        hand2Values = sorted([card.value for card in hand2], reverse = True)
        hand1ValCounter = Counter(hand1Values)
        hand2ValCounter = Counter(hand2Values)
        hand1Pairs = []
        for key in hand1ValCounter:
            if hand1ValCounter.get(key) == 2:
                hand1Pairs.append(key)
        hand2Pairs = []
        for key in hand2ValCounter:
            if hand2ValCounter.get(key) == 2:
                hand2Pairs.append(key)
        for card in range(2):
            if hand1Pairs[card] > hand2Pairs[card]:
                return 1
            elif hand1Pairs[card] < hand2Pairs[card]:
                return -1
        return self.compareHighCards(hand1, hand2)
    
    def compareTrips(self, hand1, hand2):
        hand1Values = sorted([card.value for card in hand1], reverse = True)
        hand2Values = sorted([card.value for card in hand2], reverse = True)
        hand1ValCounter = Counter(hand1Values)
        hand2ValCounter = Counter(hand2Values)
        revHand1ValCounter = {v: k for k, v in hand1ValCounter.items()}
        revHand2ValCounter = {v: k for k, v in hand2ValCounter.items()}
        if revHand1ValCounter.get(3) > revHand2ValCounter.get(3):
            return 1
        elif revHand1ValCounter.get(3) < revHand2ValCounter.get(3):
            return -1
        return self.compareHighCards(hand1, hand2)
    
    def compareStraights(self, hand1, hand2):
        if hand1[0].value > hand2[0].value:
            return 1
        elif hand1[0].value > hand2[0].value:
            return -1
        return 0
    
    def compareFullHouses(self, hand1, hand2):
        hand1Values = sorted([card.value for card in hand1], reverse = True)
        hand2Values = sorted([card.value for card in hand2], reverse = True)
        hand1ValCounter = Counter(hand1Values)
        hand2ValCounter = Counter(hand2Values)
        revHand1ValCounter = {v: k for k, v in hand1ValCounter.items()}
        revHand2ValCounter = {v: k for k, v in hand2ValCounter.items()}
        if revHand1ValCounter.get(3) > revHand2ValCounter.get(3):
            return 1
        elif revHand1ValCounter.get(3) < revHand2ValCounter.get(3):
            return -1
        return self.comparePairs(hand1, hand2)
    
    def compareQuads(self, hand1, hand2):
        hand1Values = sorted([card.value for card in hand1], reverse = True)
        hand2Values = sorted([card.value for card in hand2], reverse = True)
        hand1ValCounter = Counter(hand1Values)
        hand2ValCounter = Counter(hand2Values)
        revHand1ValCounter = {v: k for k, v in hand1ValCounter.items()}
        revHand2ValCounter = {v: k for k, v in hand2ValCounter.items()}
        if revHand1ValCounter.get(4) > revHand2ValCounter.get(4):
            return 1
        elif revHand1ValCounter.get(4) < revHand2ValCounter.get(4):
            return -1
        return self.compareHighCards(hand1, hand2)

