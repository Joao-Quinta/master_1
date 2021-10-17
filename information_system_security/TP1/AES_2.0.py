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
rc = ["0x01", "0x02", "0x04", "0x08", "0x10", "0x20", "0x40", "0x80", "0x1b", "0x36", "0x00", "0x00", "0x00", ]
# N = number of 32 bit words of the key -> 128 bit key = 4 * 32 bits
N = 4
# R = number of keys needed
R = 11


# fill binary with 0's
def fill_binary(bin_to_fill):  # VERIFIED
    while len(bin_to_fill) < 6:
        bin_to_fill = bin_to_fill[0:2] + "0" + bin_to_fill[2:]
    return bin_to_fill


# input : k hexadecimal values (str -> "0xa1"), output : a str of bits (-> "0b10100001")
def hex_to_binary_str(hex):  # VERIFIED
    l = fill_binary(bin(int(hex[2:3], 16)))
    r = fill_binary(bin(int(hex[3:], 16)))
    return l + r[2:]  # [2:] -> pour enlever 0b


# input : a srt of n bits (-> "0b10100001"), output : hexadecimal values (str -> "0xa1")
def binary_str_to_hex(binary):  # VERIFIED
    if len(binary) == 10:
        l = hex(int(binary[2:6], 2))
        r = hex(int(binary[6:], 2))
    else:
        l = hex(int("0b0000", 2))
        r = hex(int(binary[2:6], 2))
    return l + r[2:]  # [2:] -> pour enlever 0x


# input is i -> that determines which rci we want, -> returns array of 4 binary strings
# 1st string is the rci we want, and the last 3 are the 8 bits set to 0 -> [rci, "0x00", "0x00", "0x00"] -> in binary
def get_rc(i):  # VERIFIED
    rconi = [rc[i], "0x00", "0x00", "0x00"]
    return [hex_to_binary_str(hex_) for hex_ in rconi]


# generate [k_{0}, k_{1}, .... , k_{N-1}]
def generate_k_n_1(key_input, n):  # VERIFIED
    k = []
    for i in range(n):
        ki = []
        for j in range(4):
            s = n * len(k)
            ki.append(key_input[s + j])
        k.append(ki)
    return k


# input : liste de 4 elements, chaque élément 8 bits
def rotation(liste_bits):  # VERIFIED
    liste_copy = liste_bits.copy()
    return liste_copy[1:] + liste_copy[:1]


# input binary -> decimal value as output
def binary_decimal(binary):  # VERIFIED
    split_bits = [int(s) for s in binary]
    pow_bit = [128, 64, 32, 16, 8, 4, 2, 1]
    decimal = 0
    for i in range(len(split_bits)):
        decimal = decimal + split_bits[i] * pow_bit[i]
    return decimal


# input decimal -> transforms to binary of 8 bits
def decimal_binary(decimal):  # VERIFIED
    pow_bit = [128, 64, 32, 16, 8, 4, 2, 1]
    binary = '0b'
    for i in range(len(pow_bit)):
        if decimal >= pow_bit[i]:
            binary = binary + '1'
            decimal = decimal - pow_bit[i]
        else:
            binary = binary + '0'
    return binary


# S box operation
def sBox(list_binary):  # VERIFIED
    pos_sbox = []
    for bi in list_binary:
        a_bi = bi[2:]
        while len(a_bi) < 8:
            a_bi = "0" + a_bi
        index = binary_decimal(a_bi)
        dec_val = Sboxes.Sbox[index]
        binary = decimal_binary(dec_val)
        pos_sbox.append(binary)
    # print(pos_sbox)
    return pos_sbox


# calcule xor de deux listes avec des chaines binaires
def xor_operation(b1, b2):  # VERIFIED
    xor_d = []
    for i in range(len(b1)):
        b = '0b'
        for j in range(len(b1[i][2:])):
            if b1[i][2 + j] == b2[i][2 + j]:
                b = b + '0'
            else:
                b = b + '1'
        xor_d.append(b)
    return xor_d


# key expansion, key is in hex -> need to create nb of rounds + 1 key -> 11 keys
def key_expansion(Ki):
    Wi = []
    for i in range(4 * R):
        if i < N:
            to_app = Ki[i]
        elif i >= N and i % N == 0:
            # print("ici - > ", i)
            l = Wi[i - N] # GOOD
            # print("LEFT -> ", l, " ## ", [binary_str_to_hex(s) for s in l])
            # print("MIDDLE : ")
            # print("wi-1 -> ", Wi[i - 1], " ## ", [binary_str_to_hex(s) for s in Wi[i - 1]]) # GOOD
            # print("rot(wi-1) -> ", rotation(Wi[i - 1]), " ## ", [binary_str_to_hex(s) for s in rotation(Wi[i - 1])]) # GOOD
            m = sBox(rotation(Wi[i - 1]))
            # print("MIDDLE ALL  -> ", m, " ## ", [binary_str_to_hex(s) for s in m])
            r = get_rc(int(i / N) - 1)
            # print("RIGHT -> ", r, " ## ", [binary_str_to_hex(s) for s in r])
            # this = xor_operation(l, m)
            # print(" FIRST XOR -> ", xor_operation(l, m), " ## ", [binary_str_to_hex(s) for s in xor_operation(l, m)])
            # print(" SECOND XOR -> ", xor_operation(this, r), " ## ", [binary_str_to_hex(s) for s in xor_operation(this, r)])
            # print("TOO APP -> ", xor_operation(xor_operation(l, m), r), " ## ", [binary_str_to_hex(s) for s in xor_operation(xor_operation(l, m), r)])
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


key_binary = [hex_to_binary_str(f) for f in key]
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
