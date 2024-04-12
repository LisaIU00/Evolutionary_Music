import numpy as np
from numpy import random as r
import matplotlib.pyplot as plt

import song as s

def convert2abc(mylist):
    abc = "M:4/4\nL:1/1"
    i=0
    for chord in mylist:
        abc = abc+"|["
        for note in chord:
            abc = abc+str(note)
        abc = abc+"]"
        i+=1
    abc = abc+""
    return abc


def bestSolution(solutions, tot_song):
    best_song = solutions[0]
    best_index = 0
    index = 1
    
    while index<tot_song:
        if best_song.getCost() > solutions[index].getCost():
            best_song = solutions[index]
            best_index = index
        index += 1

    return best_song, best_index

def selection(solutions, tot_song):
    selected = []
    costs = []
    for s in solutions:
        costs.append(s.getCost())

    for i in range(tot_song):
        elem = min(costs)
        index = costs.index(elem)
        selected.append(solutions[index])
        costs.remove(elem)
    return selected

def geneticIteration(solutions, tot_song, length, note ):
    sol_crossover = []
    for ts in range(tot_song):
        prob = r.random()
        if prob>0.2:
            ts1 = r.randint(0,tot_song)
            s1, s2 = solutions[ts].CrossoverOnePoint(solutions[ts1].getSong())
            sol_crossover.append(s.Song(length, note,   s1, False))
            sol_crossover.append(s.Song(length, note,   s2, False))

    for sol in sol_crossover:
        prob = r.random()
        if prob>0.8:
            sol.mutationExchange()
        prob = r.random()
        if prob>0.8:
            sol.punctualMutation()
        prob = r.random()
        if prob>0.8:
            sol.punctualMutation2()
        solutions.append(sol)

    return solutions

def requireParameters():
    while True:
        try:
            lenght = int(input("Inserisci il numero di accordi che compongono il brano:"))
        except ValueError:
            print("Per favore inserisci un numero intero positivo.")
        else:
            if lenght<1:
                print("Per favore inserisci un numero intero maggiore di 0.")
            else:
                break
    
    while True :
        try:
            note = int(input("Inserisci il numero di note che compongono un accordo:"))
        except ValueError :
            print("Per favore inserisci un numero intero maggiore o ugule a 3.")
        else:
            if note<3 or note>5:
                print("Per favore inserisci un numero intero compreso tra 3 e 5.")
            else:
                break

    return lenght, note

def main():

    length = 20 #number of chords in the song
    note = 3 #notes in a chord

    tot_song = 100 #number of songs
    iter = 200 #iterations of the algorithm

    length, note = requireParameters()
    solutions = []
    for i in range(tot_song):
        solutions.append(s.Song(length, note,   np.zeros((length, note))))
        
    best_song, best_index = bestSolution(solutions, tot_song)

    #print("BEST SOLUTION BEFORE GENETIC ALGORITHM")
    best_song.orderSong()
    #best_song.toString()
    first_best = best_song

    partial_cost = np.zeros(iter)

    it = 0
    while it<iter and best_song.getCost()>0:
        sol_iter = geneticIteration(solutions, tot_song, length, note )
        solutions = selection(sol_iter, tot_song)
        best_song, best_index = bestSolution(solutions, tot_song)
        partial_cost[it]=best_song.getCost()
        print("iterazione ",it," - costo soluzione migliore: ",partial_cost[it])
        it+=1
        

    #print("BEST SOLUTION AFTER GENETIC ALGORITHM")
    best_song.orderSong()
    #best_song.toString()

    #print(convert2abc(best_song.conversionSong()))
    print("FINE\nApri il file 'solution.txt' per visualizzare i risultati")
    
    f = open("solution.txt", "a")
    f.write("First solution: \n"+convert2abc(first_best.conversionSong())+"\n\nBest solution: \n"+convert2abc(best_song.conversionSong()))
    f.close()
    
    plt.rcParams["figure.figsize"] = (20,16)
    plt.rcParams.update({'font.size': 17})
    plt.figure('cost')
    plt.plot(np.arange(it), partial_cost[:it],'m', linewidth=3)
    plt.xlabel('iteration')
    plt.ylabel('cost')
    plt.grid()
    nomeimg = "plot_cost.png"
    plt.savefig(nomeimg)
    plt.show(block=False)
    
if __name__ == "__main__":
    main()

