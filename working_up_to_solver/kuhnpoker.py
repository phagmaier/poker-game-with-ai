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
        if hero > vill:
            check_check = self.hero_strat[hero][0] * self.villian_strat[vill][0]
            bet_fold = self.hero_strat[hero][1] * self.villian_strat[vill][0]
            bet_call = (self.hero_strat[hero][1] * self.villian_strat[vill][1])
            check_bet_fold = self.hero_strat[hero][0] * self.villian_strat[vill][1] * self.hero_strat[hero][0]
            check_bet_call = 2 * (self.hero_strat[hero][0] * self.villian_strat[vill][1] * self.hero_strat[hero][1])

            #NOW I'M JUST GETTING THE EV
            ev_check_check = check_check * check_check
            ev_bet_fold = bet_fold * bet_fold
            ev_bet_call = (bet_call * bet_call) * 2
            ev_check_bet_fold = -1* (check_bet_fold * check_bet_fold)
            ev_check_bet_call = 2 * (check_bet_call * check_bet_call)
        else:
            check_check = self.hero_strat[hero][0] * self.villian_strat[vill][0]
            bet_fold = self.hero_strat[hero][1] * self.villian_strat[vill][0]
            bet_call = self.hero_strat[hero][1] * self.villian_strat[vill][1]
            check_bet_fold = self.hero_strat[hero][0] * self.villian_strat[vill][1] * self.hero_strat[hero][0]
            check_bet_call = self.hero_strat[hero][0] * self.villian_strat[vill][1] * self.hero_strat[hero][1]

            #NOW I'M JUST GETTING THE EV
            ev_check_check = -1 * (check_check * check_check)
            ev_bet_fold = bet_fold * bet_fold
            ev_bet_call = -2 * (bet_call * bet_call)
            ev_check_bet_fold = -1 * (check_bet_fold * check_bet_fold)
            ev_check_bet_call = -2 * (check_bet_call * check_bet_call)

        #NOW I'M UPDATING THE CURRENT STRAT HAVE TO WAIT TO "PUBLISH" CHANGES FOR HERO
        self.update(ev_check_check,ev_check_bet_fold,ev_check_bet_call,ev_bet_fold,ev_bet_call)


    def update(self,check_check,check_bet_fold, check_bet_call,bet_fold, bet_call):
        self.hero_updates[0] += check_check + check_bet_fold + check_bet_call
        self.hero_updates[1] += bet_call + bet_fold
        self.hero_updates[2] += check_bet_fold
        self.hero_updates[3] += check_bet_call

        self.vill_updates[0] += -1 * check_check
        self.vill_updates[1] += -1 * (check_bet_call + check_bet_fold)
        self.vill_updates[2] += -1 * bet_fold
        self.vill_updates[3] += -1 * bet_call

    def update_strat(self,arr,changes):
        for i in range(len(arr)):
            arr[i] = min(1,max(0,arr[i]+changes[i]))
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
            for i in range(len(self.hero_strat)):
                print(f"{bet_check[i]} at a frequency of {self.hero_strat[i]}")

        fold_call = {0:"Check when checked to", 1:"Bet when checked to", 2: "Fold when bet to", 3:"Call when bet to"}
        for card in range(len(self.cards)):
            print(f"SECOND PLAYER TO ACT STRAT FOR CARD: {card_dic[card]}")
            for i in range(len(self.villian_strat)):
                print(f"{fold_call[i]} at a frequency of {self.villian_strat[i]}")

kuhn = Poker(1000)
