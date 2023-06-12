import random

# representing the suits of a deck
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')  # representing the card ranks
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}  # associating the rank to a value inside a dictionary for comparison and calculating purposes later on

playing = True


class Card:

    def __init__(self, suit, rank):
        #Initialize a card object with given suit and rank
        self.suit = suit
        self.rank = rank

    def __str__(self):
        # Return a string of the card object updated with it's proper suit and rank
        return f"{self.rank} of {self.suit}"


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                # generating cards from the values of touples ranks and suits
                created_cards = Card(suit, rank)
                # adding the created cards into the deck list
                self.deck.append(created_cards)

    def __str__(self):
        # Return a string for every element in the deck list
        deck_str = ''  # empty string placeholder
        for card in self.deck:
            # getting the values of the elements of the deck and transforming them to strings with a new line separator
            deck_str += str(card) + '\n'
        return deck_str

    def shuffle(self):
        # Shuffle the elements of the deck list
        random.shuffle(self.deck)

    def deal(self):
        # get one element from the deck list
        return self.deck.pop()


class Hand:

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)  # add the card to the hand's cards list
        # add the value of the card to the hand's value
        self.value += values[card.rank]

        # Check if the added card is an Ace and adjust for it if necessary
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # If the total value of the hand is greater than 21 and there are aces,
        # adjust the value of the aces from 11 to 1 until the total value is less than or equal to 21
        while self.value > 21 and self.aces > 0:
            self.value -= 10  # Adjust the value of the Ace from 11 to 1
            self.aces -= 1   # Decrease the count of aces


class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet
        self.bet = 0

    def lose_bet(self):
        self.total -= self.bet
        self.bet = 0

    def check_total(self):
        if self.total <= 0:
            user_input = input("Oops! You're out of chips! Do you want to add chips? Y or N ").upper()
            if user_input == 'Y':
                added_chips = int(input('Enter chips number: '))
                self.total += added_chips
            elif user_input != 'N':
                print('Sorry wrong input')
        return self.total



def take_bet(chips):
    while True:
        try:
            player_bet = int(input('Place your bet: '))
        except ValueError:
            print('Please provide a number for your bet.')
        else:
            if player_bet <= chips.total:
                chips.bet = player_bet  # Assign the player's bet to the chips' bet attribute
                return
            else:
                print('Insufficient chips. Please place a valid bet.')



def hit(deck, hand):
    new_card = deck.deal()  # Deal one card from the deck
    hand.add_card(new_card)  # Add the dealt card to the hand
    hand.adjust_for_ace()  # Adjust the hand's value if there are aces


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while playing:
        # player input controlling the loop
        player_choice = input('HIT or STAND? (H for Hit and S for stand) ').upper()
        if player_choice == 'H':
            return hit(deck, hand)
        elif player_choice == 'S':
            playing = False
            break
        else:
            print('Sorry, wrong input')


def show_some(player, dealer):
    player_hand = [str(card) for card in player.cards]
    dealer_hand = [str(card) for card in dealer.cards[1:]
                   ]  # Hide the dealer's first card

    print(
        f"Player's Hand: {player_hand}, value = {player.value}\nDealer's Hand: [Hidden Card], {dealer_hand}")


def show_all(player, dealer):
    # in case show_all is called, also return the value of the player's and dealer's hand
    player_hand = [str(card) for card in player.cards]
    dealer_hand = [str(card) for card in dealer.cards]

    print(f"Player's Hand: {player_hand} \nPlayer's Total Value: {player.value}\nDealer's Hand: {dealer_hand}\nDealer's Total Value: {dealer.value}")


def player_busts(player, chips):
    # prints a string for the player hand
    player_hand = [str(card) for card in player.cards]

    if player.value > 21:  # 21 is the max winning value in blackjack
        chips.lose_bet()  # update the total chips
        print(
            f"Player Busts! Player's hand: {player_hand}. Remaining chips: {chips.total}")
        return True  # Return True when the player busts
    
    return False  # Return False if the player didn't bust


def player_wins(player, dealer, chips):
    # prints a string for the player hand
    player_hand = [str(card) for card in player.cards]

    # in case 21 is not reached, the higher value between the player's and dealer's hand wins
    if player.value <= 21 and (player.value > dealer.value or dealer.value > 21):
        chips.win_bet()  # update the total chips
        print(f"Player Wins! Player's hand: {player_hand}. Remaining chips: {chips.total}")


def dealer_busts(dealer, chips):
    # prints a string for the player hand
    dealer_hand = [str(card) for card in dealer.cards]

    if dealer.value > 21:
        chips.win_bet()  # update the total chips
        print(f"Dealer Busts! Dealer's hand: {dealer_hand}.")


def dealer_wins(player, dealer, chips):
    # prints a string for the player hand
    dealer_hand = [str(card) for card in dealer.cards]

    if dealer.value <= 21 and (dealer.value > player.value or player.value > 21):
        chips.lose_bet()
        print(f"Dealer Wins! Dealer's hand: {dealer_hand}. Remaining chips: {chips.total}")


def push(player, dealer, chips):
    if player.value == dealer.value:
        chips.total
        print(f"It's a tie! Chips returned to the player. Remaining chips: {chips.total}")



''' CALLING THE GAME '''

# Set up the Player's chips
player_chips = Chips()

# Print an opening statement
print("Welcome to Light's Blackjack! Your initial chip total is 100. Enjoy!")

play_again = True
while play_again:

    # Create & shuffle the deck, deal two cards to each player
    new_deck = Deck()
    new_deck.shuffle()

    player = Hand()  # creating instances of the Hand class for the player and dealer
    dealer = Hand()

    for t in range(2):  # t is a throwaway variable used only to start the for loop in this case to execute each line of the code below twice
        player.add_card(new_deck.deal())
        dealer.add_card(new_deck.deal())

    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(new_deck, player)

        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_busts(player, player_chips):
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    else:
        dealer_playing = True

        while dealer_playing and dealer.value < 17:
            # this functions needs to loop so the dealer keeps getting cards based on the conditions above
            dealer.add_card(new_deck.deal())
            dealer.adjust_for_ace()
            show_some(player, dealer)
            if dealer.value > 21 or dealer.value > player.value:
                break

        # Show all cards
        show_all(player, dealer)

        # Run different winning scenarios
        player_wins(player, dealer, player_chips)
        # I need to set the conditions in which these are run
        dealer_busts(dealer, player_chips)
        dealer_wins(player, dealer, player_chips)
        push(player, dealer, player_chips)

    # Ask to play again
    if player_chips.check_total() <= 0:
        print(f"Player's remaining chips: {player_chips.total}")
        play_again = False
    else:
        play_again_input = input('Do you want to play again Y or N? : ').upper()
        if play_again_input == 'Y':
            playing = True
            print('Good luck in this round!')
        else:
            print(f"Player's remaining chips: {player_chips.total}")
            play_again = False

    
''' 
Changelog
v2 THE PROMPT ASKING PLAYERS FOR ADDITIONAL CHIPS WAS ADDED
v2.1 fixed the bust scenario acting code to freeze. Implemented H as an input for Hit and S for Stand to improve UX.
user note: no need for the input to be a capital letter since a function has been implemented to make sure the input is always uppercase.
v2.2 added check for aces function for the dealer. Added total player chips feedback in case of a tie.
'''
