import random
import math
import player as obj

class Crossover:                # TODO: mejor forma de devolver al player
    
    @staticmethod
    def one_point(player_one, player_two):
        s = random.randint(0,player_one.n_genes-1)
        print(s)
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(s,player_one.n_genes):
            h1[i], h2[i] = h2[i], h1[i]
        return obj.Player(player_one.player_class, h1[0],h1[1],h1[2],h1[3],h1[4],h1[5]), obj.Player(player_one.player_class, h2[0],h2[1],h2[2],h2[3],h2[4],h2[5])
    
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
        return obj.Player(player_one.player_class, h1[0],h1[1],h1[2],h1[3],h1[4],h1[5]), obj.Player(player_one.player_class, h2[0],h2[1],h2[2],h2[3],h2[4],h2[5])

    @staticmethod
    def ring(player_one, player_two):
        s = player_one.n_genes
        p = random.randint(0, s-1)
        l = random.randint(0, math.ceil(s/2))
        print(p,l)
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(p,p+l):
            h1[i%s], h2[i%s] = h2[i%s], h1[i%s]
        return obj.Player(player_one.player_class, h1[0],h1[1],h1[2],h1[3],h1[4],h1[5]), obj.Player(player_one.player_class, h2[0],h2[1],h2[2],h2[3],h2[4],h2[5])
    
    @staticmethod
    def uniform(player_one, player_two):
        h1, h2 = player_one.genes(), player_two.genes()
        for i in range(0,player_one.n_genes):
            if random.choice([True, False]):
                h1[i], h2[i] = h2[i], h1[i]
        return obj.Player(player_one.player_class, h1[0],h1[1],h1[2],h1[3],h1[4],h1[5]), obj.Player(player_one.player_class, h2[0],h2[1],h2[2],h2[3],h2[4],h2[5])


class Mutation(object):
    def __init__(self, pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
        self.pm = pm
        self.weapon_list = weapon_list
        self.boots_list = boots_list
        self.helmet_list = helmet_list
        self.gloves_list = gloves_list
        self.armor_list = armor_list
        self.map = [weapon_list, boots_list, helmet_list, gloves_list, armor_list]
        self.M = 6

    def mutate(self, player):
        pass

    @staticmethod
    def rand_pm(Pm):
        return random.randint(0,100) < (Pm*100)
    
    # def new_gen(self, n_gene):
    #     if n_gene == 0: return random.randint(1.3, 2)
    #     elif n_gene == 1: return self.weapon_list[random.randint(0, len(self.weapon_list) - 1)]
    #     elif n_gene == 2: return self.boots_list[random.randint(0, len(self.weapon_list) - 1)]
    #     elif n_gene == 3: return self.helmet_list[random.randint(0, len(self.weapon_list) - 1)]
    #     elif n_gene == 4: return self.gloves_list[random.randint(0, len(self.weapon_list) - 1)]
    #     elif n_gene == 5: return self.armor_list[random.randint(0, len(self.weapon_list) - 1)]
    #     else: print("error")    # TODO: para test

class SimpleGen(Mutation):
    def __init__(self, pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
        super().__init__(pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list)

    def mutate(self, player):
        if self.rand_pm(self.pm):
            gene = random.randint(0,player.n_genes-1)
            player_genes = player.genes()
            print(gene)
            if gene == 0:
                player_genes[gene] = round(random.uniform(1.3,2), 2)
            else:
                player_genes[gene] = self.map[gene-1][random.randint(0, len(self.map[gene-1]) - 1)]
            player.update(player_genes)
        return player
    
class MultiLimited(Mutation):
    def __init__(self, pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
        super().__init__(pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list)

    def mutate(self, player):
        if self.rand_pm(self.pm):
            qty = random.randint(1,self.M)
            changes = random.sample(range(0,player.n_genes-1),qty)
            print('\n',changes,'\n')
            player_genes = player.genes()
            for gene_i in changes:
                if gene_i == 0:
                    player_genes[gene_i] = round(random.uniform(1.3,2), 2)
                else:
                    player_genes[gene_i] = self.map[gene_i-1][random.randint(0, len(self.map[gene_i-1]) - 1)]
            player.update(player_genes)
        return player

class MultiUniform(Mutation):
    def __init__(self, pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
        super().__init__(pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list)

    def mutate(self, player):
        qty = random.randint(0,player.n_genes-1)
        changes = random.sample(range(0,player.n_genes-1),qty)
        print('\n',changes,'\n')
        player_genes = player.genes()
        for gene_i in changes:
            if self.rand_pm(self.pm):
                if gene_i == 0:
                    player_genes[gene_i] = round(random.uniform(1.3,2), 2)
                else:
                    player_genes[gene_i] = self.map[gene_i-1][random.randint(0, len(self.map[gene_i-1]) - 1)]
        player.update(player_genes)
        return player

class Full(Mutation):
    def __init__(self, pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
        super().__init__(pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list)

    def mutate(self, player):
        if self.rand_pm(self.pm):
            player_genes = player.genes()
            for gene_i in range(0,player.n_genes):
                if gene_i == 0:
                    player_genes[gene_i] = round(random.uniform(1.3,2), 2)
                else:
                    player_genes[gene_i] = self.map[gene_i-1][random.randint(0, len(self.map[gene_i-1]) - 1)]
            player.update(player_genes)
        return player

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