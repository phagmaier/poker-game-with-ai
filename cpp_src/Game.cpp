//
// Created by Parker Hagmaier on 10/6/23.
//

//Because straights and straight flushes
//need to remove duplicate vlaues need to use a set
//or if the last value is the same as the current value you just skip over it
#include "Game.h"
//#include <vector>
//#include "Player.h"
//#include "Dealer.h"
//#include "helperfunctions.cpp"
Game::Game(int num, float stack, float b_b, float s_b){
    num_players = num;
    for (int i=0;i<num; ++i){
        players.emplace_back(stack,b_b,s_b);
    }
    sb_pos = 0;
    bb_pos = 0;
    sb = s_b;
    bb = b_b;
    utg = (num_players>2) ? bb_pos +1 : sb_pos;
    dealer_button = (num_players>2) ? num_players -1 : bb_pos;

    create_straights();
    dealer = Dealer(num_players);
    pot = 0;
    blinds = 0;
    for (int i=0;i<num_players;++i){
        all_in.push_back(false);
        in_hand.push_back(true);
    }
    //community_cards = nullptr;
    flush_count = 0;
    flush_suit = 'I';
    sb_paid = 0;
    bb_paid = 0;
    blind_payouts = true;
    hand_rankings = {{"SF", 900}, {"Q",800}, {"FH",700},
                     {"F",600}, {"5F",500}, {"S",400},
                     {"T",300}, {"TP",200}, {"P",100}, {"H",0}};
}

void Game::change_blinds(){
    if (num_players > 2){
        bb_pos = (bb_pos + 1 < num_players) ? bb_pos +1 : 0;
        sb_pos = (sb_pos + 1 < num_players) ? sb_pos +1 : 0;
        dealer_button =(dealer_button + 1 < num_players) ? dealer_button +1 : 0;
        utg = (utg + 1 < num_players) ? utg +1 : 0;
    }
    else{
        bb_pos = (bb_pos + 1 < num_players) ? bb_pos+1 : 0;
        sb_pos = (sb_pos + 1 < num_players) ? sb_pos+1 : 0;
        utg = sb_pos;
        dealer_button = bb_pos;
    }
}

void Game::preflop(){
    std::vector player_cards = dealer.deal_preflop();
    for (int i=0;i<num_players;++i){
        players[i].get_cards(player_cards[i]);
    }
    bool temp;
    std::tie(bb_paid,temp) = players[bb_pos].pay_bb();
    all_in[bb_pos] = temp;
    std::tie(sb_paid,temp) = players[bb_pos].pay_sb();
    all_in[sb_pos] = temp;
    blinds = bb_paid + sb_paid;
    pot = blinds;
}

void Game::street_preflop(){
    bool temp_all_in;
    bool temp_in_hand;
    float bet = 0;
    float total = 0;
    int count = 0;
    float prev_bet = 0;
    int current = utg;
    float min_bet = 2 * bb;
    bool collect_sb = true;
    std::string action_taken;
    while (count < num_players) {
        if (!(all_in[current]) && in_hand[current]) {
            std::tie(bet, temp_all_in, temp_in_hand, total, action_taken) =
                    players[current].get_action(prev_bet, pot, min_bet);
            std::cout << "Player " << count << ": " << action_taken << "\n";
            //Think this is wrong
            //don't know what the proper boolean comparison would be
            //but if bb bets just one blinde and only the small blind calls
            //this would never trigger
            //can add more complicated logic later
            //think you can just make it to check or if total = 1 bb not 100% sure
            //ALSO THINK SOME OF THE OTHER LOGIC IS FUCKED UP CHECK PYTHON
            //CODE CAUSE EASIER TO READ
            if (bet >= min_bet) {
                blind_payouts = false;
            }
            if (collect_sb && current == sb_pos) {
                collect_sb = false;
                if (bet) {
                    if (bet >= sb) {
                        blinds += sb;
                    } else {
                        blinds += bet;
                    }
                }
            }
            if (bet && ! all_in[current] || bet == 0){
                prev_bet = total;
            }
            else{
                if (total >= 2 * prev_bet && total > min_bet){
                    prev_bet = total;
                }
                else{
                    if (prev_bet){
                        prev_bet = (total < 2 * prev_bet) ? prev_bet : total;
                    }
                    else{
                        prev_bet = (total < min_bet) ? min_bet : total;
                    }
                }
            }
            pot += bet;
        }
        std::cout << "The pot is: " << pot << "\n";
        current = (current+1 < num_players) ? current+1 : 0;
        ++count;
    }
}

void Game::street(){
    float total = 0;
    int count = 0;
    float prev_bet = 0;
    int current = sb_pos;
    float min_bet = bb;
    float bet;
    bool temp_all_in = false;
    bool temp_in_hand = true;
    std::string action_taken;
    while (count < num_players){
        if (! all_in[current] && in_hand[current]) {
            std::tie(bet, temp_all_in, temp_in_hand, total, action_taken) = players[current].get_action(prev_bet, pot, min_bet);
            std::cout << "Player " << current << " " << action_taken << "\n";

            if (bet && !all_in[current] || bet == 0) {
                prev_bet = total;
            } else {
                if (total >= 2 * prev_bet && total > min_bet) {
                    prev_bet = total;
                } else {
                    if (prev_bet) {
                        prev_bet = (total < 2 * prev_bet) ? prev_bet : total;
                    } else {
                        prev_bet = (total < min_bet) ? min_bet : total;
                    }
                }
            }
            pot += bet;
            std::cout << "The pot is " << pot << "\n";
        }
        current = (current +1 < num_players) ? current +1 : 0;
        ++count;
    }
}

void Game::reset(){
    int count = 0;
    for(Player player : players){
        std::cout << "AT THE END OF THE HAND PLAYER: " << count << "s stack is: " << player.get_stack() << "\n";
    }
    blinds = 0;
    //community_cards = {0,0,0,0,0};
    pot = 0;
    for (int i=0;i<num_players;++i){
        in_hand[i] = true;
        all_in[i] = false;
        players[i].reset();
    }
    dealer.reset();
    change_blinds();
}

//CREATE A SEPERATE FUNCTION FOR SINGLE PAYOUTS
//OR LITERALLY JUST DO IT BY HAND
void Game::payout(std::vector<std::tuple<int,std::tuple<float, std::string>>> end_players){
    int players_in_hand = 0;
    std::vector<float> player_bets;
    for (int i=0; i<num_players; ++i){
        player_bets.push_back(players[i].get_amount_to_win());
        if (in_hand[i]){
            ++players_in_hand;
        }
    }
    if (blind_payouts){
        payouts_blinds(end_players);
    }
    while (players_in_hand){
        if (players_in_hand == 1){
            for (int i=0; i< num_players; ++i){
                if (in_hand[i]){
                    players_in_hand = 0;
                    players[i].add_to_stack(pot);
                }
            }
        }
        else{
            int smallest_bet_index = get_smallest(player_bets, in_hand, num_players);
            float min_bet = player_bets[smallest_bet_index];
            float side_pot = min_bet * players_in_hand;
            float best_hand = get_best_hand(end_players,in_hand);
            std::vector<int>indexes = get_indexes(end_players,best_hand,in_hand);
            float winnings = side_pot / indexes.size();
            pot -= side_pot;
            players_in_hand = 0;
            for (auto tup : end_players){
                if (in_indexes(indexes,std::get<0>(tup))){
                    players[std::get<0>(tup)].add_to_stack(winnings);
                }
                players[std::get<0>(tup)].reduce_amount_to_win(min_bet);
                //check if amount to win is 0 and if it is set in_hand to false
                if (players[std::get<0>(tup)].get_amount_to_win() == 0){
                    in_hand[std::get<0>(tup)] = false;
                }
                else{
                    players_in_hand +=1;
                }
            }
        }
        if (players_in_hand == 0){
            //should really call reset
            break;
        }
    }
}



//Not implimented just putting so payouts doesn't error
void Game::payouts_blinds(std::vector<std::tuple<int,std::tuple<float, std::string>>> end_players) {
    mySort(end_players);
    for (std::tuple<int,std::tuple<float,std::string>> tup : end_players){
        int indexx = std::get<0>(tup);
        if (indexx == bb_pos && bb_paid < bb || indexx == sb_pos && sb_paid < bb){
            if (indexx == bb_pos){
                in_hand[indexx] = false;
                float temp_amount;

                if (bb_paid >= sb_paid){
                    temp_amount = bb_paid + sb_paid;
                    sb_paid = 0;
                }
                else{
                    temp_amount = bb_paid + sb_paid - (sb_paid-bb_paid);
                    sb_paid = sb_paid - bb_paid;
                }
                players[indexx].add_to_stack(temp_amount);
                pot -= temp_amount;
                blinds -= temp_amount;
            }
            else{
                float temp_amount;
                if (sb_paid >= bb_paid){
                    temp_amount = sb_paid + bb_paid;
                }
                else{
                    temp_amount = sb_paid + bb_paid - (bb_paid - sb_paid);
                    bb_paid = bb_paid - sb_paid;
                }
                players[indexx].add_to_stack(temp_amount);
                pot -= temp_amount;
                blinds -= temp_amount;
            }
        }
        else{
            players[indexx].add_to_stack(blinds);
            pot -= blinds;
            return;
        }
    }
}

std::vector<std::tuple<int,std::tuple<float,std::string>>> Game::get_hand_strength(){
    std::vector<std::tuple<int,std::tuple<float,std::string>>>hand_strengths;
    for (int i=0; i<num_players;++i){
       if (in_hand[i]){
           auto [a,b] = hand_strength(players[i]);
           hand_strengths.push_back(std::make_tuple(i,std::make_tuple(a,b)));
       }
    }
    return hand_strengths;
}

std::tuple<float,std::string> Game::hand_strength(Player player){
    return std::make_tuple(2.0,"Gay");

}
//should break a lot of this into smaller functions
//also i need to static cast the ints to floats
// example: static_cast<float>(vec[0])/10
float Game::apair(Player player) {
    std::map<int, int> board_map = dealer.get_value_count();
    std::vector<int> board_vals;
    //since I think it returns real thing need to manually do deep copys
    std::map<int, int> temp_board_pairs = dealer.get_board_pairs();
    std::map<int, int> board_pairs;
    std::vector<int> board_pair_vals; //items in python
    for (auto it = board_map.begin(); it != board_map.end(); ++it) {
        board_vals.push_back(it->first);
    }
    for (auto i: temp_board_pairs) {
        board_pair_vals.push_back(i.first);
        board_pairs[i.first] = i.second;
    }
    //auto temp = std::find(board_pair_vals.begin(), board_pair_vals.end(),player.left_val);
    //if (player.left_val)
    if (player.left_val == player.right_val) {
        auto temp = std::find(board_pair_vals.begin(), board_pair_vals.end(), player.left_val);
        if (temp != board_pair_vals.end()) {
            board_pairs[player.left_val] += 2;
        } else {
            board_pairs[player.left_val] = 2;
        }
    } else {
        auto temp = std::find(board_vals.begin(), board_vals.end(), player.left_val);
        if (temp != board_vals.end()) {
            auto other = std::find(board_pair_vals.begin(), board_pair_vals.end(), player.left_val);
            if (other != board_pair_vals.end()) {
                board_pairs[player.left_val] += 1;
            }
            else {
                board_pairs[player.left_val] = 2;
            }
        }
        auto temp2 = std::find(board_vals.begin(), board_vals.end(), player.right_val);
        if (temp2 != board_vals.end()) {
            auto other2 = std::find(board_pair_vals.begin(), board_pair_vals.end(), player.right_val);
            if (other2 != board_pair_vals.end()) {
                board_pairs[player.right_val] += 1;
            }
            else {
                board_pairs[player.right_val] = 2;
            }
        }
    }
    int quads = 0;
    int trips = 0;
    std::vector<int> a_pair;
    if (!board_pairs.empty()){
        if (check_in_vals(player.left_val,board_pair_vals)){
            board_pairs[player.left_val] += 1;
        }
        if (check_in_vals(player.right_val,board_pair_vals)){
            board_pairs[player.right_val] += 1;
        }
        for (auto i : board_pairs) {
            quads = (i.second == 4) ? i.first : 0;
            trips = (i.second == 3) ? i.first : 0;
            if (i.second == 2) {
                a_pair.push_back(i.first);
            }
        }
            if (quads){
                return static_cast<float>(hand_rankings["Q"]) + static_cast<float>(quads);
            }
            if (trips){
                if (!a_pair.empty()){
                    std::sort(a_pair.begin(), a_pair.end());
                    return static_cast<float>(hand_rankings["FH"]) + static_cast<float>(trips) + static_cast<float>(a_pair[a_pair.size()-1])/100;
                }
                else{
                    std::vector<int> all_cards;
                    for (int i: board_vals){
                        if (i != trips) {
                            all_cards.push_back(i);
                        }
                    }
                    if (player.left_val != trips) {
                        all_cards.push_back(player.left_val);
                    }
                    if (player.right_val != trips){
                    all_cards.push_back(player.right_val);
                        }
                    std::sort(all_cards.begin(), all_cards.end());
                    return static_cast<float>(all_cards[all_cards.size()-2])/1000 + static_cast<float>(all_cards[all_cards.size()-1])/100 + static_cast<float>(hand_rankings["T"]);

                }
            }
            if (a_pair.size() == 2){
                std::sort(a_pair.begin(), a_pair.end());
                std::vector<int> all_cards;
                for (int i: board_vals){
                    if (!check_in_vals(i,a_pair)){
                    all_cards.push_back(i);}
                }
                if (!check_in_vals(player.left_val, a_pair)){
                    all_cards.push_back(player.left_val);
                }
                if (!check_in_vals(player.right_val, a_pair)){
                    all_cards.push_back(player.right_val);
                }
                std::sort(all_cards.begin(), all_cards.end());
                return static_cast<float>(hand_rankings["TP"]) + static_cast<float>(a_pair[a_pair.size()-1]) / 10
                +static_cast<float>(a_pair[a_pair.size()-2]) / 100 + static_cast<float>(all_cards[all_cards.size()-1])/1000;
            }
            if (!a_pair.empty()){
                std::vector<int> all_cards;
                for (int i: board_vals) {
                    if (!check_in_vals(i, a_pair)) {
                        all_cards.push_back(i);
                    }
                }
                    if (!check_in_vals(player.left_val,a_pair)){
                        all_cards.push_back(player.left_val);
                    }
                    if (!check_in_vals(player.right_val,a_pair)){
                        all_cards.push_back(player.right_val);
                    }
                    std::sort(all_cards.begin(), all_cards.end());
                    return static_cast<float>(hand_rankings["P"]) + static_cast<float>(a_pair[0])
                    + static_cast<float>(all_cards[all_cards.size()-1])/100 + static_cast<float>(all_cards[all_cards.size()-2])/200 + static_cast<float>(all_cards[all_cards.size()-3])/300;

            }
        }
        return 0;
}
//There's a way mor efficient way to do this
//should just add a helper function that determines
//if a straight is even possibe that is called before this
float Game::flush(Player player){

    if (flush_suit != 'I'){
       if (flush_count < 5){
           std::vector<int> flush_cards;
           if (player.left_suit == flush_suit){
               flush_cards.push_back(player.left_val);
           }
           if (player.right_suit == flush_suit){
               flush_cards.push_back(player.right_val);
           }
           for (int i=0; i<5; ++i){
               if(community_cards[i].suit == flush_suit){
                   flush_cards.push_back(community_cards[i].value);
               }
           }
           if (flush_cards.size() >=5){
               float s_f = straight_flush(flush_cards);
               if (s_f){
                   return s_f;
               }
               auto flush_card = std::max_element(flush_cards.begin(),flush_cards.end());
                return static_cast<float>(hand_rankings["F"]) + static_cast<float>(*flush_card);
           }

       }
       if (flush_count == 5){
           std::vector<int> flush_cards;
          if (player.left_suit == flush_suit){
              flush_cards.push_back(player.left_val);
          }
          if (player.right_suit == flush_suit){
              flush_cards.push_back(player.right_val);
          }
          std::sort(flush_cards.begin(), flush_cards.end());
          float val = 0;
          for (int i=4;i>=0;--i){
              val+= static_cast<float>(flush_cards[i]);
          }
          return static_cast<float>(hand_rankings["5F"]) + val;
       }
    }
    return 0;
}

float Game::straight_flush(std::vector<int> flush_cards2){
    std::sort(flush_cards2.begin(),flush_cards2.end());
    //need to check if 14 is in flush cards and if so then put 1 in
    if (check_in_vals(14,flush_cards2)){
        flush_cards2.push_back(1);
    }
    std::vector<int> temp;
    std::sort(flush_cards2.begin(),flush_cards2.end(), std::greater<int>());
    int maxx;
    int x = 0;
    while (x + 5 < flush_cards2.size()) {
        for (int i = 0; i < 10; ++i) {
            maxx = straights[i][0];
            for (int z = x; z < 5; ++z) {
                if (straights[i][x] != flush_cards2[x]) {
                    break;
                }
                if (x == 4) {
                    return static_cast<float>(maxx);
                }
            }
        }
        ++x;
    }
    return 0;
}

//because of this function you will need a function that deletes the memory
void Game::create_straights() {
    int count2 = 0;
    int count;
    for (int i=14; i >= 5; --i) {
        count =0;
        for (int x=i; x>i-5;--x) {
            straights[count2][count] = x;
            ++count;
        }
       ++count2;
    }
}

//NOW YOU ARE ON STRAIGHTS
//CAN REUSE SOME OF THE CODE FROM STRAIGHT FLUSH

float Game::astraight(Player player) {
    std::set<int> all_cards_set = {community_cards[0].value,
                                   community_cards[1].value,
                                   community_cards[2].value,
                                   community_cards[3].value,
                                   community_cards[4].value};
    int inner = 0;
    for (int outer=0;outer<10;++outer){
        int maxx = straights[outer][0];
       if (does_it_match(all_cards_set, straights[outer])){
           return static_cast<float>(maxx);
       }
    }
    return 0;
}


void Game::flop(){
    std::tie(community_cards[0],community_cards[1],
             community_cards[2]) = dealer.deal_flop();
}
void Game::turn(){
    community_cards[3] = dealer.deal_turn();
}
void Game::river(){
    community_cards[4] = dealer.deal_river();
}

float Game::high_card(Player player){
    //std::sort(community_cards, community_cards + (sizeof(community_cards)/sizeof(community_cards[0])));
    std::vector<int> mycards;
    for (int i=0;i<5;++i){
        mycards.push_back(community_cards[i].value);
    }
    mycards.push_back(player.left_val);
    mycards.push_back(player.right_val);
    std::sort(mycards.begin(), mycards.end(), [](int a, int b) {
        return a > b; // Compare in descending order
    });
    return static_cast<float>(mycards[0])/10 + static_cast<float>(mycards[1])/20
    + static_cast<float>(mycards[2])/30 + static_cast<float>(mycards[3])/30 + static_cast<float>(mycards[4])/40;
}

bool Game::hand_over(){
    for (bool i : in_hand){
        if (i){
            return true;
        }

    }
    return false;
}

//Also need to check if hand is over if so
//just go to preflop
void Game::gameloop() {
    std::cout << "PREFLOP\n";
    preflop();
    for (int i=0;i<num_players;++i){
        std::cout << "Player " << i << "s hand\n";
        std::cout << players[i];
        std::cout << "\n";
    }
    street_preflop();
    //call street_preflop reset (need to create this func)
    flop();
    //should make this a function
    //just pass what street so the first line can say the X came:
    for (int i=0;i<3;++i){
        std::cout << "The flop came: ";
        std::cout << community_cards[0].value << community_cards[0].suit;
        std::cout << "  " << community_cards[1].value << community_cards[1].suit;
        std::cout << "  " << community_cards[2].value << community_cards[2].suit << "\n";
    }
    street();
    //call street reset
    turn();

    for (int i=0;i<4;++i){
        std::cout << "The turn came: ";
        std::cout << community_cards[0].value << community_cards[0].suit;
        std::cout << "  " << community_cards[1].value << community_cards[1].suit;
        std::cout << "  " << community_cards[2].value << community_cards[2].suit;
        std::cout << "  " << community_cards[3].value << community_cards[3].suit << "\n";
    }
    street();
    //call street reset
    river();

    street();
    //Call street reset
    //NEED A FUNCTION THAT GETS ALL PLAYERS STILL IN
    //HAND AND GETS HAND STRENGTHS
    //std::vector<std::tuple<int,std::tuple<float,std::string>>>
    std::vector<std::tuple<int,std::tuple<float,std::string>>> end_players;
    //end_players = get_hand_strength();
    //payout() -> call with rsults hand strengths
}