import random
from player import Player
from game import Game
from dealer import Dealer
if __name__ == '__main__':


	random.seed(42)
	game = Game(3,100,1,.5)

	print(f"big blind position{game.bb_pos}")
	print(f"small blind position{game.sb_pos}")

	#PREFLOP
	print("PREFLOP")
	game.preflop()
	print("PLAYER HANDS:")
	for player in game.players:
		print(player)
	print()
	print(f"THE POT BEFORE PRFLOP ACTION IS: {game.pot}")
	game.street_preflop()
	game.street_reset()
	if game.hand_over():
		game.payout(game.get_player())
		game.reset()
	
	#FLOP
	print("FLOP")
	game.community_cards = game.dealer.deal_flop() #Should probably just make a flop function
	game.street()
	game.street_reset()
	if game.hand_over():
		game.payout(game.get_player())
		game.reset()

	print("TURN")
	#TURN
	game.dealer.deal_turn()
	game.street()
	game.street_reset()
	if game.hand_over():
		game.payout(game.get_player())
		game.reset()

	print("RIVER")
	#RIVER
	game.dealer.deal_river()
	game.street()
	game.street_reset()
	print("AMOUNT EACH PLAYER CAN WIN")
	for i in game.players:
		print(i.amount_to_win)
	if game.hand_over():
		game.payout(game.get_player())
		game.reset()
	else:
		game.flush_suit, game.flush_count = game.dealer.get_poss_flush()
		hand_strengths = game.get_hand_strengths()
		game.payout(hand_strengths, True)
		game.reset()






	
	
