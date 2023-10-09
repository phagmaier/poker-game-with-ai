cmake_minimum_required(VERSION 3.26)
project(see_what_s_wrong)

set(CMAKE_CXX_STANDARD 20)

add_executable(see_what_s_wrong main.cpp
        Card.cpp
        Card.h
        Dealer.cpp
        Dealer.h
        Player.cpp
        Player.h
        Game.cpp
        Game.h
        helperfunctions.cpp
        helperfunctions.h)
