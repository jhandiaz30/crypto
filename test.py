import os

# yassim example

#eeeeeeeee

#m

key = os.urandom(16)

print(key.hex())


# Demande à l'utilisateur d'entrer un message

message = input("Entrez un message (max 16 caractères) : ")

# Compléter le message avec des espaces si moins de 16 caractères
message = message.ljust(16)

# Convertir en hexadécimal (chaque caractère → 2 chiffres hex)
message_hex = message.encode("utf-8").hex()

# Diviser la chaîne hex en octets (2 caractères = 1 octet
octets = [message_hex[i:i+2] for i in range(0, len(message_hex), 2)]

# Créer la matrice 4x4 (16 cases) si la matrice est inferiuere a 16, automatiquement on mets d['espaces 
matrice = []
index = 0
for i in range(4):
    ligne = []
    for j in range(4):
        ligne.append(octets[index])
        index += 1
    matrice.append(ligne)

# Afficher la matrice hexadécimale
print("\nMatrice 4x4 (en hex) :")
for ligne in matrice:
    print(ligne)