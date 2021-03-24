import player

# with open("dataset.txt", "r") as file:
#     lines = [line.rstrip('\n') for line in file]
#     print(lines)

def aux(player_class):
    print(player_class(10, 20))

print(player.PlayerClass.Arquero(10, 20))
aux(player.PlayerClass.Arquero)

Boots = player.Equipment(player.EquipmentType.Boots, 0, 1, 1, 1, 1, 1)
Weapon = player.Equipment(player.EquipmentType.Weapon, 0, 1, 1, 1, 1, 1)
Helmet = player.Equipment(player.EquipmentType.Helmet, 0, 1, 1, 1, 1, 1)
Armor = player.Equipment(player.EquipmentType.Armor, 0, 1, 1, 1, 1, 1)
Gloves = player.Equipment(player.EquipmentType.Gloves, 0, 1, 1, 1, 1, 1)

player.Player(player.PlayerClass.Arquero, 1.0, Weapon, Boots, Helmet, Gloves, Armor)