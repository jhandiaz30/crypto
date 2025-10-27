# ============================================================
#  🧠 AES-128 - Version pédagogique complète et commentée
#  ------------------------------------------------------------
#  Chiffrement et déchiffrement d’un bloc de 16 octets (128 bits)
#  avec génération automatique des 11 sous-clés.
# ============================================================

# --- Clé AES principale (16 octets = 128 bits)
key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")

# --- Table S-BOX officielle (utilisée pour SubBytes)
S_BOX = [
    [0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76],
    [0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0],
    [0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15],
    [0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75],
    [0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84],
    [0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf],
    [0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8],
    [0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2],
    [0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73],
    [0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb],
    [0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79],
    [0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08],
    [0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a],
    [0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e],
    [0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf],
    [0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]
]

# --- Constantes Rcon utilisées dans la génération des sous-clés
RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

# --- Lecture du message utilisateur
message = input("Entrez un message (max 16 caractères) : ")[:16].ljust(16)

# --- Conversion du texte clair en liste d’octets
octets = [b for b in message.encode()]

# --- Création de la matrice d’état 4x4 (AES travaille colonne par colonne)
state = [[0]*4 for _ in range(4)]
index = 0
for c in range(4):
    for r in range(4):
        state[r][c] = octets[index]
        index += 1

# --- Fonction d’affichage lisible des matrices
def print_state(title, s):
    print(f"\n{title}")
    for ligne in s:
        print(" ".join(f"{x:02x}" for x in ligne))

# ============================================================
# 🔧  FONCTIONS DE BASE AES
# ============================================================

def add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    return state

def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            byte = state[i][j]
            state[i][j] = S_BOX[byte >> 4][byte & 0x0F]
    return state

def shift_rows(state):
    new_state = [[0]*4 for _ in range(4)]
    new_state[0] = state[0]
    new_state[1] = state[1][1:] + state[1][:1]
    new_state[2] = state[2][2:] + state[2][:2]
    new_state[3] = state[3][3:] + state[3][:3]
    return new_state

def xtime(a):
    a <<= 1
    if a & 0x100:
        a ^= 0x11B
    return a & 0xFF

def mul(a, b):
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        a = xtime(a)
        b >>= 1
    return res

def mix_columns(state):
    for c in range(4):
        a = [state[r][c] for r in range(4)]
        state[0][c] = mul(a[0],2) ^ mul(a[1],3) ^ a[2] ^ a[3]
        state[1][c] = a[0] ^ mul(a[1],2) ^ mul(a[2],3) ^ a[3]
        state[2][c] = a[0] ^ a[1] ^ mul(a[2],2) ^ mul(a[3],3)
        state[3][c] = mul(a[0],3) ^ a[1] ^ a[2] ^ mul(a[3],2)
    return state

# ============================================================
# 🔑  KEY EXPANSION – Génération des 11 sous-clés
# ============================================================

def key_expansion(key):
    key_symbols = list(key)
    key_schedule = [key_symbols[i:i+4] for i in range(0,16,4)]
    for i in range(4,44):
        temp = key_schedule[i-1][:]
        if i % 4 == 0:
            temp = temp[1:]+temp[:1]
            temp = [S_BOX[b>>4][b&0x0F] for b in temp]
            temp[0] ^= RCON[(i//4)-1]
        word = [a^b for a,b in zip(key_schedule[i-4],temp)]
        key_schedule.append(word)
    return [sum(key_schedule[4*i:4*(i+1)],[]) for i in range(11)]

def key_to_matrix(round_key):
    matrix = [[0]*4 for _ in range(4)]
    idx = 0
    for c in range(4):
        for r in range(4):
            matrix[r][c] = round_key[idx]
            idx += 1
    return matrix

# ============================================================
# 🔒  CHIFFREMENT AES-128
# ============================================================

def AESchiffrement(state, key):
    round_keys = key_expansion(key)
    print("\n=== Sous-clés générées ===")
    for i,k in enumerate(round_keys):
        print(f"Clé {i:02d} : {''.join(f'{b:02x}' for b in k)}")

    state = add_round_key(state, key_to_matrix(round_keys[0]))
    for i in range(1,10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, key_to_matrix(round_keys[i]))
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key_to_matrix(round_keys[10]))
    return state

# ============================================================
# 🔓  DÉCHIFFREMENT AES-128
# ============================================================

# Table inverse S-Box
INV_S_BOX = [[0]*16 for _ in range(16)]
for i in range(16):
    for j in range(16):
        val = S_BOX[i][j]
        INV_S_BOX[val>>4][val&0x0F] = (i<<4)|j

def inv_sub_bytes(state):
    for i in range(4):
        for j in range(4):
            byte = state[i][j]
            state[i][j] = INV_S_BOX[byte>>4][byte&0x0F]
    return state

def inv_shift_rows(state):
    new_state = [[0]*4 for _ in range(4)]
    new_state[0] = state[0]
    new_state[1] = state[1][-1:]+state[1][:-1]
    new_state[2] = state[2][-2:]+state[2][:-2]
    new_state[3] = state[3][-3:]+state[3][:-3]
    return new_state

def inv_mix_columns(state):
    for c in range(4):
        a = [state[r][c] for r in range(4)]
        state[0][c] = mul(a[0],0x0e)^mul(a[1],0x0b)^mul(a[2],0x0d)^mul(a[3],0x09)
        state[1][c] = mul(a[0],0x09)^mul(a[1],0x0e)^mul(a[2],0x0b)^mul(a[3],0x0d)
        state[2][c] = mul(a[0],0x0d)^mul(a[1],0x09)^mul(a[2],0x0e)^mul(a[3],0x0b)
        state[3][c] = mul(a[0],0x0b)^mul(a[1],0x0d)^mul(a[2],0x09)^mul(a[3],0x0e)
    return state

def AESdechiffrement(state, key):
    round_keys = key_expansion(key)
    state = add_round_key(state, key_to_matrix(round_keys[10]))
    for i in range(9,0,-1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, key_to_matrix(round_keys[i]))
        state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, key_to_matrix(round_keys[0]))
    return state

# ============================================================
# 🧪 TEST FINAL : CHIFFRER → AFFICHER → DÉCHIFFRER
# ============================================================

print_state("État initial (texte clair)", state)

# --- Chiffrement
cipher = AESchiffrement([row[:] for row in state], key)
print_state("\nÉtat final (matrice chiffrée)", cipher)

# --- Conversion du résultat en ligne hexadécimale
cipher_bytes = [cipher[r][c] for c in range(4) for r in range(4)]
cipher_hex = "".join(f"{b:02x}" for b in cipher_bytes)
print(f"\nTexte chiffré (hex) : {cipher_hex}")

# --- Tentative d'affichage du texte brut (si caractères imprimables)

# --- Déchiffrement
plain = AESdechiffrement([row[:] for row in cipher], key)
print_state("\nÉtat redéchiffré (matrice)", plain)

# --- Reconstruction du texte clair
plain_bytes = [plain[r][c] for c in range(4) for r in range(4)]
decoded = bytes(plain_bytes).decode().rstrip()
print(f"\nTexte déchiffré : {decoded}")
