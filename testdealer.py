from dealer import Dealer

dealer = Dealer(3)

x = dealer.deal_preflop()

print(len(x))

flop = dealer.deal_flop()
print(len(flop))
print('flop')
for i in flop:
	print(i)

turn = dealer.deal_turn()
print('turn')
print(turn)