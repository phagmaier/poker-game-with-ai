from Newcards import Card
'''
NEED TO RESET WAGERED AT THE END OF EACH ROUND
BECAUSE WHEN YOU BET IT'S THE TOTAL AMOUNT YOU BET IN THIS ROUND
YOU ACTUALLY DON'T TAKE THE MONEY OUT OF THE STACK UNTIL THE END OF THE BETTING ROUND
DON'T THINK YOU NEED IS_BB 
ALSO MAKE SURE THAT YOU TURN SELF.IS_SB TO OFF AT THE END OF EACH BET
WILL PROBABLY NEED A VARIABLE FOR DISPLAY PURPOSES IN THE FUTURE THAT SHOWS CURRENT STACK
BUTT THAT'S EASY AND SINCE YOU AREN'T DOING THE WEB SHIT YET YOU WANT TO MAKE THE A.I BOT
SAVE THIS FOR LATER TILL YOU WORK THIS OUT
'''

class Player:
	def __init__(self,stack=100, bb=1,sb=.5):
		self.bb = bb
		self.sb = sb
		self.card1 = None
		self.card2 = None
		self.left_val = None
		self.right_val = None
		self.left_suit = None
		self.right_suit = None
		self.stack = 100
		self.wagered = 0
		self.is_sb = False
		self.suit_count = {'S':0,'D':0,"H":0,"C":0}

	def __str__(self):
		return f"Card 1: {str(self.card1)}  Card 2: {str(self.card2)}"

	def return_hand(self):
		return (self.card1,self.card2)

	def pair(self):
		if left.val == right_val:
			return left.val
		return 0

	def print_cards(self):
		self.card1.print_visuals()
		self.card2.print_visuals()

	def get_suits(self):
		#maybe change to set
		return suit_count


	def get_hand(self, hand):
		self.card1 = hand[0]
		self.card2 = hand[1]
		self.left_val = hand[0].value
		self.right_val =hand[1].value
		self.left_suit = hand[0].suit
		self.right_suit =hand[1].suit
		self.suit_count[self.right_suit] +=1
		self.suit_count[self.left_suit] +=1

	#like 99% sure you don't need is_bb so commenting it out
	def pay_blinds(self,amount,blind_type):
		if self.stack >= amount:
			self.wagered += amount
			#we don't take out of stack yet
			#self.stack -= amount
			if blind_type == 'sb':
				self.is_sb = True
			#elif blind_type == 'bb':
				#self.is_bb = True
			return self.wagered, False
		else:
			self.wagered = self.stack 
			self.stack = 0
			return self.wagered, True

	def get_action(self, prev_bet, pot_size):
		#MADE CHANGES HERE in # #  I preversed original
		#THINK WHAT I MESSED UP ON IS SB CAN'T CHECK 
		#AND BLINDS CAN'T BET 0
		#####################################
		'''
		if self.is_bb or self.is_sb:
			prev_bet -= self.wagered
			self.is_bb = False
			self.is_sb = False
		'''
		#####################################
		valid = False
		while not valid:
			print("Please select one of the following options (case doesn't matter) \nand then press the Enter key: ")
			print("Press F to fold")
			print("Press A or a to go all in")
			print("Press C to check or call")
			print("Enter a number to raise. If you enter a decimal we will raise that percentage of the pot")
			print("Unless you have less than a big blind in which case you are all in regardless")
			print("Raises must be at least a big blind or the ammount of the previous raise")
			action = input("Please make a selection: ")
			valid, bet,all_in,folded, action_taken = self.parse_action(action, prev_bet, pot_size)
		self.is_sb = False
		return bet,all_in,folded,action_taken

	# Because it makes my life easier to mark false if they folded on folds gonna say False
	def parse_action(self, action,prev_bet,pot_size):
		if action == 'A' or action == 'a':
			return self.all_in()
		elif action == 'c' or action == 'C':
			#checking
			if not prev_bet and not self.is_sb:
				return True,None,False,True, 'Check'
			else:
				return self.call(prev_bet)
		elif action == 'F' or action == 'f':
			return True,None,False,False, "Fold"
		else:
			try:
				action = float(action)
				if action == self.stack or action * pot_size == self.stack or self.stack < 1:
					return self.all_in()
			except:
				print("NOT A VALID CHOICE!")
				return False,None,None,None,None
			return self._raise(action,prev_bet,pot_size)
				
	def all_in(self):
		self.wagered = self.stack
		self.stack = 0
		return True,self.wagered, True, True, f"All in! for {self.wagered}"

	def call(self, amount):
		if self.is_sb and not amount:
			amount = self.bb - self.sb
		if amount >= self.stack:
			return self.all_in()
		else:
			self.wagered = amount
			return True,self.wagered, False,True, f"Call {self.wagered}"

	def _raise(self, action,prev_bet,pot_size):
		min_bet = prev_bet * 2 if prev_bet else self.bb
		if action < 1:
			bet = action * pot_size
			if pot_size > 0 and bet >= min_bet and bet < self.stack:
				self.wagered = bet
				return True,self.wagered,False,True, f"Raise to {self.wagered}"
			else:
				print("NOT A VALID CHOICE!")
				return False, None, None,None,None

		else:
			if action >= min_bet and action < self.stack:
				self.wagered = action
				return True, self.wagered,False,True,f"Raise to {self.wagered}"
			else:
				print("NOT A VALID CHOICE!")
				return False,None,None,None,None

	def collect(self):
		self.stack -= self.wagered
		self.wagered = 0

