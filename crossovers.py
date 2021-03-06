import random
import math
import player as ply

class Crossover:
    # In every method, we asume both player_classes are the same
    
    @staticmethod
    def one_point(player_one, player_two):
        p = random.randint(0,player_one.n_genes)
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(p,player_one.n_genes):
            h1[i], h2[i] = h2[i], h1[i]
        return [ply.Player.new_from_array(player_one.player_class, h1), ply.Player.new_from_array(player_one.player_class, h2)]
    
    @staticmethod
    def two_points(player_one, player_two):
        p1 = random.randint(0,player_one.n_genes)
        p2 = random.randint(0,player_one.n_genes)
        if p1>p2: p1,p2=p2,p1
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(p1,p2):
            h1[i], h2[i] = h2[i], h1[i]
        return [ply.Player.new_from_array(player_one.player_class, h1), ply.Player.new_from_array(player_one.player_class, h2)]

    @staticmethod
    def ring(player_one, player_two):
        s = player_one.n_genes
        p = random.randint(0, s-1)
        l = random.randint(0, math.ceil(s/2))
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(p,p+l):
            h1[i%s], h2[i%s] = h2[i%s], h1[i%s]
        return [ply.Player.new_from_array(player_one.player_class, h1), ply.Player.new_from_array(player_one.player_class, h2)]
    
    @staticmethod
    def uniform(player_one, player_two):
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(0,player_one.n_genes):
            if random.choice([True, False]):
                h1[i], h2[i] = h2[i], h1[i]
        return [ply.Player.new_from_array(player_one.player_class, h1), ply.Player.new_from_array(player_one.player_class, h2)]

