#!/bin/python

#Runs Monte-Carlo simulations to predict the outcome of the 2016 US presidential election, heavily uses pandas to do the solution, which I suspect is not the most efficient way to do it
import pandas as pd
import numpy as np


sim_num=100 #sets the number of Monte-carlo simulations to do, set to 100
num_cands=5 #Number of candidates we are considering, 5 - Trump, Clinton, Stein, Johnson, and McMullin
#Polling numbers by state taken from wikipedia
data=pd.read_csv("polling_data2.csv",sep=',')

#Data conversions
data=data.replace({'%': ''}, regex=True)
for i in range(2,8): data.ix[:,i]=pd.to_numeric(data.ix[:,i])/100.0

#Give McMullin 0% in every state he's not polled for
data['McMullin'].fillna(0.00, inplace=True)

col_names=list(data.columns.values)[2:7]
for i in col_names: data[i]=data[i].astype(float)

#National Polling: Johnson-5%, Stein-2%
#Fill in unknowns in available data using guesses based on other data
#We're going to distrubute the remaining votes to Stein and Johnson according to their relative proportions among themselves in national polling
data['Stein'].fillna((1.0-data['Clinton']-data['Trump']-data['McMullin'])*2.0/7.0, inplace=True)
data['Johnson'].fillna((1.0-data['Clinton']-data['Trump']-data['McMullin'])*5.0/7.0, inplace=True)

#Record the number of wins from each simulation.
wins={'Clinton':0,'Trump':0,'Johnson':0,'Stein':0,'McMullin':0}
wins=pd.DataFrame(data=wins,index=data['State'])

#Get total of electoral votes, setup data frame
wins2=pd.DataFrame(data=wins,index=['Total'])
wins=wins.append(wins2)
for i in range(num_cands): wins.ix['Total',i]=0
for i in range(sim_num):
    #If the margin of error is 0, this is an expected number of votes based on how many were cast in 2012 in each state
    d={'Clinton':data.ix[:,'Clinton']*data.ix[:,'2012 Total Votes'], 'Trump':data.ix[:,'Trump']*data.ix[:,'2012 Total Votes'], 'Johnson':data.ix[:,'Johnson']*data.ix[:,'2012 Total Votes'], 'Stein':data.ix[:,'Stein']*data.ix[:,'2012 Total Votes'], 'McMullin':data.ix[:,'McMullin']*data.ix[:,'2012 Total Votes']}
    votes=pd.DataFrame(data=d)
    #Let's use Monte-Carlo to simulate the effect of the margin of error
    results=data;results=results.drop('EV',axis=1);results=results.drop('Margin of Error',axis=1);results=results.drop('2012 Total Votes',axis=1)
    for state_idx in range(len(data.index)):
        for candidate_idx in range(num_cands): #Number of candidates, columns
            error=(data['Margin of Error'].ix[state_idx]*float(data['2012 Total Votes'].ix[state_idx]))
            #We're going to scale the votes based on the margin of error in the polling. This is a way to ensure the percent of votes per candidate sums to 100%
            adj_votes=(votes.ix[state_idx, candidate_idx]-int(np.random.normal(votes.ix[state_idx, candidate_idx], scale=error)))
            #Adjust the total votes based on the random error
            votes.ix[state_idx, candidate_idx]=votes.ix[state_idx, candidate_idx]+adj_votes
        #under the adjusted vote totals based on the margin of error, let's determine the winner in each state
        winner=str(votes.ix[state_idx, :].idxmax(axis=1))
        wins.ix[state_idx, winner]+=1

        for i in range(1,num_cands+2): results.ix[state_idx,i]=0.0
        EV_won=data['EV'].ix[state_idx]
        results.ix[state_idx,winner]=EV_won

    #These are the total Electoral votes in each state for each candidate
    results.sum().drop('State',axis=0)
    total_ev=(results.sum().drop('State',axis=0))

    maxid=-1;max_ev=0
    for i in range(len(total_ev)): 
        if max_ev<total_ev[i]: max_ev=total_ev[i];maxid=i-1

    #Let's record the winner based on total electoral votes and rerun another simulation
    wins.ix['Total',maxid]+=1
#print the final table showing how many times each candidate won each state in the simulation
#Might want to check convergence and calculate a percentage rather than 
print('Times each candidate won each state or the election (see Total) out of: '+str(sim_num))
print(wins)

#Example output
#Times each candidate won each state or the election (see Total) out of: 100
#                Clinton  Johnson  McMullin  Stein  Trump
#Alabama             0.0      0.0       0.0    0.0  100.0
#Alaska             73.0      0.0       0.0    0.0   27.0
#Arizona            33.0      0.0       0.0    0.0   67.0
#Arkansas            0.0      0.0       0.0    0.0  100.0
#California        100.0      0.0       0.0    0.0    0.0
#Colorado           79.0      0.0       0.0    0.0   21.0
#Connecticut       100.0      0.0       0.0    0.0    0.0
#Delaware          100.0      0.0       0.0    0.0    0.0
#Florida            14.0      0.0       0.0    0.0   86.0
#Georgia             4.0      0.0       0.0    0.0   96.0
#Idaho               0.0      0.0       0.0    0.0  100.0
#Illinois           99.0      0.0       0.0    0.0    1.0
#Indiana             2.0      0.0       0.0    0.0   98.0
#Iowa                2.0      0.0       0.0    0.0   98.0
#Kansas              0.0      0.0       0.0    0.0  100.0
#Kentucky            0.0      0.0       0.0    0.0  100.0
#Louisiana           1.0      0.0       0.0    0.0   99.0
#Maine              80.0      0.0       0.0    0.0   20.0
#Maryland          100.0      0.0       0.0    0.0    0.0
#Massachusetts     100.0      0.0       0.0    0.0    0.0
#Michigan           32.0      0.0       0.0    0.0   68.0
#Minnesota          96.0      0.0       0.0    0.0    4.0
#Missouri           14.0      0.0       0.0    0.0   86.0
#Montana             0.0      0.0       0.0    0.0  100.0
#Nebraska            0.0      0.0       0.0    0.0  100.0
#Nevada             52.0      0.0       0.0    0.0   48.0
#New Hampshire      99.0      0.0       0.0    0.0    1.0
#New Jersey         99.0      0.0       0.0    0.0    1.0
#New Mexico         72.0      0.0       0.0    0.0   28.0
#New York          100.0      0.0       0.0    0.0    0.0
#North Carolina     51.0      0.0       0.0    0.0   49.0
#North Dakota        5.0      0.0       0.0    0.0   95.0
#Ohio                3.0      0.0       0.0    0.0   97.0
#Oklahoma            0.0      0.0       0.0    0.0  100.0
#Oregon             89.0      0.0       0.0    0.0   11.0
#Pennsylvania       89.0      0.0       0.0    0.0   11.0
#Rhode Island      100.0      0.0       0.0    0.0    0.0
#South Carolina      3.0      0.0       0.0    0.0   97.0
#South Dakota        0.0      0.0       0.0    0.0  100.0
#Tennessee           8.0      0.0       0.0    0.0   92.0
#Texas               0.0      0.0       0.0    0.0  100.0
#Utah                0.0      0.0       0.0    0.0  100.0
#Vermont           100.0      0.0       0.0    0.0    0.0
#Virginia           86.0      0.0       0.0    0.0   14.0
#Washington         99.0      0.0       0.0    0.0    1.0
#West Virginia       0.0      0.0       0.0    0.0  100.0
#Wisconsin         100.0      0.0       0.0    0.0    0.0
#Wyoming             0.0      0.0       0.0    0.0  100.0
#Hawaii            100.0      0.0       0.0    0.0    0.0
#Mississippi         0.0      0.0       0.0    0.0  100.0
#Washington DC     100.0      0.0       0.0    0.0    0.0
#Total              69.0     31.0       0.0    0.0    0.0