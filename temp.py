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