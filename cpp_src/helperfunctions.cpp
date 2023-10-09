//
// Created by Parker Hagmaier on 10/6/23.
//
#include "helperfunctions.h"
#include <algorithm>
//#include <vector>
//#include <limits>
//#include <tuple>
//#include <string>
//can actually just return the index
int get_smallest(std::vector<float> const &bets, std::vector<bool> const &in_hand, int num_players){
    float min_val = std::numeric_limits<float>::infinity();
    int min_index;
    for (int i=0; i< num_players;++i){
        if (bets[i] < min_val && in_hand[i]){
            min_val = bets[i];
            min_index = i;
        }
    }
    return min_index;
}


float get_best_hand(std::vector<std::tuple<int,std::tuple<float, std::string>>> const &end_players,
                    std::vector<bool> const &in_hand){
    float max_val = 0;
    for (int i=0; i<end_players.size(); ++i){
        int index = std::get<0>(end_players[0]);
        float val = std::get<0>(std::get<1>(end_players[i]));
        if (val > max_val && in_hand[index]){
            max_val = val;
        }

    }
    return max_val;
}

std::vector<int> get_indexes(std::vector<std::tuple<int,std::tuple<float, std::string>>> const &end_players,
                             float best_hand, std::vector<bool> const &in_hand){
    std::vector<int> winners;
    for (int i=0;i<end_players.size();++i){
        if (best_hand == std::get<0>(std::get<1>(end_players[i])) && in_hand[std::get<0>(end_players[i])]){
            winners.push_back(std::get<0>(end_players[i]));}
    }
    return winners;
}


bool in_indexes(std::vector<int> indexes, int index){
    for (int val : indexes){
        if (val == index){
            return true;
        }
    }
    return false;
}

//std::vector<std::tuple<int,std::tuple<float, std::string>>> const &end_players



void mySort(std::vector<std::tuple<int, std::tuple<float, std::string>>>& end_players){
    auto customComparator = [](const std::tuple<int, std::tuple<float, std::string>>& a,
                               const std::tuple<int, std::tuple<float, std::string>>& b) {
        // Compare based on the first value within the inner tuple of the second item
        return std::get<0>(std::get<1>(a)) < std::get<0>(std::get<1>(b));
    };
    std::sort(end_players.begin(), end_players.end(),customComparator);
}

bool check_in_vals(int num,std::vector<int> vec){
    for (int a : vec){
        if (a == num){
            return true;
        }
    }
    return false;
}

bool does_it_match(std::set<int> const &aset, int *arr){
    for (std::set<int>::iterator it = aset.begin(); it != aset.end(); ++it) {
        bool isfalse = false;
        for (int i=0;i<5;++i){
            if (*it == arr[i]){
                isfalse = true;
                break;
            }
        }
        if (!isfalse){
        return false;}
    }
    return true;
}

