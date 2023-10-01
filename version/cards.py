class Card:
	def __init__(self,suit, value):
		self.suit = suit
		self.value = value
		self.value_string_dic = {14:"A",13:"K",12:"Q",11:"J",10:"T",9:"9",
		8:"8",7:"7",6:"6",5:"5",4:"4",3:"3",2:"2"}
		self.suit_string_dic = {'S':'♠', 'C':'♣', 'D':'♦', "H":'♥'}
		self.card_string = f"""\
┌─────────┐
│{self.value_string_dic[self.value]}        │
│         │
│         │
│    {self.suit_string_dic[self.suit]}    │
│         │
│         │
│       {self.value_string_dic[self.value]} │
└─────────┘
"""
	def print_visuals(self):
		print(self.card_string)
	def __str__(self):
		return f"{self.value_string_dic[self.value]}{self.suit_string_dic[self.suit]}"



