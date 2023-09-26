from dealer import Dealer
from Newcards import Card
from player import Player
import copy
class Game:
	#MAKE SURE BETS ARE IN WHOLE NUMBERS
	#I FUCKED UP ON SPLIT POT SEE NOTES
	def __init__(self, num_players=2,bb=1,sb=.5,starting_stack=100):
		self.num_players = num_players
		self.players = [Player(starting_stack, bb,sb) for _ in range(num_players)]
		self.in_hand = [True for _ in range(num_players)]
		self.all_in = [False for _ in range(num_players)]
		self.dealer = Dealer(num_players)
		self.community_cards = []
		self.pot = 0
		self.player_bets = [0 for i in range(num_players)]
		self.sb_posted = 0
		self.bb_posted = 0
		self.bb = bb
		self.sb = sb
		self.sb_pos = 0
		self.bb_pos = 1
		self.utg = self.bb_pos +1 if num_players > 2 else self.sb_pos
		self.dealer_button = num_players -1 if num_players > 2 else self.bb_pos
		self.straights = self.create_straights()
		self.flush_count = 0
		self.flush_suit = None
		#from strongest to weakest 5F = Five flush cause largest card may be on the board
		self.hand_rankings = {'SF':900,'Q':800,'FH':700,'F':600, '5F':500 ,'S':400,'T':300,
		'TP':200,'P':100,'H':0}
		print()
		print(f"BIG BLIND POSITION: {self.bb_pos}")
		print(f"SMALL BLIND POSITION: {self.sb_pos}")
		print(f"UNDER THE GUN POSITION: {self.utg}")
		print(f"DEALER BUTTON POSITION: {self.dealer_button}")
		print()

	def gameloop(self):
		#PREFLOP
		self.deal_cards()
		#preflop action
		self.street(True)
		if self.hand_over():
			i = 0
			while not self.in_hand[i]:
				i+=1
			self.payout(self.in_hand[i])
			return
		#FLOP
		self.community_cards = self.dealer.deal_flop()
		flop_display = ""
		for i in self.community_cards:
			flop_display += str(i) + " "
		print(f"The Flop came: {flop_display}")
		self.street(False)
		if self.hand_over():
			i = 0
			while not self.in_hand[i]:
				i+=1
			self.payout(self.in_hand[i])
			return
		#TURN
		self.community_cards.append(self.dealer.deal_turn())
		print(f"The Turn came: {flop_display}" + str(self.community_cards[-1]))
		self.street(False)
		if self.hand_over():
			i = 0
			while not self.in_hand[i]:
				i+=1
			self.payout(self.in_hand[i])
		#RIVER
		self.community_cards.append(self.dealer.deal_river())
		print(f"The River came: {flop_display}" + str(self.community_cards[-2]) + " " +\
		 str(self.community_cards[-1]))
		self.street(False)
		if self.hand_over():
			i = 0
			while not self.in_hand[i]:
				i+=1
			self.payout(self.players[i])
		else:
			self.flush_suit, self.flush_count = self.dealer.get_poss_flush()
			hand_strengths = self.get_hand_strengths()
			self.payout(hand_strengths,True)
	'''
	ask players if they want to reload and if players who busted want to rejoin
	if a player busts and doesn't rejoin make sure to change self.numplayers 
	Basically kick out broke players if they don't rejoin ask them 
	also if player adds have to find way to account for that don't care for now
	'''
	def reset(self):
		self.community_cards = []
		self.pot = 0
		self.player_bets = []
		self.in_hand = [True for _ in range(num_players)]
		self.all_in = [False for _ in range(num_players)]
		self.player_bets = [0 for _ in range(self.num_players)]
		self.dealer.reset()
		self.change_blinds()

	def payout(self,players,multiple=False):
		if not multiple:
			players.stack += self.pot
			return self.reset()
		players_in_hand = sum(self.in_hand)
		
		while players_in_hand:
			if players_in_hand == 1:
				#just give the rest of the pot to the player
				for i,_ in players:
					if self.in_hand[i] == True:
						self.players[i].stack += self.pot
						return self.reset()
						#self.in_hand[i] = False
			else:
				#side_pot = min([players[1] for i in players]) * dont_stop
				min_bet = min([self.player_bets[i] for i,_ in players if self.in_hand[i]])
				side_pot = min_bet * players_in_hand
				self.pot -= side_pot
				best_hand = max(i for x,i in players if self.in_hand[x])
				indexes = [i for i,x in players if self.in_hand[i] and x == best_hand]
				winnings = side_pot/len(indexes)
				for index,_ in players:
					if index in indexes:
						self.players[index].stack += winnings
					elif self.in_hand[index]:
						self.players[index].stack -= min_bet

					self.player_bets[index] -= min_bet
					self.in_hand[index] = False if self.player_bets[index] == 0 else True
			
			players_in_hand = sum(self.in_hand)	

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
			return flush
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
		board_pairs = copy.deepcopy(self.dealer.board_pairs)
		items = board_pairs.keys()
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
					return self.hand_rankings['FH'] + trips + (1/10 * a_pair[-1])
				else:
					return self.hand_rankings['T'] + trips
			elif len(a_pair) >=2:
				a_pair.sort()
				return self.hand_rankings['TP'] + sum(a_pair[0:2])
			elif a_pair:
				return self.hand_rankings['P'] + a_pair[0]
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
						return self.hand_ranking['SF'] + s_f
					if right and left:
						return self.hand_rankings['F'] + right[0] if right[0] > left[0] else\
						self.hand_rankings['F'] + left[0]
					else:
						return self.hand_rankings['F'] + right[0] if right else\
						self.hand_rankings['F'] + left[0]
			#FIVE FLUSH
			right = [] if player.right_suit != self.flush_suit else [player.right_val]
			left = [] if player.left_suit != self.flush_suit else [player.left_val]
			temp = [i.value for i in self.community_cards if i.suit == self.flush_suit] + left + right
			temp.sort(reverse=True)
			return self.hand_rankings['5F'] + sum(temp[0:5])
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

		return self.hand_rankings['H'] + sum(temp[0:5])

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


	def deal_cards(self):
		hands = self.dealer.deal_preflop()
		for player,hand in zip(self.players,hands):
			player.get_hand(hand)
		#PAY THE BLINDS
		self.bb_posted,self.all_in[self.bb_pos] = self.players[self.bb_pos].pay_blinds(self.bb, 'bb`')
		#self.bb_posted = bb == self.bb
		self.sb_posted,self.all_in[self.sb_pos] = self.players[self.sb_pos].pay_blinds(self.sb, 'sb')
		#self.sb_posted = sb == self.sb
		self.pot += self.bb_posted + self.sb_posted
	
	def street(self,preflop):
		count = 0
		prev_bet = 0

		if preflop:
			current = self.utg
			#end = self.bb_pos
		else:
			current = self.sb_pos
			#end = self.dealer_button

		while count < self.num_players:
			if self.in_hand[current] and not self.all_in[current]:
				bet, self.all_in[current],self.in_hand[current], action_taken = \
				self.players[current].get_action(prev_bet,self.pot)
				print()
				print(f"Player {current+1}: {action_taken}")
				print()
				if bet:
					self.player_bets[current] = bet
					self.pot+= bet
					prev_bet,count = (bet,0) if bet>prev_bet else (prev_bet,count)

			current += 1 if current+1 < self.num_players else -current
			count +=1

		for x,i in enumerate(self.players):
			i.collect()
			print(f"player {x}'s stack size is: {i.stack}")
