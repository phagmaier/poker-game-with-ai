from cards import Card
'''
THIS CLASS CREATES A MORE INTERESTING VISUALS FOR THINGS LIKE FLOP RIVER ETC...
'''
class Viz_Cards:
    card_viz = """\
    ┌─────────┐
    │{rank: <2}       │
    │         │
    │         │
    │    {suit: <2}   │
    │         │
    │         │
    │       {rank: >2}│
    └─────────┘
    """

    name_to_symbol = {
        'S': '♠',
        'D': '♦',
        'H': '♥',
        'C': '♣',
    }
    val_to_symbol = {
    	14: 'A',
    	13: 'K',
    	12: 'Q',
    	11: 'J',
    	10: '10',
    	9: '9',
    	8: '8',
    	7: '7',
    	6: '6',
    	5: '5',
    	4: '4',
    	3: '3',
    	2: '2'
    }

    def __init__(self, *cards):
        self.cards = cards

    def __call__(self):
        return self.join_lines(map(self.card_to_string, self.cards))

    def join_lines(self, strings):
        liness = [string.splitlines() for string in strings]
        return '\n'.join(''.join(lines) for lines in zip(*liness))

    def card_to_string(self, card):
        rank = self.val_to_symbol[card.value]
        return self.card_viz.format(rank=rank, suit=self.name_to_symbol[card.suit])
'''
# Example usage:
card1 = Card('S', 14)
card2 = Card('H', 13)
card3 = Card('H', 12)

viz = Viz_Cards(card1, card2, card3)
print(viz())

rrr = [card1,card2,card3]

viz = Viz_Cards(*rrr)
print(viz())
'''