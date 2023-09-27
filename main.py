from game import Game
import random

'''
SOMEHOW MY COMMUNITY CARDS ARE GETTING FUCKED UP (BEFORE CHECKING FOR HAND TYPES)
YOU HAVE more than in community cards and you have a duplicate
'''

if __name__ == '__main__':
	random.seed(4)
	#num_players = int(input("How many players: "))
	#big_blind_size = float(input("Big blind size: "))
	#small_blind = .5 * big_blind_size
	#starting_stack_size = int(input("Enter all players starting stack size: "))
	num_players = 3
	big_blind_size = 1
	small_blind = .5 * big_blind_size
	num_players = 3
	starting_stack_size = 100

	game = Game(num_players, big_blind_size, small_blind,starting_stack_size)
	
	while True:
		game.gameloop()
		print(f"player 1 card 1: {game.players[0].card1}  card 2: {game.players[0].card2} ")
		print(f"player 2 card 1: {game.players[1].card1}  card 2: {game.players[1].card2} ")
		print(f"player 3 card 1: {game.players[2].card1}  card 2: {game.players[2].card2} ")
		break
	#PREFLOP
	'''
	print()
	print("PREFLOP")
	print()
	game.deal_cards()
	game.street(True)
	#FLOP
	print()
	print("FLOP")
	print()
	game.community_cards = game.dealer.deal_flop()
	game.street(False)
	#TURN
	print()
	print("TURN")
	print()
	game.dealer.deal_turn()
	game.street(False)
	print()
	print("RIVER")
	print()
	game.dealer.deal_river()
	game.street(False)
	game.flush_suit, game.flush_count = game.dealer.get_poss_flush()
	hand_strengths = game.get_hand_strengths()
	print()
	print('community cards')
	for i in game.community_cards:
		print(i)
	print()
	print("players hands:")
	for i,player in enumerate(game.players):
		print(f"PLAYER {i}s cards: {player.card1}  {player.card2}")

	print()
	print('HAND STRENGTHS')
	print()
	for i in hand_strengths:
		print(i)

	game.payout(hand_strengths,True)

	for i in game.players:
		print(i.stack)
		
	'''

#[13, 5, 6, 6, 14]