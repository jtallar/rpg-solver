import random
import math

class Crossover:
    
    @staticmethod
    def one_point(player_one, player_two):
        s = random.randint(0,player_one.n_genes-1)
        print(s)
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(s,player_one.n_genes):
            h1[i], h2[i] = h2[i], h1[i]
        return h1, h2
    
    @staticmethod
    def two_points(player_one, player_two):             # TODO: check swap range
        p1 = random.randint(0,player_one.n_genes-1)
        p2 = random.randint(0,player_one.n_genes-1)
        while p1==p2: p2 = random.randint(0,player_one.n_genes-1)
        if p1>p2: p1,p2=p2,p1
        print(p1,p2)
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(p1,p2):
            h1[i], h2[i] = h2[i], h1[i]
        return h1, h2

    @staticmethod
    def ring(player_one, player_two):
        s = player_one.n_genes
        p = random.randint(0, s-1)
        l = random.randint(0, math.ceil(s/2))
        print(p,l)
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(p,p+l):
            h1[i%s], h2[i%s] = h2[i%s], h1[i%s]
        return h1, h2
    
    @staticmethod
    def uniform(player_one, player_two):
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(0,player_one.n_genes):
            if random.choice([True, False]):
                h1[i], h2[i] = h2[i], h1[i]
        return h1, h2


class Mutation:

    @staticmethod
    def gene(player):
        # gene = random.randint(0,player.n_genes-1)
        # rand_pm(0.5)
        return
    
    @staticmethod
    def limit_multi(player):
        return

    @staticmethod
    def uniform_multi(player):
        return
    
    @staticmethod
    def full(player):
        return

    def rand_pm(self, Pm):
        return random.randint(0,100)<Pm*100

class Selection:

    @staticmethod
    def elite(players):
        return 

    @staticmethod
    def roulette(players):
        return

    @staticmethod
    def universal(players):
        return

    @staticmethod
    def boltzmann(players):
        return
    
    @staticmethod
    def tournement(players):
        return
    
    @staticmethod
    def ranking(players):
        return

class Stop(object):

    def __init__(self):
        return
    
    def ask(self):
        return