#!/usr/bin/env python3
import PokerPlayer

class HumanPokerPlayer(PokerPlayer.PokerPlayer):

    def action(self, gameState, actionHistory):
        bigBlind = gameState[0]
        pot = gameState[1]
        board = gameState[2]
        folded = gameState[3]
        stringPrev = ""
        if not len(actionHistory) == 0:
            prevAction = actionHistory[len(actionHistory) - 1]
            if prevAction[1] == "bet":
                stringPrev = "Player before you bet " + str(prevAction[2]) + " chips."
            if prevAction[1] == "call":
                stringPrev = "Player before you called a bet of " + str(prevAction[2]) + " chips."
            if prevAction[1] == "check":
                stringPrev = "Player before you checked."
        return input("\nYour hand is: " + str(self.hand[0]) + " " + str(self.hand[1]) 
                     + "\nYour chip count is: " + str(self.numChips)
                     + "\n" + stringPrev
                     + " \nAction please.\n")
    
    def name(self):
        return "Human Player"
    
    