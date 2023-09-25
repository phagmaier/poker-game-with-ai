from NewDealer import Dealer
from Newcards import Card
from NewPlayer import Player
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
		#from strongest to weakest (counting five flush different because i'm an idiot)
		self.hand_rankings = {'SF':900,'Q':800,'FH':700,'F':600, '5F':500 ,'S':400,'T':300,
		'TP':3200,'P':100,'H':0}
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
			self.payout(self.in_hand[i])
		else:
			#self.get_winner()
			hand_strengths = self.get_hand_strengths()
			self.payout(hand_strengths,True)

	def reset(self):
		self.community_cards = []
		self.pot = 0
		self.player_bets = []
		self.in_hand = [True for _ in range(num_players)]
		self.all_in = [False for _ in range(num_players)]
		#need to check if anyone went broke and if so if they want to join
		#also want to ask broke players or any players with less than starting stacks
		#if they want to add back on 
		self.change_blinds()
		#maybe other stuff

	#just pass winning player and 
	def payout(self,players, multiple=False):
		if not multiple:
			self.players[player].stack += self.pot
			self.reset()

		#look atyour algo
		can_win = sum(self.in_hand)
		while can_win:
			players = sorted([players[i] for i in range(len(players)) if self.in_hand[i]], 
				key=lambda x: x[1])

			min_stack = min([self.player_bets[i] for i in range(self.num_players) if self.in_hand[i]])
			side_pot = min_sack * can_win
			self.pot -= side_pot #think this is right not 100% but 90% sure
			best_hand = players[-1]
			winners = [self.players[i[0]] for i in players if i[0] == best_hand]
			for p in winners:
				side_pot/len(winners)
			for player in players:
				self.players[player].stack -= min_stack
				if self.players[player].stack == 0:
					self.in_hand[player] = False
			if sum(self.in_hand) == 1:
				i = 0
				stop = False
				while not stop:
					if self.in_hand[i]:
						#Not sure if this will work
						self.players[i].stack += self.pot	
						stop = True
					i+=1
		self.reset()		

	#return 2 values in case of a five flush
	def possible_flush(self,player):
		suit,count = self.dealer.get_poss_flush()
		if suit:
			my_count = my_suits[suit]
			my_suits = player.get_suits()
			if count == 3 and my_count == 2:
				return self.get_flush(player,suit)
			if count == 4 and my_count >=1:
				return self.get_flush(player,suit)
			if count == 5:
				return self.five_flush(player,suit)
				pass
		return False, False

	#For five flush you just compare sum of hands to see whose is better
	def five_flush(self,player,suit):
		flush_cards = [i.value for i in self.community_cards if i.suit == suit] +\
		[i.value for i in player.return_hand() if i.suit == suit]
		flush_cards.sort(reverse=True)
		return sum(flush_cards[:5]), True

	def get_flush(self,player,suit):
		flush_cards = [i.value for i in self.community_cards if i.suit == suit] +\
		[i.value for i in player.return_hand() if i.suit == suit]
		flush_cards.sort()
		return flush_cards[-1], False

	def pairs_trips_fh_quads(self,player):
		#board_values = self.dealer.get_value_count()
		total_pairs = self.dealer.get_board_pairs()
		total_pairs[player.left_val] += 1
		total_pairs[player.right_val] += 1
		
		biggest_trips = 0
		pairs = []
		biggest_quads = 0
		biggest_pair = 0
		for i in total_pairs:
			amount = total_pairs[i]
			if amount>1:
				if amount == 4 and i > biggest_pair:
					biggest_quads = i
				elif amount == 3 and i > biggest_trips:
					biggest_trips = i
				else:
					pairs.append(i)
					if i> biggest_pair:
						biggest_pair = i
		if biggest_quads:
			return 'Q',biggest_quads
		if biggest_trips:
			if biggest_pair:
				return 'FH', (biggest_trips *10000) + (biggest_pair * 10)
			else:
				cards = [i.value for i in self.community_cards] + [player.left_val, player.right_val]
				temp = 0
				count = 0
				for i in cards:
					if i != biggest_trips:
						temp+=i
						count +=1 
						if count == 2:
							break
				return 'T', biggest_trips + 1/100 * temp
		if pairs:
			if pairs > 1:
				pairs.sort(reverse=True)
				tp = pairs[0:2]
				cards = [i.value for i in self.community_cards] + [player.left_val, player.right_val]
				cards.sort(reverse=True)
				temp = 0
				for i in cards:
					if i not in tp:
						temp = i
						break
				return 'TP', sum(pairs[0:2] + ((1/100) * temp))
			else:
				cards = [i.value for i in self.community_cards] + [player.left_val, player.right_val]
				cards.sort(reverse=True)
				temp = 0
				count = 0
				for i in cards:
					if i!= biggest_pair:
						temp+=i
						count +=1 
						if count == 4:
							break
				return 'p', biggest_pair + 1/100 * temp
		else:
			self.high_card(player)

	def high_card(self,player):
		all_cards = [i.val for i in community_cards] + [player.left_val, player.right_val]
		#all_cards = self.community_cards + [player.left_val, player.right_val]
		all_cards.sort(reverse=True)
		return 'H',sum(all_cards[0:5])

	def detect_straights(self, player):
		#will probably add a variable that keep track of all values dealt
		#for now this is fine we'll see how slow this is
		cards = [i.value for i in self.community_cards] + [player.left_val, player.right_val]
		cards.sort(reverse=True)
		if 14 == cards[0]:
			cards.append(1)
		i = 0
		while i< len(cards) -5:
			temp = cards[i:i+5]
			for straight in self.straights:
				if straight == temp:
					return straight[0]
			i+=1
		return False

	def create_straights(self):
		straights = [[i for i in range(i,i+5)][::-1] for i in range(1,11)]
		straights = straights[::-1]
		return straights


	#Determine out of active hands who the winner is
	def get_hand_strengths(self):
		return [(i,hand_strength(self.players[i])) for i,x in enumerate(self.in_hand) if self.in_hand[i]]
	

	def hand_strength(self,player):
		suit, count = self.dealer.get_poss_flush(player)
		if suit:
			maxx = self.straight_flush(player)
			if maxx:
				return 'SF',maxx
			maxx, type_of = self.possible_flush(player)
			if maxx:
				type_of_temp, temp_maxx = self.pairs_trips_fh_quads(player)
				return (type_of_temp, temp_maxx) if type_of_temp == 'Q' or type_of_temp == 'FH' else (type_of,maxx)

		type_of, maxx = self.pairs_trips_fh_quads()
		if type_of != 'FH' or type_of != 'Q':
			#type_of, maxx = 'S', self.detect_straights(player)
			temp = self.detect_straights(player)
			if temp:
				return 'S', temp
		return self.hand_rankings[type_of] + maxx 

	#checking shit multiple times should check for this in flush or something
	#also checks for royal flush
	def straight_flush(self,player):
		needed_suit = self.dealer.get_flush_suit()
		#you should be keeping track of all this to reduce the cost of doing all this
		if needed_suit:
			vals = [i.value for i in self.community_cards if i.suit == needed_suit]
			if player.left_suit == needed_suit:
				vals.append(player.left_val)
			if player.left_suit == needed_suit:
				vals.append(player.left_val)
			if vals >= 5:
				vals.sort(reverse=True)
				i = 0
				while i< len(cards) -5:
					temp = vals[i:i+5]
					for straight in self.straights:
						if temp == straight:
							if temp[0] == 14:
								return temp[0]
							return temp[0]
					i+=1
		False

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
					#end = current
					#prev_bet = bet if bet>prev_bet else prev_bet
					#prev_bet,end = (bet,current) if bet>prev_bet else (prev_bet,end)
					prev_bet,count = (bet,0) if bet>prev_bet else (prev_bet,count)

			current += 1 if current+1 < self.num_players else -current
			count +=1

		for i in self.players:
			i.collect()

if __name__ == '__main__':
	game = Game()
