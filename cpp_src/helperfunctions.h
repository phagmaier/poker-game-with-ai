//
// Created by Parker Hagmaier on 10/6/23.
//

#ifndef SEE_WHAT_S_WRONG_HELPERFUNCTIONS_H
#define SEE_WHAT_S_WRONG_HELPERFUNCTIONS_H
#include "helperfunctions.h"
#include <vector>
#include <limits>
#include <tuple>
#include <string>
#include <map>
#include <set>
int get_smallest(std::vector<float> const &bets, std::vector<bool> const &in_hand, int num_players);

float get_best_hand(std::vector<std::tuple<int,std::tuple<float, std::string>>> const &end_players,
                    std::vector<bool> const &in_hand);
std::vector<int> get_indexes(std::vector<std::tuple<int,std::tuple<float, std::string>>> const &end_players,
                             float best_hand, std::vector<bool> const &in_hand);
bool in_indexes(std::vector<int> indexes, int index);

void mySort(std::vector<std::tuple<int, std::tuple<float, std::string>>>& end_players);
bool check_in_vals(int,std::vector<int>);
bool does_it_match(std::set<int> const &aset, int *arr);
#endif //SEE_WHAT_S_WRONG_HELPERFUNCTIONS_H
