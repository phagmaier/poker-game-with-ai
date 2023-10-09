//
// Created by Parker Hagmaier on 10/6/23.
//

#ifndef SEE_WHAT_S_WRONG_PLAYER_H
#define SEE_WHAT_S_WRONG_PLAYER_H
#include <tuple>
#include "Card.h"
#include <map>
#include <string>
class Player {
public:
    Player(float stackk, float big_blind, float small_blind);
    void get_cards(std::tuple<Card,Card>hand);
    std::tuple<float,bool> pay_bb();
    std::tuple<float,bool> pay_sb();
    std::tuple<float,bool,bool,float,std::string> get_action(float prev_bet, float pot_size,float min_bet);
    std::tuple<bool,float,bool,bool,float,std::string> parse_action(std::string action,float prev_bet,float pot_size,float min_bet);
    //this function returns valid, bet, all_in, in_hand, total, action_taken
    std::tuple<bool,float,bool,bool,float,std::string> call(float prev_bet);
    static std::tuple<bool,float,bool,bool,float,std::string> fold();
    std::tuple<bool,float,bool,bool,float,std::string> all_in();
    std::tuple<bool,float,bool,bool,float,std::string> bet(std::string action, float potsize, float min_bet);
    std::tuple<bool,float,bool,bool,float,std::string> raise(std::string action, float prev_bet, float potsize, float min_bet);
    //NEW: Just easier to return all False and 0's if rejected we essentially return nothing but invalid as false
    static std::tuple<bool,float,bool,bool,float,std::string> rejected();
    void reset_street();
    void reset();
    float get_stack();
    void add_to_stack(float num);
    float get_amount_to_win();
    void reduce_amount_to_win(float amount);
    friend class Game;
private:
    Card hand1;
    Card hand2;
    int left_val;
    int right_val;
    char left_suit;
    char right_suit;
    std::map<char,int>suit_count;
    float stack;
    float bb;
    float sb;
    float wagered;
    float amount_to_win;
    float blind_adjustment;
};


#endif //SEE_WHAT_S_WRONG_PLAYER_H
