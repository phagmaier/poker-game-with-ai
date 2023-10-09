//
// Created by Parker Hagmaier on 10/6/23.
//

#include "Card.h"
#include <iostream>
Card::Card(char s,int v): suit(s),value(v) {}
std::ostream& operator<<(std::ostream& os, const Card& obj) {
    os << "Value: " << obj.value << " Suit: " << obj.suit << "\n";
    return os;
}