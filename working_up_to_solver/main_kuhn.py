'''
Going to try and add all the percentages
'''
class Kuhn:
    def __init__(self,epochs=1000):
        self.epochs = epochs
        self.num_posisble_actions = 4
        self.cards = [0,1,2]
        self.fta_strat = [[0.5 for i in range(self.num_posisble_actions)]
                          for i in range(len(self.cards))]
        self.sta_strat = [[0.5 for i in range(self.num_posisble_actions)]
                          for i in range(len(self.cards))]
        self.strat_sum_fta = [[0 for i in range(4)] for x in range(3)]
        self.strat_sum_sta = [[0 for i in range(4)] for x in range(3)]

        self.train()
        self.print_results()

    def print_results(self):
        print("-"*50)
        cardDic = {0:"Jack",1:"Queen",2:"King"}
        actions = {0:"Check",1:"Bet", 2:"Fold", 3: "Call"}
        for i, card in enumerate(self.fta_strat):
            print(f"FIRST TO ACT STRATEGY FOR {cardDic[i]}")
            print("-"*50)
            for x,action in enumerate(card):
                print(f"{actions[x]} at a rate of: {action*100:.2f}%")
                print("-"*50)
        actions = {0:"Check When Checked To", 1: "Bet When Checked To", 2: "Fold When Bet To",
                   3: "Call When Bet To"}
        print("-" * 50)
        for i,card in enumerate(self.sta_strat):
            print(f"SECOND TO ACT STRATEGY FOR {cardDic[i]}")
            print("-"*50)
            for x,action in enumerate(card):
                print(f"{actions[x]} at a rate of: {action*100:.2f}%")
                print("-"*50)



    def train(self):
        for _ in range(self.epochs):
            for card in self.cards:
                regret_fta = self.cfr_fta(card)
                regret_sta = self.cfr_sta(card)
                self.update(regret_fta,self.fta_strat[card],self.strat_sum_fta[card])
                self.update(regret_sta, self.sta_strat[card],self.strat_sum_sta[card])
            self.get_final_strat()

    def get_final_strat(self):
        for card in range(len(self.cards)):
            for i in range(len(self.strat_sum_fta[card])):
                self.fta_strat[card][i] = self.strat_sum_fta[card][i]/self.epochs
                self.sta_strat[card][i] = self.strat_sum_sta[card][i] / self.epochs


    def update(self,strat,current,strat_sum):
        first_sum = sum(strat[:2])
        second_sum = sum(strat[2:])
        if first_sum <= 0:
            current[0] = .5
            current[1] = .5
        else:
            current[0] = strat[0]/first_sum
            current[1] = strat[1]/first_sum
        if second_sum <=0:
            current[2] = .5
            current[3] = .5
        else:
            current[2] = strat[2]/second_sum
            current[3] = strat[3]/second_sum
        strat_sum[0] += current[0]
        strat_sum[1] += current[1]
        strat_sum[2] += current[2]
        strat_sum[3] += current[3]

    #try this way may need to include my current betting strategies
    def cfr_sta(self,card):
        regret_matching = [0 for i in range(4)]
        sta = self.sta_strat[card]
        for acard in self.cards:
            if acard != card:
                fta = self.fta_strat[acard]
                #fta[0] if card > acard else fta[0] * -1
                check_check = fta[0] * sta[0] if card > acard else fta[0] * sta[0] * -1
                #bet_call = 2 * fta[1] if card > acard else -2 * fta[1]
                bet_call = 2 * fta[1] * sta[3] if card > acard else -2 * fta[1] * sta[3]
                #bet_fold = fta[1]
                bet_fold = fta[1] * sta[2]
                #check_bet_call = 2 * fta[3] if card > acard else -2 * fta[3]
                check_bet_call = 2 * fta[0] * sta[1] * fta[3] if card > acard else -2 * fta[0] * sta[1] * fta[3]
                #check_bet_fold = fta[2]
                check_bet_fold = fta[0] * sta[1] * fta[2]

                ev_betting = check_bet_call + check_bet_fold
                regret_matching[0] += check_check - ev_betting
                regret_matching[1] += ev_betting - check_check
                regret_matching[2] += bet_fold - bet_call
                regret_matching[3] += bet_call - bet_fold
        regret_matching = [max(0,i) for i in regret_matching]
        return regret_matching

    def cfr_fta(self,card):
        fta = self.fta_strat[card]
        regret_matching = [0 for i in range(4)]
        for acard in self.cards:
            if acard != card:
                sta = self.sta_strat[card]
                #check_check = sta[0] if card > acard else -1 * sta[0]
                check_check = sta[0] * fta[0] if card > acard else -1 * sta[0] * fta[0]
                #check_bet_fold = sta[1] * -1
                check_bet_fold = fta[0] * sta[1] * fta[2] * -1
                #check_bet_call = sta[1] * 2 if card > acard else -2 * sta[1]
                check_bet_call = fta[0] * sta[1] * fta[3] * 2 if card > acard else -2 * fta[0] * sta[1] * fta[3]
                #bet_fold = sta[2]
                bet_fold = fta[1] * sta[2]
                #bet_call = sta[3] * 2 if card > acard else -2 * sta[3]
                bet_call = fta[1] * sta[3] * 2 if card > acard else -2 * sta[3] * fta[1]

                ev_check = check_check + check_bet_call + check_bet_fold
                ev_bet = bet_fold + bet_call

                regret_matching[0] += ev_check - ev_bet
                regret_matching[1] += ev_bet - ev_check
                regret_matching[2] += bet_fold - bet_call
                regret_matching[3] += bet_call - bet_fold
        regret_matching = [max(0,i) for i in regret_matching]

        return regret_matching

kuhn = Kuhn()
