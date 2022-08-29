from pickle import FALSE, TRUE
from random import randint, choice
import sys as system


# setup global variables

suits = ('Hearts','Clubs','Diamonds','Spades')

pip = ('Ace','King','Queen','Jack','Ten','Nine','Eight','Seven','Six','Five','Four','Three','Two')

card_val = {'Ace' : (1,11),
            'King': 10, 'Queen': 10, 'Jack': 10, 'Ten':10,
            'Nine':9, 'Eight':8, 'Seven':7, 'Six':6, 'Five':5, 'Four':4, 'Three':3, 'Two':2}


# core functions nested

def playBJ():
    winner = []
    card_history = []
    player_score = []
    pc_score = []
    pip_values = []
    count = 0
    hidden_card = []
    hidden_status = TRUE
    pc_bust_checker = 0

    def createCard():
        nonlocal pip_values 

        pip_val = choice(pip)
        suits_val = choice(suits)


        conc_cards = lambda a,b: pip_val + ' of ' + suits_val
        pip_values.append(pip_val)

        return conc_cards(pip_val,suits_val)


    def logHistory():
        nonlocal card_history, count, pip_values

        # card #1
        player_card1 = createCard()
        card_history.append(player_card1)

        # card #2
        computer_card1 = createCard()
        while computer_card1 in card_history:
            del pip_values[-1]
            computer_card1 = createCard()
        card_history.append(computer_card1)

        #card #3
        player_card2 = createCard()
        while player_card2 in card_history: 
            del pip_values[-1]
            player_card2 = createCard()
        card_history.append(player_card2)

        #card #4
        computer_card2 = createCard()
        while computer_card2 in card_history:
            del pip_values[-1]
            computer_card2 = createCard()
        card_history.append(computer_card2)

        return card_history

    def addCard(player_id):
        nonlocal card_history, count, pip_values, player_score, pc_score

        if player_id == 'player':
            newCard = createCard() 

            while newCard in card_history:
                del pip_values[-1]
                newCard = createCard()
            
            player_score.append(card_val[pip_values[-1]])
            card_history.append(newCard)
        elif player_id == 'pc':
            newCard = createCard() 

            while newCard in card_history:
                del pip_values[-1]
                newCard = createCard()
            
            pc_score.append(card_val[pip_values[-1]])
            card_history.append(newCard)

        return card_history

    def computeVal():
        nonlocal card_history, count, player_score, pc_score, pip_values, hidden_card
        check_BJ_pc = FALSE
        check_BJ_user = FALSE
        
        for i in range(count,len(card_history)):
            if (i % 2) == 0:
                player_score.append(card_val[pip_values[i]])
                print(f"You have been dealt a {card_history[i]} faced up!")
                if (card_val[pip_values[i]] == (1,11)) and (card_val[pip_values[count]] == 10): check_BJ_user = TRUE
                elif (card_val[pip_values[i]] == 10) and (card_val[pip_values[count]] == (1,11)): check_BJ_user = TRUE
            else:
                pc_score.append(card_val[pip_values[i]])
                if (i != len(card_history)-1): 
                    print(f"The house has revealed a {card_history[i]}")
                    if (card_val[pip_values[i]] == (1,11)) and (card_val[pip_values[-1]] == 10): check_BJ_pc = TRUE
                    elif (card_val[pip_values[i]] == 10) and (card_val[pip_values[-1]] == (1,11)): check_BJ_pc = TRUE
                else: 
                    hidden_card.append(card_history[-1])
                    print("The dealer puts their 2nd card faced down. All cards have now been dealt. \n")
                    if (check_BJ_pc == TRUE) and (check_BJ_user != TRUE): 
                        print(pc_score)
                        print('Blackjack! Computer Wins')
                        system.exit()
        
        print(f"Here are your card values: {player_score}")
        # print(pc_score)
        # print(pip_values)

        count += len(card_history)
        # print(count)

        return count

    def checkState():
        nonlocal player_score, pc_score, pc_bust_checker 

        while hidden_status == TRUE: 
            # check for naturals first
            for i in range(0,len(player_score)):
                if player_score[i] == (1,11):
                    ace_val = input("Would you like Ace to be valued as a 1 or 11? ")
                    player_score[i] = int(ace_val)
                    print(player_score)

            # if player decides to keep hitting
            if sum(list(player_score)) <= 21:
                if (sum(list(player_score)) == 21): 
                    print(f"Blackjack! {username} wins!")
                    system.exit() 
                else:
                    print("Nobody got 21 (boo)!")
                    playerActions()
            else: 
                print("Over 21! You lose")
                system.exit()

        while hidden_status == FALSE: 
            # ace condition
            for i in range(0,len(pc_score)):
                if pc_score[i] == (1,11):
                    if (int(pc_score[i]) + pc_bust_checker) >= 17:
                        pc_score[i] = 11 
                    else: pc_score[i] = 1 

            if sum(list(pc_score)) <= 21:
                if (sum(list(pc_score)) == 21): 
                    print(f"Blackjack! Computer wins!")
                    system.exit() 
                elif (sum(list(pc_score)) <= 16):
                    print("The computer takes another card.")
                    addCard('pc')
                    print(pc_score)
                    pc_bust_checker = sum(list(pc_score))
                    checkState()
                else: 
                    announceWinners()
                    break
            else: 
                print("Computer's over 21 and busted! You win!")
                system.exit()

        return 

    def playerActions():
        # future features to inlcude (1) splitting pairs (2) doubling down and (3) insurance
    
        player_action = input("Would you like to (1) Hit or (2) stand? ")
        if (player_action == 'Hit') or (player_action == '1'):
            new_log = addCard('player')
            print(f"You have been dealt a {new_log[-1]}.")
            checkState()
        elif (player_action == 'Stand') or (player_action == '2'):
            print("You have not asked for another card. Waiting for next player/computer action. \n")
            pcActions()
        else: 
            print('Invalid action; please try again: ')
            playerActions()

        return 

    def pcActions():
        nonlocal hidden_card, pc_score, hidden_status, pc_bust_checker

        print(f"The dealer reveals the {hidden_card[-1]} as the hidden card!")
        hidden_status = FALSE 

        for i in range(0,len(pc_score)):
            if (pc_score[i]) == (1,11):
                if (pc_score[i] == (1,11)) and (pc_score[-1] != (1,11)) and (11 + int(pc_score[-1]) >= 17):
                    pc_score[i] = 11
                elif (pc_score[i] == (1,11)) and (pc_score[-1] == (1,11)):
                    pc_score[i] = 11
                    pc_score[-1] = 1
                else: pc_score[i] = 1
        
        pc_bust_checker = sum(list(pc_score))

        checkState()

        return 

    def announceWinners():
        nonlocal player_score, pc_score

        player_final = sum(list(player_score))
        pc_final = sum(list(pc_score))

        result = max(player_final,pc_final)

        print(f"{username} wins this round!") if result == sum(list(player_score)) else print("Computer wins this round. Better luck next time!")
        system.exit()

        return 

    return logHistory, computeVal, checkState


# run script
startGame, dealCards, thePlay = playBJ() 

username = input("What is your name? ")
print(f"Welcome to the Game of Black Jack, {username}!")

startGame()
dealCards()
thePlay()

