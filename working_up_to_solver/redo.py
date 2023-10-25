class Kuhn:
    def __init__(self,epochs=100):
        self.epochs = epochs
        self.num_posisble_actions = 4
        self.cards = [0,1,2]
        self.fta_strat = [[0.5 for i in range(self.num_posisble_actions)]
                          for i in range(len(self.cards))]
        self.sta_strat = [[0.5 for i in range(self.num_posisble_actions)]
                          for i in range(len(self.cards))]

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
                self.update(regret_fta,regret_sta,card)

    def update(self,fta,sta,card):
        i=0
        while i < len(fta):
            if fta[i] > fta[i+1]:
                self.fta_strat[card][i] += fta[i]
            else:
                self.fta_strat[card][i+1] += fta[i+1]
            temp = self.fta_strat[card][i] + self.fta_strat[card][i+1]
            self.fta_strat[card][i] = self.fta_strat[card][i] / temp
            self.fta_strat[card][i+1] = self.fta_strat[card][i+1] / temp
            if sta[i] > sta[i+1]:
                self.sta_strat[card][i] += sta[i]
            else:
                self.sta_strat[card][i+1] += sta[i+1]

            temp = self.sta_strat[card][i] + self.sta_strat[card][i+1]
            self.sta_strat[card][i] = self.sta_strat[card][i] / temp
            self.sta_strat[card][i+1] = self.sta_strat[card][i+1] / temp
            i+=2


    #try this way may need to include my current betting strategies
    def cfr_sta(self,card):
        regret_matching = [0 for i in range(4)]
        sta = self.sta_strat[card]
        for acard in self.cards:
            if acard != card:
                fta = self.fta_strat[acard]
                check_check = sta[0] * fta[0] if card > acard else sta[0] * fta[0] * -1
                bet_call = 2 * fta[1] * sta[3] if card > acard else -2 * fta[1] * sta[3]
                bet_fold = fta[1] * sta[2] * -1
                check_bet_call = fta[0] * 2 * fta[3] * sta[1] if card > acard else -2 * fta[3] * sta[1] * fta[0]
                check_bet_fold = fta[0] * sta[1] * fta[2]

                ev_checkback = check_check
                ev_check_bet = check_bet_call + check_bet_fold
                ev_bet_fold = -1
                ev_bet_call = 2 if card > acard else -2

                regret_matching[0] += ev_checkback - ev_check_bet
                regret_matching[1] += ev_check_bet - ev_checkback
                regret_matching[2] += ev_bet_fold - ev_bet_call
                regret_matching[3] += ev_bet_call - ev_bet_fold
        return regret_matching



    def cfr_fta(self,card):
        fta = self.fta_strat[card]
        regret_matching = [0 for i in range(4)]
        for acard in self.cards:
            if acard != card:
                sta = self.sta_strat[card]
                check_check = fta[0] * sta[0] if acard > card else -1 * sta[0] * fta[0]
                check_bet_fold = -1 * sta[1] * fta[0] * fta[2]
                check_bet_call = fta[0] * sta[1] * fta[3] * 2 if card> acard else -2 * fta[0] * sta[1] * fta[3]
                bet_fold = sta[2] * -1 * fta[1]
                bet_call = fta[1] * sta[3] * 2 if card > acard else -2 * sta[3] * fta[1]

                ev_check = check_check + check_bet_call + check_bet_fold
                ev_bet = bet_fold + bet_call
                ev_bet_fold = -1
                ev_bet_call = -2 if card < acard else 2

                regret_matching[0] += ev_check - ev_bet
                regret_matching[1] += ev_bet - ev_check
                regret_matching[2] += ev_bet_fold - ev_bet_call
                regret_matching[3] += ev_bet_call - ev_bet_fold

        return regret_matching

kuhn = Kuhn()
