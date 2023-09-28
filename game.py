from dealer import Dealer
from Newcards import Card
from player import Player
import copy
'''
out community cards are a copy of the dealers community cards so when we append them in
dealer it appens to the game so actually appending it is unnecisary
'''
class Game:
	def __init__(self, num_players=2,bb=1,sb=.5,starting_stack=100):
		self.num_players = num_players
		self.players = [Player(starting_stack, bb,sb) for _ in range(num_players)]
		self.in_hand = [True for _ in range(num_players)]
		self.all_in = [False for _ in range(num_players)]
		self.dealer = Dealer(num_players)
		self.community_cards = []
		self.pot = 0
		self.bb = bb
		self.sb = sb
		#NEW FOR ADDING BLINDS FOR PAYOUTS
		#self.blinds = 0
		self.sb_pos = 0
		self.bb_pos = 1
		self.utg = self.bb_pos +1 if num_players > 2 else self.sb_pos
		self.dealer_button = num_players -1 if num_players > 2 else self.bb_pos
		self.straights = self.create_straights()
		self.flush_count = 0
		self.flush_suit = None
		self.player_bets = [0 for _ in range(num_players)]
		self.street_bets = [0 for _ in range(num_players)]
		#from strongest to weakest 5F = Five flush cause largest card may be on the board
		self.hand_rankings = {'SF':900,'Q':800,'FH':700,'F':600, '5F':500 ,'S':400,'T':300,
		'TP':200,'P':100,'H':0}
		'''
		print()
		print(f"BIG BLIND IS PLAYER: {self.bb_pos+1}")
		print(f"SMALL BLIND PLAYER: {self.sb_pos+1}")
		print(f"UNDER THE GUN PLAYER: {self.utg+1}")
		print(f"DEALER BUTTON PLAYER: {self.dealer_button+1}")
		print()
		'''

	#PRINT OUT COMMUNITY CARDS AT EACH STAGE AND SEE WHERE THE ERROR IS TAKING PLACE
	def gameloop(self):
		#PREFLOP
		self.deal_cards()
		#preflop action
		print("PREFLOP ACTION")
		self.street(True)
		self.collect_stack()
		if self.hand_over():
			i = 0
			while not self.in_hand[i]:
				i+=1
			self.payout(self.players[i])
			return
		#FLOP
		self.community_cards = self.dealer.deal_flop()
		flop_display = ""
		for i in self.community_cards:
			flop_display += str(i) + " "
		print(f"The Flop came: {flop_display}")
		self.street(False)
		self.collect_stack()
		if self.hand_over():
			i = 0
			while not self.in_hand[i]:
				i+=1
			self.payout(self.players[i])
			return
		#TURN
		#self.community_cards.append(self.dealer.deal_turn())
		self.dealer.deal_turn()
		print(f"The Turn came: {flop_display}" + str(self.community_cards[-1]))
		self.street(False)
		self.collect_stack()
		if self.hand_over():
			i = 0
			while not self.in_hand[i]:
				i+=1
			self.payout(self.players[i])
		#RIVER
		#self.community_cards.append(self.dealer.deal_river())
		self.dealer.deal_river()
		print(f"The River came: {flop_display}" + str(self.community_cards[-2]) + " " +\
		 str(self.community_cards[-1]))
		self.street(False)
		self.collect_stack()
		if self.hand_over():
			i = 0
			while not self.in_hand[i]:
				i+=1
			self.payout(self.players[i])
		else:
			self.flush_suit, self.flush_count = self.dealer.get_poss_flush()
			hand_strengths = self.get_hand_strengths()
			self.payout(hand_strengths,True)
	
	def reset(self):
		for i,player in enumerate(self.players):
			print(f"AT THE END OF THE HAND PLAYER {i}s stack is: {player.stack}")
		print()
		print()
		self.community_cards = []
		self.pot = 0
		self.in_hand = [True for _ in range(self.num_players)]
		self.all_in = [False for _ in range(self.num_players)]
		self.dealer.reset()
		self.change_blinds()
		for i,player in enumerate(self.players):
			player.reset()
			print(f"AT THE END END END OF THE HAND PLAYER {i}s stack is: {player.stack}")

	def payout(self,players,multiple=False):	
		if not multiple:
			players.stack += self.pot
			return self.reset()
		player_bets = [player.can_win_amount for player in self.players]
		players_in_hand = sum(self.in_hand)
		while players_in_hand:
			if players_in_hand == 1:
				print("\nONE PLAYER REMAINING\n")
				for i,_ in players:
					if self.in_hand[i] == True:
						self.players[i].stack += self.pot
						return self.reset()
						#self.in_hand[i] = False
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
						self.players[index].stack -= min_bet
					player_bets[index] -= min_bet
					self.in_hand[index] = False if player_bets[index] == 0 else True
			
			players_in_hand = sum(self.in_hand)
			if players_in_hand == 0:
				#print("\nNO PLAYERS RAMINING\n")
				return self.reset()


	def create_straights(self):
		straights = [[i for i in range(i,i+5)][::-1] for i in range(1,11)]
		straights = straights[::-1]
		return straights


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
			elif trips:
				if a_pair:
					a_pair.sort()
					return self.hand_rankings['FH'] + trips + a_pair[-1]/100
				else:
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


	def flush(self,player):
		if self.flush_suit:
			if self.flush_count < 5:
				right = [] if player.right_suit != self.flush_suit else [player.right_val]
				left = [] if player.left_suit != self.flush_suit else [player.left_val]
				temp = [i.value for i in self.community_cards if i.suit == self.flush_suit] + left + right
				if len(temp) >= 5:
					s_f = self.straight_flush(temp)
					if s_f:
						return self.hand_rankings['SF'] + s_f
					#if len(right) and len(left):
						#return self.hand_rankings['F'] + right[0] if right[0] > left[0] else\
						#self.hand_rankings['F'] + left[0]
					else:
						return self.hand_rankings['F'] + right[0] if right else\
						self.hand_rankings['F'] + left[0]
			if self.flush_count == 5:
				#FIVE FLUSH
				right = [] if player.right_suit != self.flush_suit else [player.right_val]
				left = [] if player.left_suit != self.flush_suit else [player.left_val]
				temp = [i.value for i in self.community_cards if i.suit == self.flush_suit] + left + right
				temp.sort(reverse=True)
				temp = temp[0] + temp[1] /10 + temp[2] /100 + temp[3] / 200 + temp[4] / 300
				return self.hand_rankings['5F'] + temp
		return False

	#just return the hand ranking if valid
	def straight_flush(self,hand):
		maxx = False
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

	def _straight(self,player):
		cards = [i.value for i in self.community_cards] + [player.left_val, player.right_val]
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

	#technically the amount they anyone can win is the amount the bb 
	def deal_cards(self):
		hands = self.dealer.deal_preflop()
		for player,hand in zip(self.players,hands):
			player.get_hand(hand)
		#PAY THE BLINDS
		self.player_bets[self.bb_pos],self.all_in[self.bb_pos] = self.players[self.bb_pos].pay_blinds(self.bb, 'bb`')
		sb_temp,self.all_in[self.sb_pos] = self.players[self.sb_pos].pay_blinds(self.sb, 'sb')
		self.pot += self.player_bets[self.bb_pos] + sb_temp #doing it this way cause theoretically player could be all in
		for i,player in enumerate(self.players):
			if i != self.sb_pos:
				player.can_win_amount = self.player_bets[self.bb_pos]
			else:
				player.can_win_amount = sb_temp
	def street(self,preflop):
		count = 0
		prev_bet = 0
		self.street_bets = [0 for _ in range(self.num_players)]
		current_pot = 0

		if preflop:
			current = self.utg
			self.sb_check = True
			min_bet = 2 * self.bb
		else:
			current = self.sb_pos
			self.sb_check = False
			min_bet = self.bb

		while count < self.num_players:
			if self.in_hand[current] and not self.all_in[current]:
				bet, self.all_in[current],self.in_hand[current], action_taken = \
				self.players[current].get_action(prev_bet,self.pot,min_bet)
				print()
				print(f"Player {current+1}: {action_taken}")
				print()
				if bet:
					self.street_bets[current] = bet
					self.pot = sum(self.street_bets) + sum(self.player_bets)
					if bet > prev_bet and bet >= min_bet:
						prev_bet,count = bet,0
					else:
						if self.sb_check:
							self.sb_check = False
						else:
							prev_bet,count = min_bet,count

					
			current += 1 if current+1 < self.num_players else -current
			count +=1

	def collect_stack(self):
		print(f"The pot size is {self.pot}")
		for i,player in enumerate(self.players):
			player.collect()
			self.player_bets[i] += self.street_bets[i]

		


