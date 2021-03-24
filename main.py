import player as obj
import time

# with open("dataset.txt", "r") as file:
#     lines = [line.rstrip('\n') for line in file]
#     print(lines)

def aux(player_class):
    print(player_class(10, 20))

print(obj.PlayerClass.Arquero(10, 20))
aux(obj.PlayerClass.Arquero)

Boots = obj.Equipment(obj.EquipmentType.Boots, 0, obj.Stats(1, 1, 1, 1, 1))
Weapon = obj.Equipment(obj.EquipmentType.Weapon, 0, obj.Stats(1, 1, 1, 1, 1))
Helmet = obj.Equipment(obj.EquipmentType.Helmet, 0, obj.Stats(1, 1, 1, 1, 1))
Armor = obj.Equipment(obj.EquipmentType.Armor, 0, obj.Stats(1, 1, 1, 1, 1))
Gloves = obj.Equipment(obj.EquipmentType.Gloves, 0, obj.Stats(1, 1, 1, 1, 1))

player = obj.Player(obj.PlayerClass.Arquero, 1.0, Weapon, Boots, Helmet, Gloves, Armor)

player.player_stats()
start_time = time.time()
print(player.fitness(), time.time() - start_time)
start_time = time.time()
print(player.fitness(), time.time() - start_time)