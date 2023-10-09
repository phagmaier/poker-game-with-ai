class Player:
	def __init__(self,stack,bb,sb):
		self.stack = stack
		self.bb = bb
		self.sb = sb
		self.card1 = None
		self.card2 = None
		self.left_val = None
		self.left_suit = None
		self.right_val = None
		self.right_suit = None
		self.suit_count = {'S':0,'D':0,"H":0,"C":0}
		self.wagered = 0
		self.amount_to_win = 0
		self.blind_adjustment = 0

	def get_cards(self,hand):
		self.card1,self.card2 = hand
		self.left_val,self.right_val = self.card1.value, self.card2.value
		self.left_suit,self.right_suit = self.card1.suit, self.card2.suit
		self.suit_count[self.right_suit] +=1
		self.suit_count[self.left_suit] +=1

	def pay_bb(self):
		if self.stack > self.bb:
			self.wagered = self.bb
			self.blind_adjustment = self.bb
			return self.bb,False
		else:
			self.wagered = self.stack
			self.stack = 0
			return self.wagered,True

	def pay_sb(self):
		if self.stack > self.sb:
			self.wagered = self.sb
			self.blind_adjustment = self.sb
			return self.sb,False
		else:
			self.wagered = self.stacks
			self.stack = 0
			return temp,True

	def get_action(self,prev_bet,pot_size,min_bet):
		valid = False
		while not valid:
			"""
			print("Please select one of the following options (case doesn't matter) \nand then press the Enter key: ")
			print("Press F to fold")
			print("Press A or a to go all in")
			print("Press C to check or call")
			print("Enter a number to raise. If you enter a decimal we will raise that percentage of the pot")
			print("Unless you have less than a big blind in which case you are all in regardless")
			print("Raises must be at least a big blind or the ammount of the previous raise")
			"""
			#print("BETTING STAGE WE ARE JUST CHECKING FOR NOW")
			#action = 'C'
			action = input("Please make a selection: ")
			valid,bet,all_in,in_hand,total,action_taken = self.parse_action(action, prev_bet, pot_size,min_bet)
			if not valid:
				print("NOT A VALID SELECTION PLEASE TRY AGAIN")
		self.blind_adjustment = 0
		return bet,all_in,in_hand,total,action_taken

	def parse_action(self,action,prev_bet,pot_size,min_bet):
		if action == 'c' or action == 'C':
			if not prev_bet and not self.wagered:
				return True,0,False,True, 0,f"CHECK"
			else:
				if prev_bet < self.stack:
					return self.call(prev_bet)
				else:
					return self.all_in()
		elif action == 'f' or action == 'F':
			return self.fold()

		if action == 'a' or action == 'A':
			return self.all_in()
		else:
			if not prev_bet:
				return self.bet(action,pot_size,min_bet)
			else:
				return self._raise(action,prev_bet,pot_size,min_bet)

	#valid,bet,all_in,in_hand,total,action_taken			
	def call(self,prev_bet):
		temp = prev_bet - self.wagered
		if temp == 0:
			return True,0,False,True, 0, f"CHECK"
		if temp < 0:
			if temp == -self.bb:
				return True,0,False,True, 0,f"CHECK"
			else:
				if self.bb < self.stack:
					self.wagered = self.bb
					return True,self.sb,False,True, self.wagered, f"CALL {self.sb}"
				else:
					return self.all_in()
		self.wagered += temp
		self.amount_to_win += temp + self.blind_adjustment
		return True,temp,False,True, self.wagered, f"CALL {self.wagered}"

	def all_in(self):
		if self.blind_adjustment and self.stack > self.bb:
			self.amount_to_win += self.stack - (self.wagered + self.blind_adjustment)
		else:
			self.amount_to_win = self.stack - self.wagered
		temp = self.stack - self.wagered
		self.wagered = self.stack
		return True, temp, True,True, self.wagered, f"ALL IN FOR: {self.wagered}"

	def _raise(self,action,prev_bet,pot_size,min_bet):
		try:
			action = float(action)
			if action < 1 and action > 0:
				bet = action * pot_size
				if bet > 2 * prev_bet:
					temp = bet - self.wagered
					self.wagered += temp

					self.amount_to_win += temp + self.blind_adjustment
					return True,temp,False,True,self.wagered,f"Raise to {self.wagered}"
				else:
					return False,0,None,None,None,None
			else:
				if action > min_bet:
					temp = action - self.wagered
					self.wagered += temp
					self.amount_to_win += temp
					return True,temp,False,True,self.wagered,f"Raise to {self.wagered}"
				else:
					return False,None,None,None,None,None
		except:
			return False,0,None,None,None,None
	#valid,bet,all_in,in_hand,total,action_taken
	def bet(self,action,pot_size,min_bet):
		try:
			action = float(action)
			if action >= min_bet:
				if action >= self.stack:
					return self.all_in()
				temp = action - self.wagered
				self.wagered += temp
				self.amount_to_win += (temp + self.blind_adjustment)

				return True, temp,False,True,self.wagered, f"BET {self.wagered}"
			else:
				return False,0,None,None,None,None
		except:
			return False,0,None,None,None,None

	#valid,bet,all_in,in_hand, action_taken
	def fold(self):
		return True,0,False,False,0,"FOLD"



	def reset_street(self):
		self.stack -= self.wagered
		self.wagered = 0


	def reset(self):
		self.suit_count = {'S':0,'D':0,"H":0,"C":0}
		self.wagered = 0
		self.amount_to_win = 0

	def __str__(self):
		return f"Card 1: {str(self.card1)}  Card 2: {str(self.card2)}"

