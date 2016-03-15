"""
    Blackjack.py - Yevheniy Chuba - Spring 2014
    Implementation of Blackjack. Enjoy: http://www.codeskulptor.org/#user31_R8PVRLqskziSghE.py
    
    Although we used class-specific CodeSculptor for graphics, most of the methods
    and the rest of the concepts are similar if not the same in other Python librararies, 
    such as Pygame.
    Learned to:
        - play Blackjack
        - nice intro to OOP
        - track/flowchart complex logic
"""

import simplegui
import random

# load card sprite - 950x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize global variables
all_cards = []
in_play = False
win_loose_mess = ""
hit_stand_mess = "Hit or Stand?"
score = 0

player_hand = []
dealer_hand = []

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", self.suit, self.rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_SIZE[0] * (0.5 + RANKS.index(self.rank)), CARD_SIZE[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_SIZE[0] / 2, pos[1] + CARD_SIZE[1] / 2], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self, deck_cards, player_hand, dealer_hand):
        self.deck_cards = deck_cards
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand

    def __str__(self):
        pass	# replace with your code

    def add_card(self):
        card = self.deck_cards[4]
        self.player_hand += [card]
        return self.player_hand
    
    def add_card_dealer(self):
        card = self.deck_cards[4]
        self.dealer_hand += [card]
        return self.dealer_hand

    # count aces as 1, if the hand has an ace, then add 10 to hand value if don't bust
    def get_value(self, player_hand):
        final_value = []
        self.player_hand = player_hand
        for card in self.player_hand:
            final_value.append(VALUES[card[1]])
        if sum(final_value) > 21:
            final_value = [100,1]
        return sum(final_value)
    
    def get_value_dealer(self, dealer_hand):
        final_value = []
        self.dealer_hand = dealer_hand
        for card in self.dealer_hand:
            final_value.append(VALUES[card[1]])
        if sum(final_value) > 21:
            final_value = [100,1]
        return sum(final_value)
        

    def busted(self):
        in_play = False
        pass	# replace with your code
    
    def draw(self, canvas, p):
        pass	# replace with your code
 
        
# define deck class
class Deck:
    def __init__(self):
        self.RANKS = RANKS
        self.SUITS = SUITS
        self.deck_cards = []

    # add cards back to deck and shuffle
    def shuffle_cards(self):
        for rank in self.RANKS: 
            card_c = [self.SUITS[0], rank]
            card_h = [self.SUITS[1], rank]
            card_d = [self.SUITS[2], rank]
            card_s = [self.SUITS[3], rank]
            self.deck_cards.append(card_c)
            self.deck_cards.append(card_h)
            self.deck_cards.append(card_d)
            self.deck_cards.append(card_s)
        random.shuffle(self.deck_cards)
        return self.deck_cards

    def deal_card(self):
        card = self.deck_cards[4]
        self.deck_cards.pop(4)
        return card


#define callbacks for buttons
def deal():
    global win_loose_mess, hit_stand_mess, in_play, score, deck, all_cards
    global dealers_card_1, dealers_card_2, players_card_1, players_card_2, player_hand, dealer_hand
    
    if in_play:
        player_hand = []
        dealer_hand = []
        all_cards = []
        deck = Deck() # initiate the game
        all_cards = deck.shuffle_cards()
        #Initiate the cards
        dealers_card_1 = Card(all_cards[0][0], all_cards[0][1])
        dealers_card_2 = Card(all_cards[1][0], all_cards[1][1])
        dealer_hand = [[dealers_card_1.get_suit(), dealers_card_1.get_rank()],
                     [dealers_card_2.get_suit(), dealers_card_2.get_rank()]]

        players_card_1 = Card(all_cards[2][0], all_cards[2][1])
        players_card_2 = Card(all_cards[3][0], all_cards[3][1])
        player_hand = [[players_card_1.get_suit(),players_card_1.get_rank()],
                       [players_card_2.get_suit(), players_card_2.get_rank()]]
    
        score = score
        win_loose_mess = ""
        hit_stand_mess = "Hit or Stand?"
    else: # if the game has not been played yet
        
        deck = Deck() # initiate the game
        all_cards = deck.shuffle_cards()
        in_play = True
        
        

def hit():
    global player_hand, dealer_hand, player_final_value, score, win_loose_mess, hit_stand_mess, in_play
    # if the hand is in play, hit the player
    if in_play:
        playing_hand = Hand(all_cards, player_hand, dealer_hand)
        player_hand = playing_hand.add_card()
        player_hand_value = playing_hand.get_value(player_hand)
        player_final_value = player_hand_value
        print player_hand_value
        #print player_hand_value
        if player_hand_value == 101:
            score -= 1
            win_loose_mess = "You Lost - over 21"
            hit_stand_mess = "New Deal?"
            
            
   
    # if busted, assign an message to outcome, update in_play and score
       
def stand():
    global player_hand, dealer_hand, player_final_value, dealer_final_value, score, win_loose_mess, hit_stand_mess, in_play
    
    dealing_hand = Hand(all_cards, player_hand, dealer_hand)
    dealer_hand_value = dealing_hand.get_value_dealer(dealer_hand)
    
    playing_hand = Hand(all_cards, player_hand, dealer_hand)
    player_final_value = playing_hand.get_value(player_hand)
    
    if dealer_hand_value == 101:
        score += 1
        win_loose_mess = "You Win!"
        hit_stand_mess = "New Deal?"
    elif dealer_hand_value < 17:
        dealer_hand = dealing_hand.add_card_dealer()
        dealer_hand_value = dealing_hand.get_value_dealer(dealer_hand)
        if dealer_hand_value == 101:
            score += 1
            win_loose_mess = "You Win!"
            hit_stand_mess = "New Deal?"
        elif dealer_hand_value > player_final_value:
            score -= 1
            win_loose_mess = "You Lost"
            hit_stand_mess = "New Deal?"
        elif dealer_hand_value < player_final_value:
            score += 1
            win_loose_mess = "You Win!"
            hit_stand_mess = "New Deal?"
        elif dealer_hand_value == player_final_value:
            score -= 1
            win_loose_mess = "You Lost"
            hit_stand_mess = "New Deal?"
    elif dealer_hand_value > 17:	
        if dealer_hand_value > player_final_value:
            score -= 1
            win_loose_mess = "You Lost"
            hit_stand_mess = "New Deal?"
        elif dealer_hand_value < player_final_value:
            score += 1
            win_loose_mess = "You Win!"
            hit_stand_mess = "New Deal?"
        elif dealer_hand_value == player_final_value:
            score -= 1
            win_loose_mess = "You Lost"
            hit_stand_mess = "New Deal?"
            

def draw(canvas):
    global all_cards, win_loose_mess, hit_stand_mess, score, player_hand, dealer_hand
    # draw static text: blackjack, dealer, player
    canvas.draw_text('Blackjack', (5, 50), 50, 'Blue', 'serif')
    canvas.draw_text('Dealer', (20, 150), 40, 'Black', 'serif')
    canvas.draw_text('Player', (20, 350), 40, 'Black', 'serif')
    # draw dynamic text: Score, "Hit or Stand" or "New Deal"
    canvas.draw_text('Score: '+str(score), (400, 50), 40, 'Black', 'serif')
    canvas.draw_text(hit_stand_mess, (230, 350), 40, 'Black', 'serif')
    canvas.draw_text(win_loose_mess, (230, 150), 40, 'Black', 'serif')
    
    
    dealers_card_1.draw(canvas, [60, 170])
    dealers_card_2.draw(canvas, [170, 170])
    
    players_card_1.draw(canvas, [60, 400])
    players_card_2.draw(canvas, [170, 400])
    
    if len(dealer_hand) == 3:
        dealers_card_3 = Card(all_cards[4][0], all_cards[4][1])
        dealers_card_3.draw(canvas, [290, 170])
        dealer_hand = [[dealers_card_1.get_suit(),dealers_card_1.get_rank()],
                        [dealers_card_2.get_suit(), dealers_card_2.get_rank()], 
                        [dealers_card_3.get_suit(), dealers_card_3.get_rank()]]
    
    if len(player_hand) == 3:
        players_card_3 = Card(all_cards[5][0], all_cards[5][1])
        players_card_3.draw(canvas, [290, 400])
        player_hand = [[players_card_1.get_suit(),players_card_1.get_rank()],
                        [players_card_2.get_suit(), players_card_2.get_rank()], 
                        [players_card_3.get_suit(), players_card_3.get_rank()]]
    
    if len(dealer_hand) == 4:
        dealers_card_3 = Card(all_cards[4][0], all_cards[4][1])
        dealers_card_3.draw(canvas, [290, 170])
        dealers_card_4 = Card(all_cards[6][0], all_cards[6][1])
        dealers_card_4.draw(canvas, [400, 170])
        dealer_hand = [[dealers_card_1.get_suit(),dealers_card_1.get_rank()],
                        [dealers_card_2.get_suit(), dealers_card_2.get_rank()], 
                        [dealers_card_3.get_suit(), dealers_card_3.get_rank()],
                        [dealers_card_4.get_suit(), dealers_card_4.get_rank()]]
    
    if len(player_hand) == 4:
        players_card_3 = Card(all_cards[5][0], all_cards[5][1])
        players_card_3.draw(canvas, [290, 400])
        players_card_4 = Card(all_cards[7][0], all_cards[7][1])
        players_card_4.draw(canvas, [400, 400])
        player_hand = [[players_card_1.get_suit(),players_card_1.get_rank()],
                        [players_card_2.get_suit(), players_card_2.get_rank()], 
                        [players_card_3.get_suit(), players_card_3.get_rank()],
                        [players_card_4.get_suit(), players_card_4.get_rank()]]

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()
#Initiate the cards
dealers_card_1 = Card(all_cards[0][0], all_cards[0][1])
dealers_card_2 = Card(all_cards[1][0], all_cards[1][1])
dealer_hand = [[dealers_card_1.get_suit(), dealers_card_1.get_rank()],
               [dealers_card_2.get_suit(), dealers_card_2.get_rank()]]

players_card_1 = Card(all_cards[2][0], all_cards[2][1])
players_card_2 = Card(all_cards[3][0], all_cards[3][1])
player_hand = [[players_card_1.get_suit(),players_card_1.get_rank()],
               [players_card_2.get_suit(), players_card_2.get_rank()]]



# get things rolling
frame.start()