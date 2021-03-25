import random

(min_height, max_height) = (1.3, 2.0)

class Mutation(object):
    def __init__(self, pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
        """Returns a Mutation object, should not be used from outside (Abstract class)

        Parameters
        ----------
        pm : float e [0, 1]
            Probability of mutation
        weapon_list : list of Weapon
            List of weapons available
        boots_list : list of Boots
            List of boots available
        helmet_list : list of Helmet
            List of helmets available
        gloves_list : list of Gloves
            List of gloves available
        armor_list : list of Armor
            List of armors available
        """

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
    
    # def new_gen(self, n_gene):
    #     if n_gene == 0: return random.randint(min_height, max_height)
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
        if random.random() < self.Pm:
            gene = random.randint(0,player.n_genes-1)
            player_genes = player.genes()
            if gene == 0:
                player_genes[gene] = random.uniform(min_height,max_height)
            else:
                player_genes[gene] = self.map[gene-1][random.randint(0, len(self.map[gene-1]) - 1)]
            player.update(player_genes)
        return player
    
class MultiLimited(Mutation):
    def __init__(self, pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
        super().__init__(pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list)

    def mutate(self, player):
        if random.random() < self.Pm:
            qty = random.randint(1,self.M)
            changes = random.sample(range(0,player.n_genes),qty)
            player_genes = player.genes()
            for gene_i in changes:
                if gene_i == 0:
                    player_genes[gene_i] = random.uniform(min_height,max_height)
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
        player_genes = player.genes()
        # TODO: La iteracion no es in range(0,player.n_genes)?
        for gene_i in changes:
            if random.random() < self.Pm:
                if gene_i == 0:
                    player_genes[gene_i] = random.uniform(min_height,max_height)
                else:
                    player_genes[gene_i] = self.map[gene_i-1][random.randint(0, len(self.map[gene_i-1]) - 1)]
        player.update(player_genes)
        return player

class Full(Mutation):
    def __init__(self, pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list):
        super().__init__(pm, weapon_list, boots_list, helmet_list, gloves_list, armor_list)

    def mutate(self, player):
        if random.random() < self.Pm:
            player_genes = player.genes()
            for gene_i in range(0,player.n_genes):
                if gene_i == 0:
                    player_genes[gene_i] = random.uniform(min_height,max_height)
                else:
                    player_genes[gene_i] = self.map[gene_i-1][random.randint(0, len(self.map[gene_i-1]) - 1)]
            player.update(player_genes)
        return player
