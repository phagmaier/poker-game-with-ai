from Newcards import Card
import random

class Dealer:
	def __init__(self,players=2):
		self.num_players = players
		self.deck = self.make_deck()
		self.pos = 0
		self.flush_count = {i:0 for i in ['S', 'C', 'D', 'H']}
		self.value_count = {i:0 for i in range(2,15)}
		self.board_pairs = {}
		self.community = None

	def make_deck(self):
		suits = ['S', 'C', 'D', 'H']
		values = [i for i in range(2,15,1)]
		deck = []
		for suit in suits:
			for val in values:
				deck.append(Card(suit,val))
		return deck

	def reset(self):
		self.flush_count = {i:0 for i in ['S', 'C', 'D', 'H']}
		self.value_count = {i:0 for i in range(2,15)}
		self.pos = 0
		self.community = None
		self.board_pairs = {}
		random.shuffle(self.deck)

	def deal_preflop(self):
		random.shuffle(self.deck)
		self.pos = self.num_players *2
		return [(self.deck[i], self.deck[i+1]) for i in range(0,self.num_players * 2,2)]

	def deal_flop(self):
		self.community = [self.deck[i] for i in range(self.pos, self.pos+3)]
		for i in self.community:
			self.flush_count[i.suit] += 1
			self.value_count[i.value] += 1
			if self.value_count[i.value] > 1:
				self.board_pairs[i.value] = self.value_count[i.value]
		return self.community

	#THIS SHOULD BE FIXED
	def deal_turn(self):
		self.pos +=4
		new = self.deck[self.pos-1]
		self.community.append(new)
		self.flush_count[new.suit] += 1
		self.value_count[new.value] += 1
		if self.value_count[new.value] > 1:
				self.board_pairs[new.value] = self.value_count[new.value]
		return new

	#DO THE SAME FOR TURN AS YOU DO FOR DEAL RIVER
	def deal_river(self):
		new = self.deck[self.pos]
		self.flush_count[new.suit] += 1
		self.value_count[new.value] += 1
		if self.value_count[new.value] > 1:
				self.board_pairs[new.value] = self.value_count[new.value]
		return self.deck[self.pos]

	def get_value_count(self):
		return {i:[self.value_count[i]] for i in self.value_count if self.value_count[i] > 0}
		

	def get_board_pairs(self):
		return self.board_pairs

	def get_poss_flush(self):
		for i in self.flush_count:
			if self.flush_count[i] >=3:
				return i, self.flush_count[i]
		return None, None

	




		





