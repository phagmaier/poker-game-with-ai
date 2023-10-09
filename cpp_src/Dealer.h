//
// Created by Parker Hagmaier on 10/6/23.
//

#ifndef SEE_WHAT_S_WRONG_DEALER_H
#define SEE_WHAT_S_WRONG_DEALER_H
#include "Card.h"
#include <map>
#include <tuple>

class Dealer {
public:
    Dealer(int num=1);
    void make_deck();
    //~Dealer();
    void reset();
    std::vector<std::tuple<Card,Card>> deal_preflop();
    std::tuple<Card,Card,Card> deal_flop();
    Card deal_turn();
    Card deal_river();
    std::map<int,int> get_value_count();
    std::map<int,int> get_board_pairs();
    //If not possible set int to like 0 or -1
    std::tuple<char,int> get_poss_flush();

private:
    //should probably be a pointer?
    Card deck[52];
    int pos;
    std::map<char,int> flush_count;
    std::map<int,int> value_count;
    std::map<int,int> board_pairs;
    //unsure if community truly used
    Card community[5];
    int num_players;
};


#endif //SEE_WHAT_S_WRONG_DEALER_H
