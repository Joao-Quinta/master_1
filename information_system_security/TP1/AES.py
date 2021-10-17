import copy
import Sboxes

# AES -> Joao Filipe Costa da Quinta
# TO DO: ASK FOR KEY AS INPUT
key = ["0x54", "0x68", "0x61", "0x74",
       "0x73", "0x20", "0x6d", "0x79",
       "0x20", "0x4b", "0x75", "0x6e",
       "0x67", "0x20", "0x46", "0x75"]

# on fait 128 bits key -> 10 rounds
# lets define rconi
rc = ["0x01", "0x02", "0x04", "0x08", "0x10", "0x20", "0x40", "0x80", "0x1b", "0x36"]
# N = number of 32 bit words of the key -> 128 bit key = 4 * 32 bits
N = 4
# R = number of keys needed
R = 11


# fill binary with 0's
def fill_binary(bin_to_fill):
    while len(bin_to_fill) < 6:
        bin_to_fill = bin_to_fill[0:2] + "0" + bin_to_fill[2:]
    return bin_to_fill


# input : k hexadecimal values (str -> "0xa1"), output : a str of bits (-> "0b10100001")
def hex_to_binary_str(hex):
    l = fill_binary(bin(int(hex[2:3], 16)))
    r = fill_binary(bin(int(hex[3:], 16)))
    return l + r[2:]  # [2:] -> pour enlever 0b


# input : a srt of n bits (-> "0b10100001"), output : hexadecimal values (str -> "0xa1")
def binary_str_to_hex(binary):
    if len(binary) == 10:
        l = hex(int(binary[2:6], 2))
        r = hex(int(binary[6:], 2))
    else:
        l = hex(int("0b0000", 2))
        r = hex(int(binary[2:6], 2))
    return l + r[2:]  # [2:] -> pour enlever 0x


# generate [k_{0}, k_{1}, .... , k_{N-1}]
def generate_k_n_1(key_input, n):
    k = []
    for i in range(n):
        ki = []
        for j in range(4):
            s = n * len(k)
            ki.append(key_input[s + j])
        k.append(ki)
    return k


# input : liste de 4 elements, chaque élément 8 bits
def rotation(liste_bits):
    liste_copy = liste_bits.copy()
    return liste_copy[1:] + liste_copy[:1]


# S box operation
def sBox(list_binary):
    pos_sbox = []
    for bi in list_binary:
        # THIS IS WRONG -> NEED TO TURN
        if len(bi) == 10:
            left_bin_int = int(bi[2:6], 2)
            right_bin_int = int(bi[6:], 2)
        else:
            left_bin_int = int('0000', 2)
            right_bin_int = int(bi[2:], 2)
        index = left_bin_int * 16 + right_bin_int
        pos_sbox.append(bin(Sboxes.Sbox[index]))
    return pos_sbox


# calcule xor de deux listes avec des chaines binaires
def xor_operation(b1, b2):
    # print("la1", b1)
    # print("la2", b2)
    xor_d = []
    for i in range(len(b1)):
        xor_d.append(bin(int(b1[i], 2) ^ int(b2[i], 2)))
    # print("xor done")
    return [fill_binary(b) for b in xor_d]


# key expansion, key is in hex -> need to create nb of rounds + 1 key -> 11 keys
def key_expansion(Ki):
    Wi = []
    for i in range(4 * R):
        to_app = 0
        if i < N:
            to_app = Ki[i]
        elif i >= N and i % N == 0:
            # print("ici - > ", i)
            l = Wi[i - N]
            m = sBox(rotation(Wi[i - 1]))
            # HAVE TO REDO THIS -> IT IS WRONG, FULL 0'S
            r = [rc_binary[int(i / N)] for _ in range(4)]
            # print(r)
            to_app = xor_operation(xor_operation(l, m), r)
        elif i >= N > 6 and i % N == 4:
            l = Wi[i - N]
            r = sBox(Wi[i - 1])
            to_app = xor_operation(l, r)
        else:
            # print("ici 2222 - > ", i)
            l = Wi[i - N]
            r = Wi[i - 1]
            # the fuck here ?
            to_app = xor_operation(l, r)
        Wi.append(to_app)
    return Wi


# on transforme la cle hex en une cle binaire
key_binary = [hex_to_binary_str(f) for f in key]
rc_binary = [hex_to_binary_str(f) for f in key]

# K_i -> K0 = K_i[0] ... KN-1 = K_i[-1]
K_i = generate_k_n_1(key_binary, N)
print()
print([binary_str_to_hex(s) for s in K_i[0]], [binary_str_to_hex(s) for s in K_i[1]],
      [binary_str_to_hex(s) for s in K_i[2]], [binary_str_to_hex(s) for s in K_i[3]])
print()

x = key_expansion(K_i)
# print(x)
""""""
i = 0
while i < 44:
    v1 = [binary_str_to_hex(s) for s in x[i]]
    v2 = [binary_str_to_hex(s) for s in x[i + 1]]
    v3 = [binary_str_to_hex(s) for s in x[i + 2]]
    v4 = [binary_str_to_hex(s) for s in x[i + 3]]
    print(v1, v2, v3, v4)
    i = i + 4
