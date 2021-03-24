import player as obj
import time
import functions as fun

# with open("dataset.txt", "r") as file:
#     lines = [line.rstrip('\n') for line in file]
#     print(lines)

def aux(player_class):
    print(player_class(10, 20))

# print(obj.PlayerClass.Arquero(10, 20))
# aux(obj.PlayerClass.Arquero)

Boots = obj.Equipment(obj.EquipmentType.Boots, 1, obj.Stats(1, 1, 1, 1, 1))
Weapon = obj.Equipment(obj.EquipmentType.Weapon, 1, obj.Stats(1, 1, 1, 1, 1))
Helmet = obj.Equipment(obj.EquipmentType.Helmet, 1, obj.Stats(1, 1, 1, 1, 1))
Armor = obj.Equipment(obj.EquipmentType.Armor, 1, obj.Stats(1, 1, 1, 1, 1))
Gloves = obj.Equipment(obj.EquipmentType.Gloves, 1, obj.Stats(1, 1, 1, 1, 1))

player = obj.Player(obj.PlayerClass.Arquero, 0.8, Weapon, Boots, Helmet, Gloves, Armor)

Boots2 = obj.Equipment(obj.EquipmentType.Boots, 2, obj.Stats(1, 1, 1, 1, 1))
Weapon2 = obj.Equipment(obj.EquipmentType.Weapon, 2, obj.Stats(1, 1, 1, 1, 1))
Helmet2 = obj.Equipment(obj.EquipmentType.Helmet, 2, obj.Stats(1, 1, 1, 1, 1))
Armor2 = obj.Equipment(obj.EquipmentType.Armor, 2, obj.Stats(1, 1, 1, 1, 1))
Gloves2 = obj.Equipment(obj.EquipmentType.Gloves, 2, obj.Stats(1, 1, 1, 1, 1))

player2 = obj.Player(obj.PlayerClass.Arquero, 1.5, Weapon2, Boots2, Helmet2, Gloves2, Armor2)

# player.player_stats()
# start_time = time.time()
# print(player.fitness(), time.time() - start_time)
# start_time = time.time()
# print(player.fitness(), time.time() - start_time)

# print(player.genes(),'\t', player2.genes(), '\n', fun.Crossover.one_point(player, player2))

# print(player.genes(),'\t', player2.genes(), '\n', fun.Crossover.two_points(player, player2))

# print(player.genes(),'\t', player2.genes(), '\n', fun.Crossover.ring(player, player2))

print(player.genes(),'\t', player2.genes(), '\n', fun.Crossover.uniform(player, player2))