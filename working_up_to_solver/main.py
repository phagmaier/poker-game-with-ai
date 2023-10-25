'''
will try and run but I'm pretty sure i'll have to add shit to the
maybe both villian and hero ev because i'm not sure if I should and should't
include I guess the percentage or odds that that player bets to get you there
pluss to update you might want to see the regret of chosing x instead of y
for instance chosing check instead of y
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
        return [ev_check_check,ev_check_bet,ev_bet_fold,ev_bet_call]


    def ev_calc(self, hero_strat,hero_card):
        ev_check_call = []
        ev_check_fold = []
        for i in self.cards:
            if i == hero_card:
                #originall had it as none but this should make it easier to sum
                ev_check_call.append(0)
                ev_check_fold.append(0)
            else:
                #You do need to add how often villian is checking cause you need to know how often he's doing it with worse/better hands
                #ev_check_call.append(2*hero_strat[3] * self.vill_strat[i][1]) if hero_card>i else ev_check_call.append(-2 * hero_strat[3] * self.vill_strat[i][1])
                ev_check_call.append(2 * self.vill_strat[i][1]) if hero_card > i else ev_check_call.append(-2 * self.vill_strat[i][1])
                #ev_check_fold.append(-1 * hero_strat[2] * self.vill_strat[i][1])
                ev_check_fold.append(-1 * self.vill_strat[i][1])

        check = []
        bet = []
        call = []
        fold = []
        for card,i in enumerate(self.vill_strat):
            if card != hero_card:
                check.append((i[0],1)) if card < hero_card else check.append((i[0],-1))
                bet.append(i[1])
                fold.append((i[2],-1))
                call.append((i[3],2)) if card < hero_card else call.append(i[3],-2)
            else:
                check.append(None)
                bet.append((None))
                fold.append(None)
                call.append(None)


        ev_check = sum([(c * cp) + (b * cf) + (b * cc) for (c,cp),b,cf,cc in zip(check,bet,ev_check_fold,ev_check_call) if c != None])
        ev_bet = sum([c*cp + f*fp for (c,cp),(f,fp) in zip(call,fold) if c != None])

        return [ev_check,ev_bet,sum(ev_check_fold),sum(ev_check_call)]






    def train(self):
        for _ in range(self.epochs):
           self.cfr()


