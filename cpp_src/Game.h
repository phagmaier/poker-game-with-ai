//
// Created by Parker Hagmaier on 10/6/23.
//

#ifndef SEE_WHAT_S_WRONG_GAME_H
#define SEE_WHAT_S_WRONG_GAME_H
#include <iostream>
#include <vector>
#include "Player.h"
#include "Dealer.h"
#include <map>
#include <string>
#include <string>
#include "helperfunctions.h"
#include <algorithm>
#include <set>

class Game {
public:
    Game(int num, float starting_stack, float b_b, float s_b);
    void change_blinds();
    void preflop();
    void street_preflop();
    void street();
    void reset();
    void payout(std::vector<std::tuple<int,std::tuple<float, std::string>>> end_players);
    void payouts_blinds(std::vector<std::tuple<int,std::tuple<float, std::string>>> end_players);
    std::vector<std::tuple<int,std::tuple<float,std::string>>> get_hand_strength();
    std::tuple<float,std::string> hand_strength(Player player);
    float apair(Player player);
    float flush(Player player);
    float straight_flush(std::vector<int> flush_cards);
    void create_straights();
    float astraight(Player player);
    //probably won't need these using this so i don't get error with
    //community cards;
    void flop();
    void turn();
    void river();
    float high_card(Player player);
    bool hand_over();
private:
    int num_players;
    float bb;
    float sb;
    std::vector<Player> players;
    int utg;
    int dealer_button;
    Dealer dealer;
    int sb_pos;
    int bb_pos;
    float pot;
    float blinds;
    std::vector<bool> all_in;
    std::vector<bool> in_hand;
    int flush_count;
    char flush_suit;
    float sb_paid;
    float bb_paid;
    bool blind_payouts;
    std::map<std::string,int> hand_rankings;
    Card community_cards[5];
    int straights[10][5];
};




#endif //SEE_WHAT_S_WRONG_GAME_H
