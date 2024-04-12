import numpy as np
import collections

'''
•	alta percentuale (>=50%) di note uguali in uno stesso accordo: cost + numero *0.8
•   accordi con dissonanze (accordo dissonante se contiene almeno 1 intervallo dissonante): cost + numero dissonanze *10
•	Un accordo si ripete consecutivamente più di 2 volte: cost + numero di ripetizioni*1.6
•	alta percentuale (>=60%) di note uguali nella canzone: cost + numero note uguali*0.4
•	alta percentuale (>=40%) di accordi uguali nella canzone: cost + numero*10


si considera intervallo dissonante tra due note quando non è un intervallo di 
ottava, terza, quinta o sesta

'''

#consonanza = [4, 7, 9, 12, 16, 19, 21, 24]
consonanza = [2,4,5,7,9,11,12,14]
perc_acc = 50
perc_same_note = 60
perc_same_acc = 40

def verifyEqual(a1, a2):
    a11 = a1.sort()
    a22 = a2.sort()
    notequal = False
    for i in range(len(a11)):
        if not(a11[i]==a22[i]):
            notequal = True
    return  not(notequal)


def costSong(song, length, note):
    cost = 0
    equal_cost = 0
    diss_cost = 0
    repeat_cost = 0
    repeat_note = 0
    tot_equal_accord = 0

    equal_accord = []
    just_repeated = []


    for i in range(length):
        '''
        calculate first and second element of cost
        '''
        equal, d = equalDissonant(song[i,:])
        diss_cost += d
        
        if (equal*100)/note>=perc_acc:
            equal_cost += equal
        
        '''
        calculate third element of cost: number of times a chord repeats consecutively
        '''
        stop=False
        j=i+1
        repeat = 0
        while(not(stop) and j<length):
            a1 = np.sort(song[i,:])
            a2 = np.sort(song[j,:])
            if all(a1==a2):
                repeat+=1
            else:
                stop = True
            j+=1
            if j==length:
                stop = True        

        #added to the cost if the number of consecutive repetitions is greater than 2
        if repeat>0:
            repeat_cost += repeat

        '''
        calculate last element of cost
        '''
        #verify that the number of repetitions of the chord have not yet been counted
        rr = False
        k = 0
        while rr==False and k<len(just_repeated):
            a1 = np.sort(song[i,:])
            a2 = np.sort(just_repeated[k])
            if all(song[i,:] == just_repeated[k]):
                rr = True
            k += 1 

        #if have not yet been counted: Count the number of times a chord is repeated in the song
        if rr == False:
            equal_accord.append(1)
            for j in range(length):
                a1 = np.sort(song[i,:])
                a2 = np.sort(song[j,:])
                if all(a1==a2):
                    equal_accord[len(just_repeated)] += 1

            just_repeated.append(song[i,:])

    #added to the cost if the number of repetition is greater than 30%
    for ec in equal_accord:
        if (ec*100)/length >= perc_same_acc:
            tot_equal_accord += 1

    '''
    calculate fourth element of cost
    '''
    unique, counts = np.unique(song, return_counts=True)
    #added to the cost if the number of repetition of a notes in the song is greater than 50%
    for c in counts:
        if (c*100)/length >=perc_same_note:
            repeat_note += 1
    
    #return element of the cost
    return equal_cost*0.8, diss_cost*10, repeat_cost*1.6, repeat_note*0.4, tot_equal_accord*20

'''
given an accord find: 
result = number of repeating notes
dissonant = boolean equal to True if the accord is dissonant
'''
def equalDissonant(element):
    result = 0
    dissonant = 0

    for i in range(len(element)):
        partial_r = 0
        for j in range(i+1, len(element), 1):
            if element[i] == element[j]:
                partial_r+=1

            if abs(element[i] - element[j]) not in consonanza:
                dissonant += 1

        if partial_r>0:
            result += (partial_r+1)    
    return result, dissonant
    