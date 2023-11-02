#!/usr/bin/env python3
import Deck
from collections import Counter
from itertools import groupby
from itertools import combinations
import sys

class HoldemPokerHand:
    def __init__(self, players, smallBlind, bigBlind):
        self.deck = Deck.Deck()
        self.pot = 0
        self.playersInHand = players
        self.smallBlind = smallBlind
        self.bigBlind = bigBlind
        self.board = []
        self.folded = []
        for player in self.playersInHand:
            self.folded.append(False)
        self.moneyInPot = []
        for player in self.playersInHand:
            self.moneyInPot.append(0)
        self.handWon = False
        self.gameState = [self.bigBlind, self.pot, self.board, self.folded, self.playersInHand]
    
    def updateGameState(self):
        self.gameState = [self.bigBlind, self.pot, self.board, self.folded, self.playersInHand]

    def collectBlinds(self):
        if len(self.playersInHand) > 2:
            self.moneyInPot[1] += self.playersInHand[1].takeBet(self.smallBlind)
            self.moneyInPot[2] += self.playersInHand[2].takeBet(self.bigBlind)
        else:
            self.moneyInPot[0] += self.playersInHand[0].takeBet(self.smallBlind)
            self.moneyInPot[1] += self.playersInHand[1].takeBet(self.bigBlind)
        self.pot = sum(self.moneyInPot)

    def dealCards(self):
        for num in range(len(self.playersInHand)):
            self.board = []
            currentHand = []
            currentHand.append(self.deck.pop())
            currentHand.append(self.deck.pop())
            self.playersInHand[num].receiveHand(currentHand)

    def boardToString(self):
        placeholder = ["   ", "   ", "   ", "   ", "   "]
        string = ""
        for card in range(len(self.board)):
            placeholder[card] = str(self.board[card])
        for card in placeholder:
            string += card + " "
        return string
    
    def burnACard(self):
        self.deck.pop()

    def flipACard(self):
        newBoard = self.board.copy()
        newBoard.append(self.deck.pop())
        self.board = newBoard

    def __str__(self):
        if len(self.playersInHand) == 3:
            string = "\n" + self.playerString(1) + "         " + self.playerString(2)
            string += "\n             " + self.boardToString() + "Pot: " + str(self.pot) + "\n"
            string += "          " + self.playerString(0) + "\n"
            return string
        
        if len(self.playersInHand) == 9:
            string = "\n" + self.playerString(3) + "        " + self.playerString(4) + "        " + self.playerString(5) + "        " + self.playerString(6) + "\n"
            string += "\n"
            string += self.playerString(2) + "        " + self.boardToString() + "Pot: " + str(self.pot) + "            " + self.playerString(7) + "\n"
            string += "\n"
            string += self.playerString(1) + "                                             " + self.playerString(8) + "\n"
            string += "                              " + self.playerString(0)
            return string
        
        if len(self.playersInHand) == 2:
            string = "\n    " + self.playerString(1) + "\n"
            string += "\n" + self.boardToString() + "Pot: " + str(self.pot) + "\n"
            string += "\n    " + self.playerString(0) + "\n"
            return string
    
    def flop(self):
        self.burnACard()
        self.flipACard()
        self.flipACard()
        self.flipACard()

    def turn(self):
        self.burnACard()
        self.flipACard()

    def river(self):
        self.burnACard()
        self.flipACard()

    def getAction(self, bet):
        actionHistory = []
        numInHand = len(self.playersInHand)
        preFlop = False
        actionCount = 0
        moneyInAction = []
        for player in self.playersInHand:
            moneyInAction.append(0)
        if (bet > 0):
            currentAction = 3
            moneyInAction = self.moneyInPot.copy()
        else:
            currentAction = 1
        if numInHand == 2:
            currentAction = 0
        currentBet = bet
        while(actionCount < numInHand):
            #if all folded, win
            if self.folded.count(False) == 1:
                self.handWon = True
                break
            currentAction = currentAction % numInHand
            #if folded, skip
            if self.folded[currentAction] == True:
                currentAction += 1
                actionCount += 1
                continue
            #if all in or broke, skip
            if self.playersInHand[currentAction].numChips == 0:
                currentAction += 1
                actionCount += 1
                continue
            self.updateGameState()
            #print(self)
            playerAction = self.playersInHand[currentAction].action(self.gameState, actionHistory)
            if "bet" in playerAction.split(" "):
                actionHistory.append([currentAction, "bet", int(playerAction.split(" ")[1])])
                if int(playerAction.split()[1]) < currentBet + self.bigBlind:
                    print("Raise must be at least 1 BB")
                    continue
                actionCount = 1
                topBet = int(playerAction.split()[1])
                currentBet = self.playersInHand[currentAction].takeBet(int(playerAction.split()[1]) - moneyInAction[currentAction])
                self.moneyInPot[currentAction] += currentBet
                moneyInAction[currentAction] += currentBet
                currentAction += 1
                self.pot = sum(self.moneyInPot)
            elif "call" == playerAction:
                if currentBet == moneyInAction[currentAction]:
                    print("You already have called. Check instead.")
                    continue
                actionHistory.append([currentAction, "call", currentBet])
                actionCount += 1
                holdCall = self.playersInHand[currentAction].takeBet(currentBet - moneyInAction[currentAction])
                self.moneyInPot[currentAction] += holdCall
                moneyInAction[currentAction] += holdCall
                currentAction += 1
                self.pot = sum(self.moneyInPot)
            elif "check" == playerAction:
                if currentBet > moneyInAction[currentAction]:
                    print("Cannot check. You must fold, call, or raise")
                    continue
                actionHistory.append([currentAction, "check", currentBet])
                actionCount += 1
                currentAction += 1
            elif "fold" == playerAction:
                if currentBet == moneyInAction[currentAction]:
                    print("Just check bro")
                    continue
                actionHistory.append([currentAction, "fold", currentBet])
                actionCount += 1
                self.folded[currentAction] = True
                currentAction += 1
            else:
                print(playerAction, "is invalid input, try again:")
                print("bet x, call, check, fold")

    def collectWinnersChips(self, winners):
        chipsWon = []
        for players in winners:
            if len(players) == 1:
                player = players[0]
                amtWon = self.getPlayerChipsFromPot(player)
                chipsWon += [[player, amtWon]]
            else:
                smallestInPot = sys.maxsize
                smallestPlayers = []
                for player in players:
                    playerIndex = self.playersInHand.index(player)
                    if self.moneyInPot[playerIndex] < smallestInPot:
                        smallestInPot = self.moneyInPot[playerIndex]
                        smallestPlayers.clear()
                        smallestPlayers.append(player)
                    elif self.moneyInPot[playerIndex] == smallestInPot:
                        smallestPlayers.append(player)
                if len(smallestPlayers) == 1:
                    smallest = smallestPlayers[0]
                    amtWon = self.getPlayerChipsFromPot(smallest)


    def getPlayerChipsFromPot(self, player):
        playerIndex = self.playersInHand.index(player)
        amtWon = 0
        amtInPot = self.moneyInPot[playerIndex]
        for amt in self.moneyInPot:
            if amt == 0:
                continue
            if amtInPot >= amt:
                amtWon += amt
                amt = 0
            else:
                amtWon += amtInPot
                amt -= amtInPot
        return amtWon

    def getShowdownWinners(self):
        stillInIndices = []
        for int in range(len(self.folded)):
            if not self.folded[int]:
                stillInIndices.append(int)
        showDownPlayers = []
        for index in stillInIndices:
            showDownPlayers.append(self.playersInHand[index])
        winners = []
        for player in showDownPlayers:
            if len(winners) == 0:
                winners.append(player)
            else:
                for winner in winners:
                    winnersCopy = winners.copy()
                    compareVal = self.compareHands(winner, player)
                    if compareVal == 0:
                        winnersCopy.append(player)
                    elif compareVal < 0:
                        winnersCopy.clear()
                        winnersCopy.append(player)
                winners = winnersCopy
        amountWon = self.pot // len(winners)
        remainingChips = self.pot - amountWon * len(winners)
        firstWinner = True
        for winner in winners:
            winPos = self.playersInHand.index(winner)
            if firstWinner:
                winner.winsHand(remainingChips + amountWon)
                firstWinner = False
                #print("The " + self.positionToString(winPos) + " has won the hand with " + str(winner.hand[0]) + " " + str(winner.hand[1]) + "!"
                    #  + "\nTheir new chip total after winning " + str(remainingChips + amountWon - self.moneyInPot[winPos]) + " chips is: " + str(winner.numChips))
            else:
                winner.winsHand(amountWon)
                #print("The " + self.positionToString(winPos) + " has won the hand with " + str(winner.hand[0]) + " " + str(winner.hand[1]) + "!"
                    #  + "\nTheir new chip total after winning " + str(amountWon - self.moneyInPot[winPos]) + " chips is: " + str(winner.numChips))
                    
    def compareHands(self, player1, player2):
        player1Best = self.getBestHandDemonination(player1.hand + self.board)
        player2Best = self.getBestHandDemonination(player2.hand + self.board)
        if player1Best[0] > player2Best[0]:
            return 1
        elif player1Best[0] < player2Best[0]:
            return -1
        else:
            result = self.compareSameDenomHands(player1Best[1], player2Best[1], player1Best[0])
            if result > 0:
                return 1
            elif result < 0:
                return -1
            return 0

    def getBestHandDemonination(self, hand):
        possibleHands = combinations(hand, 5)
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
        hand1 = sorted(hand1, key=lambda card: card.value)
        hand2 = sorted(hand2, key=lambda card: card.value)
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

    def endHandFolded(self, player):
        self.playersInHand[player].winsHand(self.pot)
        #print("\nThe " + self.positionToString(player) + " has won the hand!"
            #  + "\nTheir new chip total after winning " + str(self.pot - self.moneyInPot[player]) + " chips is: " + str(self.playersInHand[player].numChips))

    def positionToString(self, position):
        if position == 0:
                return "Button"
        if len(self.playersInHand) == 2:
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
            
    def playerString(self, position):
        return self.positionToString(position) + " - " + str(self.playersInHand[position])


    def run(self):
        self.collectBlinds()
        self.dealCards()
        self.getAction(self.bigBlind) #PREFLOP ACTION
        if self.handWon == False:
            self.flop()
            self.getAction(0) #FLOP ACTION
            if self.handWon == False:
                self.turn()
                self.getAction(0) #TURN ACTION
                if self.handWon == False:
                    self.river()
                    self.getAction(0) #RIVER ACTION
                    if self.handWon == False:
                        self.getShowdownWinners()
                    else:
                        self.endHandFolded(self.folded.index(False))
                else:
                    self.endHandFolded(self.folded.index(False))
            else:
                self.endHandFolded(self.folded.index(False))
        else:
            self.endHandFolded(self.folded.index(False))
        return self.playersInHand