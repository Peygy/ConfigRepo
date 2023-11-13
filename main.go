package main

import "fmt"

func ParseCard(card string) int {
    switch card {
    case "ace": return 11
    case "two": return 2
    case "three": return 3
    case "four": return 4
    case "five": return 5
    case "six": return 6
    case "seven": return 7
    case "eight": return 8
    case "nine": return 9
    case "ten", "jack", "queen", "king": return 10
    default: return 0
    }
	panic("Please implement the ParseCard function")
}

// FirstTurn returns the decision for the first turn, given two cards of the
// player and one card of the dealer.
func FirstTurn(card1, card2, dealerCard string) string {
    num1 := ParseCard(card1)
    num2 := ParseCard(card2)
	numD := ParseCard(dealerCard)
    
    switch {
    case card1 == "ace" && card2 == "ace": return "P"
    case num1 + num2 == 21 && numD == 0: return "W"
    case num1 + num2 == 21 && numD > 0: return "S"
    case num1 + num2 >= 17 && num1 + num2 <= 20: return "S"
    case num1 + num2 >= 12 && num1 + num2 <= 16:
    	if numD < 7 {
            return "S"
        }
    	return "H"
    case num1 + num2 <= 11: return "H"
    default: return "S"
    }
	panic("Please implement the FirstTurn function")
}

func main() {
    fmt.Print(FirstTurn("ace", "king", "nine"));
}