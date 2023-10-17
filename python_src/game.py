'''
OK THINK YOU CAN ONLY NOT PAYOUT BLINDS WHEN BOTH BLINDS PUT IN MONEY PREFLOP IF THEY DON'T OR IF 
ONLY ONE DOES THAN ONLY THAT AMOUNT IS UP FOR GRABS
'''
import copy
from dealer import Dealer
from player import Player


class Game:
    def __init__(self,num_players,stack,bb,sb):
        self.sb = sb
        self.bb = bb
        self.num_players = num_players
        self.players = [Player(stack,bb,sb) for _ in range(num_players)]
        self.sb_pos = 0
        self.bb_pos = 1
        self.utg = self.bb_pos +1 if num_players > 2 else self.sb_pos
        self.dealer_button = num_players -1 if num_players > 2 else self.bb_pos
        self.community_cards = None
        self.dealer = Dealer(num_players)
        self.pot = 0
        self.blinds = 0
        self.all_in = [False for _ in range(num_players)]
        self.in_hand = [True for _ in range(num_players)]
        self.straights = self.create_straights()
        self.flush_count = 0
        self.flush_suit = None
        self.sb_paid = 0
        self.bb_paid = 0
        self.hand_rankings = {'SF':900,'Q':800,'FH':700,'F':600, '5F':500 ,'S':400,'T':300,
        'TP':200,'P':100,'H':0}

    def change_blinds(self):
        if self.num_players > 2:
            self.bb_pos = self.bb_pos + 1 if (self.bb_pos + 1 < self.num_players) else 0
            self.sb_pos = self.sb_pos + 1 if (self.sb_pos + 1 < self.num_players) else 0
            self.dealer_button = self.dealer_button + 1 if (self.dealer_button + 1 < self.num_players) else 0
            self.utg = self.utg + 1 if (self.utg + 1 < self.num_players) else 0
        else:
            self.bb_pos = self.bb_pos + 1 if (self.bb_pos + 1 < self.num_players) else 0
            self.sb_pos = self.sb_pos + 1 if (self.sb_pos + 1 < self.num_players) else 0
            self.utg = self.sb_pos
            self.dealer_button = self.bb_pos

    def preflop(self):
        player_cards= self.dealer.deal_preflop()
        for i,player in enumerate(self.players):
            player.get_cards(player_cards[i])
        self.bb_paid,self.all_in[self.bb_pos] = self.players[self.bb_pos].pay_bb()
        self.sb_paid,self.all_in[self.sb_pos] = self.players[self.sb_pos].pay_sb()
        self.blinds = self.bb_paid + self.sb_paid
        self.pot = self.blinds

    #Pretty sure this is working now needs more testing make same changes to non preflop
    #func
    def street_preflop(self):
        print("Here are the current positions for players:")
        print(f"UTG: {self.utg}")
        print(f"SB: {self.sb_pos}")
        print(f"BB: {self.bb_pos}")
        left_to_act = [True for _ in range(self.num_players)]
        total = 0
        prev_bet = 0
        current = self.utg
        min_bet = 2 * self.bb
        collect_sb = True
        first_bb_action = True
        edge_bb_raise_condition = False
        while sum(left_to_act)> 0:
            if not self.all_in[current] and self.in_hand[current]:
                bet,self.all_in[current],self.in_hand[current],total,action_taken = \
                self.players[current].get_action(prev_bet,self.pot,min_bet)
                print(f"player {current}: {action_taken}")
                if collect_sb and current == self.sb_pos:
                    collect_sb = False
                    if bet:
                        if total <= self.bb:
                            self.blinds += bet
                        else:
                            self.blinds -= self.sb
                elif first_bb_action and current == self.bb_pos:
                    if total >= min_bet:
                        self.blinds -= self.bb
                    first_bb_action = False
                if total >= min_bet and total >= 2*prev_bet:
                    left_to_act = [self.in_hand[i] and not self.all_in[i] for i in range(self.num_players)]
                    prev_bet = total

                self.pot += bet
                left_to_act[current] = False
            print(f"The pot is: {self.pot}")
            current += 1 if current+1 < self.num_players else -current

    def street(self):
        if sum(self.in_hand) == sum(self.all_in):
            return
        left_to_act = [True for _ in range(self.num_players)]
        total = 0
        prev_bet = 0
        current = self.sb_pos
        min_bet = self.bb

        while sum(left_to_act) > 0:
            if not self.all_in[current] and self.in_hand[current] and left_to_act[current]:
                bet,self.all_in[current],self.in_hand[current],total,action_taken = \
                self.players[current].get_action(prev_bet,self.pot,min_bet)
                print(f"player {current}: {action_taken}")
                if total > min_bet and total >= 2 * prev_bet:
                    prev_bet = total
                    left_to_act = [not self.all_in[i] and self.in_hand[i] for i in range(self.num_players)]
                self.pot += bet
                left_to_act[current] = False

            print(f"The pot is: {self.pot}")
            current += 1 if current+1 < self.num_players else -current

    def street_reset(self):
        for i,player in enumerate(self.players):
            player.reset_street()
            print(f"player: {i}s stack is: {player.stack}")


    def create_straights(self):
        straights = [[i for i in range(i,i+5)][::-1] for i in range(1,11)]
        straights = straights[::-1]
        return straights

    def reset(self):
        #print(f"The pot is: {self.pot}")
        for i,player in enumerate(self.players):
            print(f"AT THE END OF THE HAND PLAYER {i}s stack is: {player.stack}")
        print()
        print()
        self.blinds = 0
        self.community_cards = []
        self.pot = 0
        self.in_hand = [True for _ in range(self.num_players)]
        self.all_in = [False for _ in range(self.num_players)]
        self.dealer.reset()
        self.change_blinds()
        for i,player in enumerate(self.players):
            player.reset()


    def payout(self,players,multiple=False):
        print(f"pot size at the end: {self.pot}")
        for i in range(self.num_players):
            print(f"Amoutn player {i} can win is: {self.players[i].amount_to_win}")
        if not multiple:
            players.stack += self.pot
            return
            #return self.reset()
        player_bets = [player.amount_to_win for player in self.players]
        players_in_hand = sum(self.in_hand)
        self.payouts_blinds(players)

        while players_in_hand:
            #print([player_bets[i] for i,_ in players if self.in_hand[i]])
            if players_in_hand == 1:
                for i,_ in players:
                    if self.in_hand[i]:
                        self.players[i].stack += self.pot
                        return
                        #return self.reset()
            else:
                min_bet = min([player_bets[i] for i,_ in players if self.in_hand[i]])
                side_pot = min_bet * players_in_hand
                self.pot -= side_pot
                best_hand = max(i for x,(i,_) in players if self.in_hand[x])
                indexes = [i for i,(x,_) in players if self.in_hand[i] and x == best_hand]
                winnings = side_pot/len(indexes)
                for index,_ in players:
                    if index in indexes:
                        self.players[index].stack += winnings
                        #self.players[index].stack -= min_bet
                    player_bets[index] -= min_bet
                    self.in_hand[index] = False if not player_bets[index] else True

            players_in_hand = sum(self.in_hand)
            if players_in_hand == 0:
                return
    #Payouts for the bb and sb when all in are wrong 
    #you can actually win bb_paid and sb_paid depending on which is which and then you need to adjust
    #both of those
    def payouts_blinds(self,players):
        print(f"On payout blinds and the blind payout amount is: {self.blinds}")
        sorted_players = sorted(players, key= lambda x: x[1][0], reverse=True)
        #i = sorted_players[0]
        for i,_ in sorted_players:
            if i == self.bb_pos and self.bb_paid < self.bb or i == self.sb_pos and self.sb_paid < self.sb:
                if i == self.bb_pos:
                    self.in_hand[i] = False
                    self.players[i].stack += self.bb_paid
                    self.blinds -= self.bb_paid
                    self.pot -= self.bb_paid
                else:
                    self.in_hand[i] = False
                    self.players[i].stack += self.sb_paid
                    self.blinds -= self.sb_paid
                    self.pot -= self.sb_paid
            else:
                self.players[i].stack += self.blinds
                self.pot -= self.blinds
                return


    def get_hand_strengths(self):
        return [(i,self.hand_strength(self.players[i])) for i,x in enumerate(self.in_hand) if self.in_hand[i]]

    def hand_strength(self,player):
        flush = self.flush(player)
        if flush > self.hand_rankings['SF']:
            if flush == 960:
                return flush, "ROYAL FLUSH!"
            #straight flush
            return flush, 'STRAIGHT FLUSH'
        pairs = self._pair(player)
        if pairs:
            if pairs > self.hand_rankings['Q']:
                return pairs, "QUADS"
            if pairs > self.hand_rankings['FH']:
                return pairs, "FULL HOUSE"
        if flush:
            return flush, "FLUSH"
        straight = self._straight(player)
        if straight:
            return straight, "STRAIGHT"
        if pairs:
            if pairs > self.hand_rankings['T']:
                return pairs, "TRIPS"
            if pairs > self.hand_rankings['TP']:
                return pairs, "TWO PAIR"
            return pairs, "PAIR"
        return self.high_card(player), "HIGH CARD"


    def _pair(self,player):
        community_cards_vals = list(self.dealer.get_value_count().keys())
        board_pairs = copy.deepcopy(self.dealer.board_pairs)
        items = list(board_pairs.keys())
        if player.left_val == player.right_val:
            if player.left_val in items:

                board_pairs[player.left_val] +=2
            else:
                board_pairs[player.left_val] = 2
        else:
            if player.left_val in community_cards_vals:
                if player.left_val in items:
                    board_pairs[player.left_val] += 1
                else:
                    board_pairs[player.left_val] = 2
            if player.right_val in community_cards_vals:
                if player.right_val in items:
                    board_pairs[player.right_val] += 1
                else:
                    board_pairs[player.right_val] = 2
        quads = 0
        trips = 0
        a_pair = []
        if board_pairs:
            if player.left_val in items:
                board_pairs[player.left_val] +=1
            if player.right_val in items:
                board_pairs[player.right_val] += 1
            for i in board_pairs:
                quads = i if board_pairs[i] == 4 and i > quads else quads
                trips = i if board_pairs[i] == 3 and i > trips else trips
                a_pair += [i] if board_pairs[i] == 2 else []
            if quads:
                return self.hand_rankings['Q'] + quads
            if trips:
                if a_pair:
                    a_pair.sort()
                    return self.hand_rankings['FH'] + trips + a_pair[-1]/100
                all_cards = community_cards_vals + [player.left_val, player.right_val]
                temp = [card for card in all_cards if card != trips]
                temp.sort(reverse=True)
                temp = temp[0]/100 + temp[1]/1000
                return self.hand_rankings['T'] + trips + temp
            elif len(a_pair) >=2:
                all_cards = community_cards_vals + [player.left_val, player.right_val]
                a_pair.sort(reverse=True)
                temp = max([card for card in all_cards if card not in a_pair[0:2]])
                return self.hand_rankings['TP'] + a_pair[0]/10 + a_pair[1]/100 + temp/1000
            elif a_pair:
                a_pair.sort(reverse=True)
                all_cards = community_cards_vals + [player.left_val, player.right_val]
                temp = [card for card in all_cards if card not in a_pair][0:4]
                temp.sort(reverse=True)
                temp = temp[0]/10 + temp[1] / 100 + temp[2] /200 + temp[3] / 300
                return self.hand_rankings['P'] + a_pair[0] + temp
        return False

    #NEED TO SORT THIS
    def flush(self,player):
        if self.flush_suit:
            if self.flush_count < 5:
                right = [] if player.right_suit != self.flush_suit else [player.right_val]
                left = [] if player.left_suit != self.flush_suit else [player.left_val]
                temp = list(set([i.value for i in self.community_cards if i.suit == self.flush_suit] + left + right))
                if len(temp) >= 5:
                    s_f = self.straight_flush(temp)
                    if s_f:
                        return self.hand_rankings['SF'] + s_f
                    return self.hand_rankings['F'] + right[0] if right else\
                    self.hand_rankings['F'] + left[0]

            if self.flush_count == 5:
                right = [] if player.right_suit != self.flush_suit else [player.right_val]
                left = [] if player.left_suit != self.flush_suit else [player.left_val]
                temp = list(set([i.value for i in self.community_cards if i.suit == self.flush_suit] + left + right))
                temp.sort(reverse=True)
                temp = temp[0] + temp[1] /10 + temp[2] /100 + temp[3] / 200 + temp[4] / 300
                return self.hand_rankings['5F'] + temp
        return False


    #just return the hand ranking if valid
    def straight_flush(self,hand):
        hand.sort(reverse = True)
        if 14 == hand[0]:
            hand.append(1)
        i = 0
        while i < len(hand) -5:
            temp = hand[i:i+5]
            for straight in self.straights:
                if straight == temp:
                    return straight[0] + self.hand_rankings['SF']
            i+=1
        return False

    #THERE'S A NONE IN HERE SOMEHOW
    def _straight(self,player):
        cards = list(set([i.value for i in self.community_cards] + [player.left_val, player.right_val]))
        cards.sort(reverse=True)
        if 14 == cards[0]:
            cards.append(1)
        i = 0
        while i< len(cards) -5:
            temp = cards[i:i+5]
            for straight in self.straights:
                if straight == temp:
                    return straight[0] + self.hand_rankings['S']
            i+=1
        return False


    def high_card(self,player):
        temp = sorted([i.value for i in self.community_cards] + [player.left_val,player.right_val], reverse=True)
        temp = temp[0] + temp[1] /10 + temp[2] /20 + temp[3] /30 + temp[4] /50
        return self.hand_rankings['H'] + temp

    def hand_over(self,river=False):
        return sum(self.in_hand) == 1
