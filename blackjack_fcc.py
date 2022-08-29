from random import randint, choice
from re import L 

#setup

suits = ('Hearts','Clubs','Diamonds','Spades')

pip = ('Ace','King','Queen','Jack','Ten','Nine','Eight','Seven','Six','Five','Four','Three','Two')

card_val = {'Ace' : (1,11),
            'King': 10, 'Queen': 10, 'Jack': 10, 'Ten':10,
            'Nine':9, 'Eight':8, 'Seven':7, 'Six':6, 'Five':5, 'Four':4, 'Three':3, 'Two':2}


#rules 

def playBJ():
    winner = []
    card_history = []
    player_score = []
    pc_score = []
    pip_values = []
    count = 0

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

    def computeVal():
        nonlocal card_history, count, player_score, pc_score, pip_values
        
        for i in range(count,len(card_history)):
            if (i % 2) == 0:
                player_score.append(card_val[pip_values[i]])
                print(f"You have been dealt a {card_history[i]} faced up!")
            else:
                pc_score.append(card_val[pip_values[i]])
                if (i != len(card_history)-1): 
                    print(f"The house has revealed a {card_history[i]}")
                else: 
                    print("The dealer puts their 2nd card faced down. All cards have been dealt.")
        
        # print(player_score)
        # print(pc_score)
        # print(pip_values)

        count += len(card_history)
        # print(count)

        return count

    def chooseAction():
        player_action = print("Would you like to hit or stand?")
        return 

    def announceWinner(): 
        nonlocal player_score, pc_score, winner, card_history

        if player_score > pc_score:
            winner += ['Player']
        elif player_score == pc_score:
            print("No Winner. Go Again!")
        else: 
            winner += ['Computer']
        return winner 

    return logHistory, computeVal, announceWinner 

getHistory, getVal, getWinner = playBJ() 

# start game
username = input("What is your name? ")
print(f"Welcome to the Game of Black Jack, {username}!")

history_log = getHistory()

getVal()




# for suit in suits:
#     print(f"your card is {pip} of {suit}")
#     print(suits[randint(0,3)] == suit)

# print(choice(suits) == suits[randint(0,3)])

# print( (card_val['Ace'])[1] )
# print(getWinner())

