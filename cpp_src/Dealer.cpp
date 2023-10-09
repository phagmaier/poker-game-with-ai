//
// Created by Parker Hagmaier on 10/6/23.
//

#include "Dealer.h"
#include <map>
#include <iostream>
#include <algorithm>
#include <ctime>
#include <cstdlib>
#include <random>
#include <vector>
Dealer::Dealer(int num){
    num_players = num;
    make_deck();
    pos = 0;
    flush_count = {{'S',0},{'C',0},{'D',0},{'H',0}};
    value_count = {{2,0},{3,0},{4,0},{5,0},
                   {6,0},{7,0},{8,0},{9,0},
                   {10,0},{12,0},{13,0},{14,0}};
    board_pairs = {};
    //might have to make a initlization for comminity (cards)
}

//Dealer::~Dealer(){}

//deck uses pointers and new so will have to dealocate when done using
void Dealer::make_deck(){
    char suits[] = {'S','C','D','H'};

    int temp = 0;
    for (int i=2; i< 15; ++i){
        for (char x : suits){
            deck[temp] = Card(x,i);
            ++temp;
        }
    }
}

void Dealer::reset(){
    flush_count = {{'S',0},{'C',0},{'D',0},{'H',0}};
    value_count = {{2,0},{3,0},{4,0},{5,0},
                   {6,0},{7,0},{8,0},{9,0},
                   {10,0},{12,0},{13,0},{14,0}};
    pos = 0;
    board_pairs = {{}};
    //Not going to reset community because I don't think I need to
    std::random_device rd;
    std::mt19937 gen(rd());
    std::shuffle(std::begin(deck), std::end(deck), gen);
}

std::vector<std::tuple<Card,Card>> Dealer::deal_preflop(){
    //to increase performance allocate the total amount before the loop
    //Do this later
    std::vector<std::tuple<Card,Card>>cards;
    for (int i=0;i<num_players;++i){
        cards.emplace_back(deck[pos],deck[pos+1]);
        pos+=2;
    }
    return cards;
}

//This should really just be a void and go in
//Community and you can share it with game class
std::tuple<Card,Card,Card> Dealer::deal_flop(){
    for (int i=0; i<3;++i){
        community[i] = deck[pos];
        flush_count[deck[pos].suit] += 1;
        value_count[deck[pos].value] += 1;
        if (value_count[deck[pos].value] > 1){
            board_pairs[deck[pos].value] = value_count[deck[pos].value];
        }
        ++pos;
    }
    return std::make_tuple(community[0],community[1],community[2]);
}

Card Dealer::deal_turn(){
    Card turn_card = deck[pos];
    ++pos;
    community[3] = turn_card;
    flush_count[turn_card.suit] += 1;
    value_count[turn_card.suit] += 1;
    if (value_count[turn_card.value] > 1){
        board_pairs[turn_card.value] = value_count[turn_card.value];
    }
    return turn_card;
}
//This really should be the same function as above
Card Dealer::deal_river() {
    Card river_card = deck[pos];
    ++pos;
    flush_count[river_card.suit] += 1;
    value_count[river_card.suit] += 1;
    if (value_count[river_card.value] > 1){
        board_pairs[river_card.value] = value_count[river_card.value];
    }
    return river_card;
}

std::map<int,int> Dealer::get_value_count(){
    std::map<int,int> present_vals;
    for (auto item =value_count.begin(); item != value_count.end(); ++item){
        if (value_count[item->first]){
            present_vals[item->first] = item->second;
        }
    }
    return present_vals;
}

std::map<int,int> Dealer::get_board_pairs(){
    return board_pairs;
}

std::tuple<char,int> Dealer::get_poss_flush() {
    std::tuple<char, int> present_vals;
    for (auto item = value_count.begin(); item != value_count.end(); ++item) {
        if (flush_count[item->first] >= 3) {
            return std::make_tuple(item->first, item->second);
        }
    }
    return std::make_tuple('I', 0);
}