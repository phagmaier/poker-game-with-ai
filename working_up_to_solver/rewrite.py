'''
Ok The problem is you need to go through all the possabilties for the hero
and also for the villian so you need to see what happens when they have a king their check frequency
and then the total amount you win from all that
'''

import random
class Poker:
    def __init__(self,epochs):
        self.epochs = epochs
        self.cards = [0,1,2]
        self.hero_strat = [[.5 for x in range(4)] for i in range(len(self.cards))]
        self.villian_strat = [[.5 for x in range(4)] for i in range(len(self.cards))]
        #check is 0 bet is 1 fold is 0 call is 1
        self.hero_updates = [0 for i in range(4)]
        #0-1 inclusive is checked to 0 is check 1 is bet
        #2-3 inclusive is bet to 0 is fold 1 is call
        self.vill_updates = [0 for i in range(4)]
        self.train()

    def train(self):
        for epoch in range(self.epochs):
            for hero in self.cards:
                for vill in self.cards:
                    if vill != hero:
                        self.cfrm(hero,vill)
                        #print("UPDATING VILLIAN STRAT")
                        #print(f"THE CURRENT STRAT IS: {self.villian_strat}")
                        self.update_strat(self.villian_strat[vill],self.vill_updates)
                        #print(f"The new strat is: {self.villian_strat}")
                #print("Updating hero strats")
                #print(f"The current strat is: {self.hero_strat}")
                self.update_strat(self.hero_strat[hero],self.hero_updates)
                #print(f"the new strat is: {self.hero_strat}")
        self.print_results()

        # Need to get the odds first and then you'll do the actual ev
    def cfrm(self,hero,vill):
        hero_strat = self.hero_strat[hero]
        vill_strat = self.villian_strat[vill]
        store_ev_vill = [0 for i in range(4)]
        store_ev_hero = [0 for i in range(4)]
        if hero > vill:
            #PAYOUTS HERO
            check_check = 1
            check_bet_fold = -1
            check_bet_call = 2
            bet_fold = 1
            bet_call = 2

        else:
            check_check = -1
            check_bet_fold = -1
            check_bet_call = -2
            bet_fold = 1
            bet_call = -2

        store_ev_hero[0] += (vill_strat[0] * check_check) + (vill_strat[1] * hero_strat[1] * check_bet_call)
        store_ev_hero[0] += (vill_strat[1] * hero_strat[0] * check_bet_fold)
        store_ev_hero[1] += (vill_strat[2] * bet_fold) + (vill_strat[3] * bet_call)
        store_ev_hero[2] += hero_strat[2] * check_bet_fold
        store_ev_hero[3] += hero_strat[3] * check_bet_call

        store_ev_vill[0] += vill_strat[0] * check_check * -1
        store_ev_vill[1] += (hero_strat[2] * check_bet_fold * -1) + (hero_strat[3] * check_bet_call * -1)
        store_ev_vill[2] += (vill_strat[2] * bet_call * -1)
        store_ev_vill[3] += (vill_strat[3] * bet_fold * -1)

        self.hero_updates[0] += store_ev_hero[0] - store_ev_hero[1]
        self.hero_updates[1] += store_ev_hero[1] - store_ev_hero[0]
        self.hero_updates[2] += store_ev_hero[2] - store_ev_hero[3]
        self.hero_updates[3] += store_ev_hero[3] - store_ev_hero[2]

        self.vill_updates[0] += store_ev_vill[0] - store_ev_vill[1]
        self.vill_updates[1] += store_ev_vill[1] - store_ev_vill[0]
        self.vill_updates[2] += store_ev_vill[2] - store_ev_vill[3]
        self.vill_updates[3] += store_ev_vill[3] - store_ev_vill[2]




    def update_strat(self,arr,changes):
        for i in range(len(arr)):
            arr[i] = min(1,max(0.001,arr[i]+changes[i]))
            changes[i] = 0
        total1 = sum(arr[:2])
        total2 = sum(arr[2:])
        for i in range(2):
            arr[i] = arr[i]/total1
        for i in range(2,4):
            arr[i] = arr[i]/total2

    def print_results(self):
        bet_check = {0:"check",1:"bet", 2:"check_bet_fold", 3:"Check_bet_call"}
        card_dic = {0:"Jack",1:"Queen",2:"King"}
        for card in range(len(self.cards)):
            print(f"FIRST PLAYER TO ACT STRAT FOR CARD: {card_dic[card]}")
            for i in range(len(self.hero_strat[card])):
                print(f"{bet_check[i]} at a frequency of {self.hero_strat[card][i]}")

        fold_call = {0:"Check when checked to", 1:"Bet when checked to", 2: "Fold when bet to", 3:"Call when bet to"}
        for card in range(len(self.cards)):
            print(f"SECOND PLAYER TO ACT STRAT FOR CARD: {card_dic[card]}")
            for i in range(len(self.villian_strat[card])):
                print(f"{fold_call[i]} at a frequency of {self.villian_strat[card][i]}")

    def run_sim(self, how_many_hands=100):
        win_loss_fta = 0
        win_loss_sta = 0
        card_dic = {0:"Jack",1:"Queen",2:"King"}
        first_action = {0:"Bet", 1: "Check"}
        for _ in how_many_hands:
            fta,sta = random.sample(self.cards, 2)
            print(f"First player to act has a: {card_dic[fta]}")
            print(f"Second player to act has a: {card_dic[sta]}")
            first_choice = random.random()
            action = 1 if first_choice > self.hero_strat[fta][0] else 0
            print(f"Player 1 {first_action[action]}")
            choices = self.villian_strat[sta][:2] if action == 0 else self.villian_strat[sta][2:]
            next_action = random.random()
            action = choices[0] if next_action < choices[0] else choices[1]
            '''
            NEED IF STATMENT SO THAT IF IT'S NOT A TERMINAL BRANCH YOU KEEP GOING
            YOU ALSO NEED TO DEPENDING ON WHERE YOU ARE AND WHO WINS ALLOCATE
            FOR BOTH WIN_LOSS FOR FTA AND STA if you lose subtract from win_loss_x
            if win add win_loss_x do it for both
            '''




kuhn = Poker(100)
