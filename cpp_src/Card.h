//
// Created by Parker Hagmaier on 10/6/23.
//

#ifndef SEE_WHAT_S_WRONG_CARD_H
#define SEE_WHAT_S_WRONG_CARD_H
#include <iostream>

class Card {
public:
    Card(char s='I', int v=-1);
    friend std::ostream& operator<<(std::ostream& os, const Card& obj);
    friend class Player;
    friend class Dealer;
    friend class Game;
private:
    char suit;
    int value;
};


#endif //SEE_WHAT_S_WRONG_CARD_H
