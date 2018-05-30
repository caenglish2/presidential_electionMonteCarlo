# presidential_electionMonteCarlo
Monte-Carlo simulation of 2016 US presidential election

Uses polling data from Wikipedia https://en.wikipedia.org/wiki/Statewide_opinion_polling_for_the_United_States_presidential_election,_2016.

Does Monte-Carlo simulations on the margin of error in the polling and then gets a winner based on how much this error randomly shifts the number of votes in each state. Set to run 100 simulations, tend to get 70% change for Clinton, 30% for Trump in this model.

Heavily uses Pandas, might not be the most optimal way to do this, but is a thorough example of the module in use.

Have to make some judgements to fill in missing data, particularly for 3rd party candidates.
