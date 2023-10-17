import random
from player import Player
from game import Game
from dealer import Dealer
from cards import Card
from visuals import Viz_Cards


def game_loop(game):

        print(f"big blind position{game.bb_pos}")
        print(f"small blind position{game.sb_pos}")

       #PREFLOP
        print("PREFLOP")
        game.preflop()
        print("PLAYER HANDS:")
        for i,player in enumerate(game.players):
            print(f"PLAYER {i}S HAND IS: ")
            flop_viz = Viz_Cards(player.card1,player.card2)
            print(flop_viz())
            #print(player)
        print()
        print(f"THE POT BEFORE PRFLOP ACTION IS: {game.pot}")
        game.street_preflop()
        game.street_reset()
        #print([i.amount_to_win for i in game.players])
        if game.hand_over():
            game.payout(game.get_player())
            game.reset()
            return
        
        #FLOP
        print("FLOP")
        game.community_cards = game.dealer.deal_flop() #Should probably just make a flop function
        print("THE FLOP IS:")
        flop_viz = Viz_Cards(*game.community_cards)
        print(flop_viz())
        game.street()
        game.street_reset()
        if game.hand_over():
            game.payout(game.get_player())
            game.reset()
            return
            

        print("TURN")
        #TURN
        game.dealer.deal_turn()
        print("THE TURN IS:")
        turn_viz = Viz_Cards(*game.community_cards)
        print(turn_viz())
        game.street()
        game.street_reset()
        if game.hand_over():
            game.payout(game.get_player())
            game.reset()
            return
            

        print("RIVER")
        #RIVER
        game.dealer.deal_river()
        print("THE RIVER IS:")
        river_viz = Viz_Cards(*game.community_cards)
        print(river_viz())
        game.street()
        game.street_reset()
        print("AMOUNT EACH PLAYER CAN WIN")
        for i in game.players:
            print(i.amount_to_win)
        if game.hand_over():
            game.payout(game.get_player())
            game.reset()
            return
            
        else:
            game.flush_suit, game.flush_count = game.dealer.get_poss_flush()
            hand_strengths = game.get_hand_strengths()
            game.payout(hand_strengths, True)
            game.reset()
            return


if __name__ == '__main__':


    random.seed(69)
    game = Game(3,100,1,.5)

    game_loop(game)


    
        






    
    
