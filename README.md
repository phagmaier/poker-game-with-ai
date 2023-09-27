# poker-game-with-ai:
### NOTE: 
The project is in its early stages and not yet completed.
Although the bot portion is not completed if I uploaded the correct files the game itself should be working. Not as clean as I would like it's still not finished and far from perfect/optimized or completley tested but it's probably 95% of the way there. Need to impliment the visuals remove/add some print statments to make everything cleaner and it should be fine. Should have everything cleaned up tomorow and then I begin working on the 'bot' or the poker solver.
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
