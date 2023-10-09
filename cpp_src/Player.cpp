//
// Created by Parker Hagmaier on 10/6/23.
//

#include "Player.h"
#include "Player.h"
#include <tuple>
#include "Card.h"
#include <map>

Player::Player(float stackk, float big_blind, float small_blind) :
        stack(stackk), bb(big_blind), sb(small_blind), hand1(Card{'l',-1}),
        hand2(Card{'l',-1}), left_val(-1), right_val(-1), left_suit('l'),
        right_suit(-1), suit_count({{'S',0}, {'D',0}, {'H',0},{'C',0}}),
        wagered(0), amount_to_win(0), blind_adjustment(0){}

void Player::get_cards(std::tuple<Card, Card> hand) {
    auto [card1, card2] = hand;
    left_val = card1.value;
    right_val = card2.value;
    left_suit = card1.suit;
    right_suit = card2.suit;
    suit_count[right_suit] += 1;
    suit_count[left_suit] += 1;
}

std::tuple<float,bool> Player::pay_bb(){
    if (stack > bb){
        wagered = bb;
        blind_adjustment = bb;
        return std::make_tuple(bb, false);
    }
    else{
        wagered = stack;
        stack = 0;
        return std::make_tuple(wagered,true);
    }
}

std::tuple<float,bool> Player::pay_sb(){
    if (stack > sb){
        wagered = sb;
        blind_adjustment = sb;
        return std::make_tuple(sb, false);
    }
    else{
        wagered = stack;
        stack = 0;
        return std::make_tuple(wagered,true);
    }
}
//this function returns bet, all_in, in_hand, total, action_taken
std::tuple<float,bool,bool,float,std::string> Player::get_action(float prev_bet, float pot_size,float min_bet){
    std::string action;
    bool valid = false;
    float bet;
    bool all_in;
    bool in_hand;
    float total;
    std::string action_taken;
    while(!valid){
        /*
        std::cout << "Please select one of the following options (case doesn't matter) \nand then press the Enter key\n";
        std::cout << "Press F to fold\n";
        std::cout <<"Press A or a to go all in\n";
        std::cout <<"Press C to check or call\n";
        std::cout<<"Enter a number to raise. If you enter a decimal we will raise that percentage of the pot\n";
        std::cout << "Unless you have less than a big blind in which case you are all in regardless\n";
        std::cout << "Raises must be at least a big blind or the amount of the previous raise\n";
         */
        std::cout << "Please make a selection:\n";
        std::cin >> action;
        std::tie(valid,bet,all_in,in_hand,total,action_taken) = parse_action(action,prev_bet,pot_size,min_bet);
        if (!valid){
            std::cout << "NOT A VALID SELECTION PLEASE TRY AGAIN\n";
        }
    }
    blind_adjustment = 0;
    return std::make_tuple(bet,all_in,in_hand,total,action_taken);
}

//this function returns valid, bet, all_in, in_hand, total, action_taken
std::tuple<bool,float,bool,bool,float,std::string> Player::parse_action(std::string action,
                                                                        float prev_bet,
                                                                        float pot_size,
                                                                        float min_bet)
{
    if (action == "c" || action == "C"){
        if (!prev_bet && !wagered){
            return std::make_tuple(true,0,false,true,0,"Check");
        }
        else{
            if (prev_bet < stack){
                //not implimented yet
                return call(prev_bet);
            }
            return all_in();

        }
    }
    else if (action == "f" || action == "F"){
        return fold();
    }
    else if (action == "a" || action == "A"){
        return all_in();
    }
    else{
        if (!prev_bet){
            return bet(action,pot_size,min_bet);
        }
        return raise(action,prev_bet,pot_size,min_bet);
    }

}

std::tuple<bool,float,bool,bool,float,std::string> Player::call(float prev_bet){
    float temp = prev_bet - wagered;
    if (!temp){
        return std::make_tuple(true,0,false,true,0,"CHECK");
    }
    if (temp < 0){
        if (temp == -bb){
            return std::make_tuple(true,0,false,true,0,"CHECK");
        }
        else{
            if (bb < stack){
                wagered = bb;
                std::string temp_str = "CALL " + std::to_string(sb);
                return std::make_tuple(true,sb,false,true,wagered,temp_str);
            }
            return all_in();
        }
    }
    wagered += temp;
    amount_to_win += temp + blind_adjustment;
    std::string temp_str = "CALL " + std::to_string(wagered);
    return std::make_tuple(true,sb,false,true,wagered,temp_str);
}
std::tuple<bool,float,bool,bool,float,std::string> Player::all_in(){
    float temp;
    if (blind_adjustment && stack > bb){
        amount_to_win += stack - (wagered + blind_adjustment);
    }
    else{
        amount_to_win = stack - wagered;
    }
    temp = stack -wagered;
    wagered = stack;
    std::string temp_str = "ALL IN FOR: " + std::to_string(wagered);
    return std::make_tuple(true,temp,true,true,wagered,temp_str);
}



std::tuple<bool,float,bool,bool,float,std::string> Player::raise(std::string action,
                                                                 float prev_bet,
                                                                 float pot_size,
                                                                 float min_bet){
    try{
        float new_action = std::stof(action);
        if (new_action < 1 && new_action > 0){
            float bet = new_action * pot_size;
            if (bet > 2 * prev_bet){
                float temp = bet - wagered;
                amount_to_win += temp + blind_adjustment;
                std::string temp_str = "RAISE TO: " + std::to_string(wagered);
                return std::make_tuple(true,temp,false,true,wagered, temp_str);
            }
            else{
                return std::make_tuple(false,0,false,false,0,"NA");
            }
        }
        else{
            if (new_action > min_bet){
                float temp = new_action - wagered;
                wagered += temp;
                amount_to_win += temp;
                std::string temp_str = "RAISE TO: " + std::to_string(wagered);
                return std::make_tuple(true,temp,false,true,wagered,temp_str);
            }
            else{
                return rejected();
            }
        }

    }
    catch(...){
        return rejected();
    }
}

std::tuple<bool,float,bool,bool,float,std::string> Player::bet(std::string action, float potsize, float min_bet){
    try{
        float new_action = std::stof(action);
        if (new_action >= min_bet){
            if (new_action >= min_bet){
                return all_in();}
            float temp = new_action - wagered;
            wagered += temp;
            amount_to_win += (temp + blind_adjustment);
            std::string temp_str = "BET: " + std::to_string(wagered);
            return std::make_tuple(true,temp,false,true,wagered,temp_str);
        }
        return rejected();
    }
    catch (...){
        return rejected();
    }
}

std::tuple<bool,float,bool,bool,float,std::string> Player::fold(){
    return std::make_tuple(true,0,false,false,0,"FOLD");
}

std::tuple<bool,float,bool,bool,float,std::string> Player::rejected(){
    return std::make_tuple(false,0,false,false,0,"NA");
}

void Player::reset_street(){
    stack -= wagered;
    wagered = 0;
}

void Player::reset(){
    suit_count = {{'S',0}, {'D',0}, {'H',0}, {'C',0}};
    wagered = 0;
    amount_to_win = 0;
}
float Player::get_stack() {
    return stack;
}

void Player::add_to_stack(float num) {
    stack += num;
}

float Player::get_amount_to_win() {
    return amount_to_win;
}

void Player::reduce_amount_to_win(float amount){
    amount_to_win -= amount;
}