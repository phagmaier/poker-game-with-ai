from game import Game

if __name__ == '__main__':
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
		break