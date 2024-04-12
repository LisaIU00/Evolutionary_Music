import numpy as np
from numpy import random as r
import cost as c

'''
C (0) ; D (2) ; E (4) ; F(5) ; G (7) ; A (9) ; B (11) ;
c (12) ; d (14) ; e (16) ; f (17) ; g (19) ; a (21) ; b (23) ; c' (24)
consonanza = [4, 7, 9, 12, 16, 19, 21, 24]


C (0) ; D (1) ; E (2) ; F(3) ; G (4) ; A (5) ; B (6); C (7) ; D (8) ; E (9) ; F(10) ; G (11) ; A (12) ; B (13); C(14) 
consonanza = [2,4,5,7,9,11,12,14]
'''


class Song:

    #range_note = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24]
    converted_note = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'c', 'd', 'e', 'f', 'g', 'a', 'b']
    range_note = np.arange(14)

    def __init__(self, length, note, song, initial = True):
        self.length = length
        self.note = note
        if initial==False:
            self.song = song
        else:
            self.song = np.zeros((length,note))
            for i in range(length):
                for j in range(note):
                    self.song[i,j] = r.choice(self.range_note)
        self.orderSong()
        self.calculateCost()

    def calculateCost(self):
        self.element_cost = c.costSong(self.song, self.length, self.note)
        self.cost = sum(self.element_cost)

    def conversionSong(self):
        converted_song = []
        for i in range(self.length):
            converted_line = []
            for j in range(self.note):
                #index = self.range_note.index(self.song[i][j])
                index = np.where(self.range_note==self.song[i][j])[0][0]
                converted_line.append(self.converted_note[index])
            converted_song.append(converted_line)
        return converted_song

        

    def mutationExchange(self):
        a1 = r.randint(0,self.length)
        a2 = a1
        while a1==a2:
            a2 = r.randint(0,self.length)

        app = self.song[a1,:]
        self.song[a1,:] = self.song[a2,:]
        self.song[a2,:] = app
        self.orderSong()
        self.calculateCost()

    def punctualMutation(self):
        line1 = r.randint(0,self.length)
        column1 = r.randint(0,self.note)
        line2 = r.randint(0,self.length)
        column2 = r.randint(0,self.note)

        app = self.song[line1, column1]
        self.song[line1, column1] = self.song[line2, column2]
        self.song[line2, column2] = app
        self.orderSong()
        self.calculateCost()

    def punctualMutation2(self):
        line1 = r.randint(0,self.length)
        column1 = r.randint(0,self.note)

        self.song[line1, column1] = r.choice(self.range_note)
        self.orderSong()
        self.calculateCost()

    def CrossoverOnePoint(self, song1):
        p = r.randint(0,self.note)
        sf1 = np.zeros((self.length,self.note))
        sf2 = np.zeros((self.length,self.note))

        sf1[:,0:p] = self.song[:,0:p]
        sf2[:,0:p] = song1[:,0:p]

        sf1[:,p:] = self.song[:,p:]
        sf2[:,p:] = song1[:,p:]

        return sf1, sf2
    
    def orderSong(self):
        for i in range(self.length):
            self.song[i,:].sort()

    def toString(self):
        print("\nMatrix that represent song:\n",self.song)
        print("\nMatrix that represent converted song:\n", self.conversionSong())
        print("\nCost: ", self.cost, "  composed from follow elemets: ",self.element_cost)

    def getSong(self):
        return self.song
    
    def getCost(self):
        return self.cost
    