'''
Ok so currently I use regret but it's actually best to subtract from the optimal strat
for CFRM typically positive regret means you regret somethin and you ignore or don't use negative for
updating in my case you will only update with negative regrets
and for each card in a strategy the regret is going to be the regret of not chosing the optimal strategy or optimal action
At each stage
So because you have bet and check and then subtrees you'll need to find what would have been best between betting and checking and then
you add the difference between the best play and the subotimal one and adjust accordingly this will be the difference
You then do this with the subtrees in the game branch
'''

class Kuhn:
    def __init__(self,epochs):
        self.epochs = epochs
        self.cards = [0,1,2] #Jack,Queen,King
        #For the strats you have a uniform strat to start 0 index is check
        #1 index is bet, 2 index is fold if check_bet 3 is call when check bet
        self.hero_strat = [[.5 for i in range(4)] for x in range(len(self.cards))]
        #first two are how to act when chet to 0 = fold 1 = call last two are same but when bet to
        self.vill_strat = [[.5 for i in range(4)] for x in range(len(self.cards))]

    def cfr(self):
        for hero_card in range(len(self.hero_strat)):
            hero_updates = self.ev_calc(self.hero_strat[hero_card], hero_card)
            vill_updates = self.ev_calc_vill(self.vill_strat[hero_card],hero_card)
            self.update(hero_updates,vill_updates,self.hero_strat[hero_card],self.vill_strat[hero_card])

    def update(self,hero_update,vill_update,hero_strat,vill_strat):
        for i in range(len(hero_update)):
            hero_strat[i] += hero_update[i]
            vill_strat[i] += vill_update[i]
        total_hero1 = sum(hero_strat[:2])
        total_hero2 = sum(hero_strat[2:])
        total_vill1 = sum(vill_strat[:2])
        total_vill2 = sum(vill_strat[2:])
        for i in range(len(hero_update)):
            if i < 2:
                hero_strat[i] = min(.999,max(0.001,hero_strat[i])) / total_hero1
                vill_strat[i] = min(.999,max(0.001,vill_strat[i])) / total_vill1

            else:
                hero_strat[i] = min(.999,max(0.001,hero_strat[i])) / total_hero2
                vill_strat[i] = min(.999,max(0.001,vill_strat[i])) / total_vill2

    def ev_calc_vill(self,vill_strat,vill_card):
        ev_check_check = 0
        ev_check_bet = 0
        ev_bet_fold = 0
        ev_bet_call = 0

        for card,i in enumerate(self.hero_strat):
            if i != vill_card:
                ev_check_check += i[0] if card < vill_card else -1 * i[0]
                ev_check_bet += 2 * i[3] if i < vill_card else -2 * i[3]
                ev_check_bet += i[2]
                #Pretty sure this should just be -1
                ev_bet_fold += -1 * i[1]
                ev_bet_call += -2 * i[1] if i > vill_card else 2 * i[1]
        ev = [ev_check_check, ev_check_bet, ev_bet_fold, ev_bet_call]
        i=0
        for i,x in zip(ev, vill_strat):
            ev[i] = i - (x*i)
            i+=1
        return ev

    def ev_calc(self, hero_strat,hero_card):
        ev = [0 for i in range(4)]
        check_check = 0
        bet_call = 0
        for card in self.cards:
            strat = self.vill_strat[card]
            if card != hero_card:
                check_check = 1 * strat[0] if card < hero_card else -1 * strat[0]
                #this could be wrong maybe it's just supposed to be -1
                check_bet_fold = -1 * strat[1]
                check_bet_call = 2 * strat[1] if card < hero_card else -2 * strat[1]
                bet_fold = 1 * strat[2]
                bet_call = 2 * strat[3] if card < hero_card else -2 * strat[3]
                ev[0] += check_check + check_bet_fold + check_bet_call
                ev[1] += bet_fold + bet_call
                ev[2] += bet_fold
                ev[3] += bet_call
        #Going to get the regret now for each of these actions
        #ok so the CFRM is the difference between always choising x and choising it at the rate you do
        #you may also want to include the value that could have been gotten by bettig idk though
        i = 0
        for i,x in zip(ev,hero_strat):
            ev[i] = i - (x * i)
            i+=1
        return ev



    def train(self):
        for _ in range(self.epochs):
           self.cfr()

