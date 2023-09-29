# poker-game-with-ai:
### NOTE: 
The project is in its early stages and not yet completed. The game has quite a few bugs still mostly in regards to pot distribution. Because we allow players to continue even if they can't post a full BB or SB the payouts are not yet fully functional although determing the winner and the strength of a players hand is currently  working. Visuals are not yet implimented. Should be able to go through each street of action (preflop, flop, turn,river, payout) but the actual payouts are not guranteed to be accurate. Have gotten busy but this should all be fixed by the end of the weekend. The bot is only working in the preflop and flop stages and will post files when done 
## SUMMARY:
Creating a console poker game that you can practice against by playing against a bot
Not finished yet in preliminary stages. 
The goal is to create a poker game you can play in terminal and then essentially create a fairly decent poker solver that a player can chose to play against as an adversary to practice against. Another goal is just to have the solver as a seperate thing all together so you can run poker sims and see the optimal course of action to take. If all that goes well I may try to make it a website depending on how well this goes.

## TO-DO:
1. general error testing
2. Make sure split pots are working correctly
3. Add functionality to add to stack remove players automatically remove player when stack == 0 etc..
4. the current way i'm checking for the best hand is embarassingly inefficient just wanted a working prototype done to make sure my game logic is fine and that I have all the features I need.
5. Impliment the actual solver aspect which will most likley be the hardest part
6. Add visuals for cards
7. possibly add more visuals although this isn't a priority the visuals I added unnecessary and don't add much as it is but they are kind of cool as far as ASCI art goes
8. Add a way to track hand percentages when they are up against one another
9. in general make the code cleaner and more efficient
10. possibly switch the project over to c++ when I have everything worked out although i plan on using pytorch for the solver so it may be easier to keep it in Python and becuase running the actual poker game as is, is not noticably slow this change over may be pointless.
