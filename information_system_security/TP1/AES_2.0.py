import copy
import numpy as np
import Sboxes
import tables

# AES -> Joao Filipe Costa da Quinta

message = "Two One Nine Two"
key_text = "Thats my Kung Fu"

# on fait 128 bits key -> 10 rounds
# lets define rconi
rc = ["0x01", "0x02", "0x04", "0x08", "0x10", "0x20", "0x40", "0x80", "0x1b", "0x36", "0x00", "0x00", "0x00", ]
# N = number of 32 bit words of the key -> 128 bit key = 4 * 32 bits
N = 4
# R = number of keys needed
R = 11


# creates a 4x4 array of '0b0'
def new_4_4_array():
    arr = []
    for i in range(4):
        sub_arr = []
        for j in range(4):
            sub_arr.append('0b0')
        arr.append(sub_arr)
    return arr


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


# compute row shifts
def byte_shift_4_4_matrix(m):
    res_array = []
    for i in range(len(m)):
        arr = m[i]
        for j in range(i):
            arr = rotation(arr)
        res_array.append(arr)
    return res_array


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


# sbox for 4x4 matrix
def sBox_4_4_matrix(m):
    res_array = []
    for i in range(len(m)):
        res_array.append(sBox(m[i]))
    return res_array


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


# xor operation for 4x4 matrix
def xor_operation_4_4_matrix(m1, m2):
    res_array = []
    for i in range(len(m1)):
        res_array.append(xor_operation(m1[i], m2[i]))
    return res_array


# returns mix column matrix
def get_mix_column_matrix(type):
    if type == "encr":
        return [[2, 3, 1, 1],
                [1, 2, 3, 1],
                [1, 1, 2, 3],
                [3, 1, 1, 2]]
    else:
        return [[14, 11, 13, 9],
                [9, 14, 11, 13],
                [13, 9, 14, 11],
                [11, 13, 9, 14]]


def get_from_table(v, t):
    if t == 1:
        return binary_decimal(v[2:])
    elif t == 2:
        return tables.table_2[binary_decimal(v[2:])]
    elif t == 3:
        return tables.table_3[binary_decimal(v[2:])]
    elif t == 9:
        return tables.table_9[binary_decimal(v[2:])]
    elif t == 11:
        return tables.table_11[binary_decimal(v[2:])]
    elif t == 13:
        return tables.table_13[binary_decimal(v[2:])]
    elif t == 14:
        return tables.table_14[binary_decimal(v[2:])]


def dot_multiplication(a1, a2):
    val_0 = decimal_binary(get_from_table(a2[0], a1[0]))
    val_1 = decimal_binary(get_from_table(a2[1], a1[1]))
    val_2 = decimal_binary(get_from_table(a2[2], a1[2]))
    val_3 = decimal_binary(get_from_table(a2[3], a1[3]))
    return xor_operation(xor_operation(xor_operation([val_0], [val_1]), [val_2]), [val_3])[0]


def compute_mix_column_matrix(m, type):
    res = [[], [], [], []]
    mix_matrix = get_mix_column_matrix(type)
    for i in range(len(type)):
        for j in range(len(m)):
            res[i].append(dot_multiplication(mix_matrix[i], [m[0][j], m[1][j], m[2][j], m[3][j]]))
    return res


# key expansion, key is in hex -> need to create nb of rounds + 1 key -> 11 keys
def key_expansion(Ki):
    Wi = []
    for i in range(4 * R):
        if i < N:
            to_app = Ki[i]
        elif i >= N and i % N == 0:
            l = Wi[i - N]
            m = sBox(rotation(Wi[i - 1]))
            r = get_rc(int(i / N) - 1)
            to_app = xor_operation(xor_operation(l, m), r)
        elif i >= N > 6 and i % N == 4:
            l = Wi[i - N]
            r = sBox(Wi[i - 1])
            to_app = xor_operation(l, r)
        else:
            l = Wi[i - N]
            r = Wi[i - 1]
            to_app = xor_operation(l, r)
        Wi.append(to_app)
    return Wi


# #################################### inv operations

# input : liste de 4 elements, chaque élément 8 bits
def rotation_inv(liste_bits):  # VERIFIED
    liste_copy = liste_bits.copy()
    return liste_copy[3:] + liste_copy[0:3]


# compute row shifts
def byte_shift_4_4_matrix_inv(m):
    res_array = []
    for i in range(len(m)):
        arr = m[i]
        for j in range(i):
            arr = rotation_inv(arr)
        res_array.append(arr)
    return res_array


# S box operation
def sBox_inv(list_binary):  # VERIFIED
    pos_sbox = []
    for bi in list_binary:
        a_bi = bi[2:]
        while len(a_bi) < 8:
            a_bi = "0" + a_bi
        index = binary_decimal(a_bi)
        dec_val = Sboxes.Sbox_inv[index]
        binary = decimal_binary(dec_val)
        pos_sbox.append(binary)
    # print(pos_sbox)
    return pos_sbox


# sbox for 4x4 matrix
def sBox_4_4_matrix_inv(m):
    res_array = []
    for i in range(len(m)):
        res_array.append(sBox_inv(m[i]))
    return res_array


# just to print a matrix in hexadecimal
def print_4_4_matrix_hex(m):
    for i in range(len(m)):
        print(binary_str_to_hex(m[i][0]), " ", binary_str_to_hex(m[i][1]), " ", binary_str_to_hex(m[i][2]), " ",
              binary_str_to_hex(m[i][3]))


# computes and prints 1st result matrix
def compute_initialization_sept(message, key_0):
    result = xor_operation_4_4_matrix(message, key_0)
    print("result after 1st operation : ")
    print_4_4_matrix_hex(result)
    print()
    return result


def compute_rounds(matrix_pre_round, k):
    matrix_pre_round = compute_initialization_sept(matrix_pre_round, key_block[0])
    for i in range(10):
        matrix_pos_sbox = sBox_4_4_matrix(matrix_pre_round)
        matrix_pos_shift = byte_shift_4_4_matrix(matrix_pos_sbox)
        if i < 9:
            matrix_pos_column = compute_mix_column_matrix(matrix_pos_shift, "encr")
            matrix_pos_xor = xor_operation_4_4_matrix(matrix_pos_column, k[i + 1])
            matrix_pre_round = matrix_pos_xor
        else:
            matrix_pos_xor = xor_operation_4_4_matrix(matrix_pos_shift, k[i + 1])
            matrix_pre_round = matrix_pos_xor
        print("result after round ", i + 1, " : ")
        print_4_4_matrix_hex(matrix_pos_xor)
        print()
    return matrix_pre_round


def compute_rounds_(ciphertext, k):
    for i in range(10):
        if i == 0:
            post_xor = xor_operation_4_4_matrix(ciphertext, k[-1])
        else:
            post_xor = xor_operation_4_4_matrix(ciphertext, k[-1-i])
            post_xor = compute_mix_column_matrix(post_xor, "else")
        matrix_pos_shift = byte_shift_4_4_matrix_inv(post_xor)
        matrix_pos_sbox = sBox_4_4_matrix_inv(matrix_pos_shift)
        ciphertext = matrix_pos_sbox
    ciphertext = xor_operation_4_4_matrix(ciphertext, k[0])
    return ciphertext


def pad_message(m):  # VERIFIED
    k = 2
    L = len(m)
    if L < 16:
        X = 16 - L
    else:
        while L > k * 16:
            k = k + 1
        X = k * 16 - L
    binary_m = []
    for i in range(len(m)):
        binary_m.append(decimal_binary(ord(m[i])))
    for i in range(X):
        binary_m.append(decimal_binary(X))
    return binary_m, k


def generate_plaintext_blocks(b, n):  # VERIFIED
    blocks = []
    for t in range(n):
        message = new_4_4_array()
        for i in range(len(message)):
            for j in range(len(message)):
                message[i][j] = b[(t * 16) + i + (4 * j)]
        blocks.append(message)
    return blocks


def generate_key_block(k):
    binary_k = []
    for i in range(len(k)):
        binary_k.append(decimal_binary(ord(k[i])))
    # K_i -> K0 = K_i[0] ... KN-1 = K_i[-1]
    K_i = generate_k_n_1(binary_k, N)
    x = key_expansion(K_i)
    keys = []
    i = 0
    while i < 44:
        key_run = new_4_4_array()
        for j in range(len(key_run)):
            for l in range(len(key_run)):
                key_run[l][j] = x[i][l]
            i = i + 1
        keys.append(key_run)
    return keys


# create blocks of plaintext padded and in the correct format
print("######### PLAINTEXT AND KEY BLOCK #########")
print()
binary_vals, number_blocks = pad_message(message)
plaintext_blocks = generate_plaintext_blocks(binary_vals, number_blocks)
key_block = generate_key_block(key_text)

for i in range(len(plaintext_blocks)):
    print(" -> block", i + 1, "of plaintext : ")
    print_4_4_matrix_hex(plaintext_blocks[i])
    print()
print(" -> block of key: ")
print_4_4_matrix_hex(key_block[0])
print()
print("######### PLAINTEXT AND KEY BLOCK DONE #########")
print()
ciphertexts = []
for i in range(len(plaintext_blocks)):
    print("######### ENCRIPTION OF PLAINTEXT BLOCK ", i + 1, " #########")
    print()
    ciphertexts.append(compute_rounds(plaintext_blocks[i], key_block))

plaintexts = []
for i in range(len(ciphertexts)):
    print("######### DECREPTION OF CIPHERTEXT BLOCK ", i + 1, " #########")
    print()
    plaintexts.append(compute_rounds_(ciphertexts[i], key_block))
    print("result decription block  : ", i + 1)
    print_4_4_matrix_hex(plaintexts[-1])
