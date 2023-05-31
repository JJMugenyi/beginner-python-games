import random
import os
from sys import platform

# Clears command line
def clear():
    os.system("clear" if os.name == "posix" else "cls")

# Global Variables
n_decks = 6    # Standard casino's number
suit = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def new_cards():
    total = suit * 4 * n_decks
    return total

# Gets player's deposit
def deposit():
    while True:
        balance = input("How much would you like to deposit? $")
        if balance.isdigit() and int(balance) > 0:
            return int(balance)
        else:
            print("Invalid deposit amount. Please enter a positive number.")

# Gets player's bet amount
def get_bet(balance):
    while True:
        amount = input(f"How much would you like to bet? (Available balance: ${balance}) $")
        if amount.isdigit() and 0 < int(amount) <= balance:
            return int(amount)
        else:
            print("Invalid bet amount. Please enter a valid bet.")

# Draws card from the cards
def deal_card(cards):
    card = random.choice(cards)
    cards.remove(card)
    return card

# Calculates total hand
def calc_score(hand):
    if sum(hand) == 21 and len(hand) == 2:
        return 0
    if 11 in hand and sum(hand) > 21:
        hand.remove(11)
        hand.append(1)
    return sum(hand)

# Checks for winner
def check_winner(user_score, computer_score, balance, bet):
    if user_score > 21 and computer_score > 21:
        print("You lose, you went over. 😤")
        return balance - bet
    if user_score == computer_score:
        print("Draw 🙃")
        return balance
    elif computer_score == 0:
        print("You lose, dealer has Blackjack 😱")
        return balance - bet
    elif user_score == 0:
        print("You Win with a Blackjack 😎")
        return balance + int(bet * 1.5)
    elif user_score > 21:
        print("You lose, you went over 😭")
        return balance - bet
    elif computer_score > 21:
        print("You win, dealer went over 😁")
        return balance + bet
    elif user_score > computer_score:
        print("You win 😃")
        return balance + bet
    else:
        print("You lose 😤")
        return balance - bet

def play_game(balance, cards):
    user_cards = []
    computer_cards = []
    is_game_over = False

    if not cards:
        cards = new_cards()

    for _ in range(2):
        user_cards.append(deal_card(cards))
        computer_cards.append(deal_card(cards))
    
    while not is_game_over:
        user_score = calc_score(user_cards)
        computer_score = calc_score(computer_cards)
        print(f"\nYour cards: {user_cards}, current score: {user_score}")
        print(f"Dealer's card: [{computer_cards[0]}, _ ]")
    
        if user_score == 0 or computer_score == 0 or user_score > 21:
            is_game_over = True
        else:
            user_should_deal = input("\nType 'y' to get another card, type 'n' to pass: ")
            if user_should_deal.lower() == "y":
                user_cards.append(deal_card(cards))
            else:
                is_game_over = True
    
    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card(cards))
        computer_score = calc_score(computer_cards)
    
    print(f"\nYour final hand: {user_cards}, final score: {user_score}")
    print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
    return check_winner(user_score, computer_score, balance, bet)

clear()
balance = deposit()
cards = new_cards()
while True:
    if balance <= 0:
        print("\nYou've lost all of your money! 😭")
        input()
        quit()
    play = input("Press enter to play ('q' to quit)")
    clear()
    if play.lower() == "q":
        exit()
    print(f"Your current balance is ${balance}\n")
    bet = get_bet(balance)

    if len(cards) < 300:
        print("Time to shuffle the cards!")
        cards = new_cards()

    balance = play_game(balance, cards)
