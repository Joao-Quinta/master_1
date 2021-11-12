import copy

import AES_JoaoFilipe_CostadaQuinta as Joao_AES
import Correc_TP1_AES
import math


# message of 128 bits set to 0 in matrix form
def generate_128_bits_0():
    message = Joao_AES.new_4_4_array()
    for i in range(len(message)):
        for j in range(len(message)):
            message[i][j] = '0b00000000'
    return message


# returns a matrix of binary in a hexa line
def print_matrix_in_hexa_line(m):
    f = "0x"
    for i in range(len(m)):
        for j in range(len(m)):
            f = f + Joao_AES.binary_str_to_hex(m[j][i])[2:]
    return f


# computes hash subkey, encryption of 0^128 with the key (-> computes key blocks for each step, and we keep them)
def compute_hash_subkey(key):
    plaintext = generate_128_bits_0()
    key_block = Joao_AES.generate_key_block(key)
    return Joao_AES.compute_rounds(plaintext, key_block), key_block


# simple letter to binary form (-> correct form for the rest of the computations)
def convert_letter_to_bin(c):
    return Joao_AES.decimal_binary(ord(c))


# from an array of 14 elements -> turns it into 4x4 matrix in the correct order
def convert_to_matrix_form(arr):
    r = Joao_AES.new_4_4_array()
    for i in range(len(r)):
        for j in range(len(r)):
            r[j][i] = arr[j + 4 * i]
    return r


# from a matrix 4x4 returns an array with the values in the correct order
def convert_to_array_form(ma):
    r = []
    for i in range(len(ma)):
        for j in range(len(ma)):
            r.append(ma[j][i])
    return r


# finds the first 0 in a binary number, and switches '1' to '0' if it finds them while searching for the first 0 (starts from the right)
def find_zero(s):
    i = len(s) - 1
    s = list(s)
    found = False
    while i > 1:
        if s[i] == '1':
            s[i] = '0'
            i = i - 1
        else:
            found = True
            s[i] = '1'
            i = 0
    return ''.join(s), found


# receives 4x4 matrix and computes its incrementation
def increment_1(matrix):
    arr = convert_to_array_form(matrix)
    i = len(arr) - 1
    done = False
    while not done:
        b, done = find_zero(arr[i])
        arr[i] = b
        if i > 0:
            i = i - 1
        else:
            return convert_to_matrix_form(arr)
    return convert_to_matrix_form(arr)


# only works if len(iv) = 12 chars -> 96 bits
def compute_counter(iv_t, h):
    if len(iv_t) == 12:
        iv = [convert_letter_to_bin(char) for char in iv_t]
        for i in range(3):
            iv.append('0b00000000')
        iv.append('0b00000001')
        arr = convert_to_matrix_form(iv)
        return arr
    else:
        arr = compute_auth_blocks(iv_t)
        mod_polynome_ = [128, 7, 2, 1, 0]
        ivf = convert_to_matrix_from_single_binary(
            multiplication_poly_gf_128(convert_to_single_binary(arr[0]), convert_to_single_binary(h), mod_polynome_))

        for i in range(1, len(arr)):
            ivf = Joao_AES.xor_operation_4_4_matrix(ivf, arr[i])
            ivf = convert_to_matrix_from_single_binary(
                multiplication_poly_gf_128(convert_to_single_binary(ivf), convert_to_single_binary(h), mod_polynome_))
        return ivf


def xor_op_last_block(m1, m2, p):
    res = Joao_AES.new_4_4_array()
    for i in range(len(m1)):
        for j in range(len(m2)):
            if m2[j][i] != '0b0':
                r = '0b'
                b1 = m1[j][i][2:]
                b2 = m2[j][i][2:]
                for t in range(len(b1)):
                    if b1[t] == b2[t]:
                        r = r + '0'
                    else:
                        r = r + '1'
                res[j][i] = r
            else:
                res[j][i] = p
    return res


# compute 1 cipher for each plaintext block -> we increment the counter (1) -> encrypt it with the key (2),
# perform xor between plaintext block and the result of the encryption (result of (2)) -> results in a cipherblock
def compute_ciphers(plaintext, key_block, counter):
    ciphers = []
    for i in range(len(plaintext)):
        counter = increment_1(counter)
        etape_1 = Joao_AES.compute_rounds(counter, key_block)
        if i == len(plaintext) - 1:
            ciphers.append(xor_op_last_block(etape_1, plaintext[i], '0b0'))
        else:
            ciphers.append(Joao_AES.xor_operation_4_4_matrix(etape_1, plaintext[i]))
    return ciphers


# computes auth blocks
def compute_auth_blocks(auth):
    auth_blocks = []
    while len(auth) > 0:
        if len(auth) >= 16:
            string_block = auth[:16]
            auth = auth[16:]
        else:
            string_block = auth
            auth = ""
        binary_str_block = [Joao_AES.decimal_binary(ord(string_block[i])) for i in range(len(string_block))]
        while len(binary_str_block) < 16:
            binary_str_block.append('0b00000000')
        auth_blocks.append(convert_to_matrix_form(binary_str_block))
    return auth_blocks


def aide_compute_L(arr, ah):
    full_arr = ah
    while len(arr) < 64:
        arr.insert(0, '0')
    for i in range(8):
        b = '0b'
        for j in range(8):
            b = b + arr[i * 8 + j]
        full_arr.append(b)
    return full_arr


# compute L block
def compute_L(a, c):
    full_arr = []
    arr_a = list(bin(len(a)))[2:]
    nb_binary = 0
    for t in range(len(c)):
        for i in range(len(c[t])):
            for j in range(len(c[t])):
                if c[t][j][i] != '0b0':
                    nb_binary = nb_binary + 1
    arr_c = list(bin(nb_binary))[2:]
    full_arr = aide_compute_L(arr_a, full_arr)
    full_arr = aide_compute_L(arr_c, full_arr)
    return convert_to_matrix_form(full_arr), nb_binary


# this function performs binary multiplication and then applies mod
# i know that there are easier ways of performing this computation, but because of how my binary data was,
# this was the easiest way i found for it to work correctly
# mod is a list of form -> [128, 7, 2, 1, 0]
# each value in the list mod, tells us with bits are set to 1 for the mod operation
# which means this function works for every size of p1 and p2 and for every mod,
# returns something that is the same size as p1
def multiplication_poly_gf_128(p1, p2, mod):
    p1 = list(p1)[2:]
    p2 = list(p2)[2:]
    deg_p1 = len(p1) - 1
    deg_p2 = len(p2) - 1
    res = []
    while len(res) < deg_p1 + deg_p2 + 1:
        res.append('0')
    deg_res = deg_p1 + deg_p2
    for i in range(len(p1)):
        if p1[i] == '1':
            for j in range(len(p2)):
                if p2[j] == '1':
                    deg_p1_h = deg_p1 - i
                    deg_p2_h = deg_p2 - j
                    deg_res_h = deg_p1_h + deg_p2_h
                    index = deg_res - deg_res_h
                    if res[index] == '0':
                        res[index] = '1'
                    else:
                        res[index] = '0'
    deg_mod = max(mod)
    len_mod = deg_mod + 1
    mod_poly = []
    for i in range(len_mod):
        mod_poly.append('0')
    for deg in mod:
        mod_poly[deg_mod - deg] = '1'
    while len(res) > len(p1):
        if res[0] == '0':
            res.pop(0)
        else:
            for j in range(len(mod_poly)):
                if res[j] == mod_poly[j]:
                    res[j] = '0'
                else:
                    res[j] = '1'
    return '0b' + ''.join(res)


# receives a matrix 4x4 and converts all the data to a single binary form of 128 bits -> for poly multiplication
def convert_to_single_binary(matrix):
    arr = convert_to_array_form(matrix)
    res = '0b'
    for i in range(len(arr)):
        res = res + arr[i][2:]
    return res


# does the opposite of the previous function (convert_to_single_binary) -> recovers the matrix form
# from a single binary form of 128 bits
def convert_to_matrix_from_single_binary(binary):
    binary = binary[2:]
    arr = []
    for i in range(16):
        arr.append('0b' + binary[8 * i:8 * i + 8])
    ma = convert_to_matrix_form(arr)
    return ma


# help for function -> generate_plaintext
def generate_plaintext_aide(m, b):
    for i in range(len(m)):
        for j in range(len(m)):
            if m[j][i] == '0b0':
                m[j][i] = b
                return m, True
    return m, False


# generates message blocks in the correct way for this tp -> no padding
def generate_plaintext(m, t):
    plaintext_blocks = []
    if t == 0:
        binary_chars = [Joao_AES.decimal_binary(ord(m[i])) for i in range(len(m))]
    else:
        binary_chars = []
        m = m[2:]
        while len(m) > 0:
            binary_chars.append(Joao_AES.hex_to_binary_str('0x' + m[0:2]))
            m = m[2:]
    block = Joao_AES.new_4_4_array()
    while len(binary_chars) > 0:
        block, a = generate_plaintext_aide(block, binary_chars[0])
        if a:
            binary_chars.pop(0)
        else:
            plaintext_blocks.append(copy.deepcopy(block))
            block = Joao_AES.new_4_4_array()
    plaintext_blocks.append(copy.deepcopy(block))
    return plaintext_blocks


# computes tag
def compute_tag(auth_data_, h, cipher_blocks, L_block_, c_start_):
    mod_polynome_ = [128, 7, 2, 1, 0]
    # step 1 -> polynomial GF(128) multiplication between auth_data[0] and H
    step = convert_to_matrix_from_single_binary(
        multiplication_poly_gf_128(convert_to_single_binary(auth_data_[0]), convert_to_single_binary(h), mod_polynome_))

    # if there are more auth data blocks -> we first do XOR with the result from the previous result with auth_data[i]
    # and then do polynomial GF(128) multiplication between the result from XOR and H
    for i in range(1, len(auth_data_)):
        step = Joao_AES.xor_operation_4_4_matrix(step, auth_data_[i])
        step = convert_to_matrix_from_single_binary(
            multiplication_poly_gf_128(convert_to_single_binary(step), convert_to_single_binary(h), mod_polynome_))

    # from the result of the previous operations, we do:
    # XOR with cipher[i], and polynomial GF(128) multiplication between the result from XOR and H
    # we do it for each cipher block
    for i in range(len(cipher_blocks)):
        if i == len(cipher_blocks) - 1:
            step = xor_op_last_block(step, cipher_blocks[i], '0b00000000')
        else:
            step = Joao_AES.xor_operation_4_4_matrix(step, cipher_blocks[i])
        step = convert_to_matrix_from_single_binary(
            multiplication_poly_gf_128(convert_to_single_binary(step), convert_to_single_binary(h), mod_polynome_))

    # XOR with the result and L block
    step = Joao_AES.xor_operation_4_4_matrix(step, L_block_)

    # polynomial GF(128) multiplication between the result from XOR and H
    step = convert_to_matrix_from_single_binary(
        multiplication_poly_gf_128(convert_to_single_binary(step), convert_to_single_binary(h), mod_polynome_))

    # and finally we do a XOR with the previous result and C_start
    step_f = Joao_AES.xor_operation_4_4_matrix(step, c_start_)
    return step_f


# does all the computations for encryption returns cipherblocks and tag
def signed_encription(K, IV, M, A):
    # (1) compute HASH_SUBKEY (and key block for the key)
    hash_sub, key_block_ = compute_hash_subkey(K)
    # (2) compute iv
    iv = compute_counter(IV, hash_sub)
    # (3) compute c start -> encr de iv avc la cle
    c_start = Joao_AES.compute_rounds(iv, key_block_)
    # (4) generate plaintext blocks for our message we want to encr
    plaintext_blocks = generate_plaintext(M, 0)
    # (5) create the cipher blocks, each plaintext block has a corresponding cipher block
    cipher_blocks_ = compute_ciphers(plaintext_blocks, key_block_, iv)
    # (6) compute authentication blocks
    auth_blocks_ = compute_auth_blocks(A)
    # (7) compute L
    L, number_b = compute_L(A, cipher_blocks_)
    # (8) compute tag
    tag = compute_tag(auth_blocks_, hash_sub, cipher_blocks_, L, c_start)

    ad = 0
    cipher_text = "0x"
    for t in range(len(cipher_blocks_)):
        for i in range(len(cipher_blocks_[t])):
            for j in range(len(cipher_blocks_[t])):
                if ad < number_b:
                    cipher_text = cipher_text + Joao_AES.binary_str_to_hex(cipher_blocks_[t][j][i])[2:]
                    ad = ad + 1

    return cipher_text, tag


def compute_decre(C, T, K, A, IV):
    # (1) compute HASH_SUBKEY (and key block for the key)
    hash_sub, key_block_ = compute_hash_subkey(K)
    # (2) compute iv
    iv = compute_counter(IV, hash_sub)
    # (3) compute c start -> encr de iv avc la cle
    c_start = Joao_AES.compute_rounds(iv, key_block_)
    # (4) compute authentication blocks
    auth_blocks_ = compute_auth_blocks(A)
    # (5) compute cipher_blocks from C
    c_blocks = generate_plaintext(C, 1)
    # (6) compute L
    L, number_b = compute_L(A, c_blocks)

    # (7) compute tag
    T_ = compute_tag(auth_blocks_, hash_sub, c_blocks, L, c_start)
    if T == T_:
        print("TAG CORRECT")
        p = compute_ciphers(c_blocks, key_block_, iv)

        ad = 0
        cipher_text = ""
        for t in range(len(p)):
            for i in range(len(p[t])):
                for j in range(len(p[t])):
                    if ad < number_b:
                        cipher_text = cipher_text + chr(Joao_AES.binary_decimal(p[t][j][i][2:]))
                        ad = ad + 1

        return cipher_text, True
    else:
        print("FAIL")
        return [], False


# VALUES
message = "salut je veux envoyer ce message en secret, et le signer"
key_in_text = "YoU cAn'T sEe m3"
iv_ = "je peux etre de n'importe quel taille moi !"
auth_data = "je peux faire ce que je veux ici, parce que je veux "

print("## VARIABLES START ##")
print()
print("message : ", message, " |||| len : ", len(message))
print("key : ", key_in_text, " |||| len : ", len(key_in_text))
print("iv : ", iv_, " |||| len : ", len(iv_))
print("auth data : ", auth_data, " |||| len : ", len(auth_data))
print()
print("## VARIABLES DONE ##")

print()
c, t = signed_encription(key_in_text, iv_, message, auth_data)
print("##### RESULT OF ENCRE START #####")
print()
print("CYPHERTEXT BLOCKS & TAG: ")
print("c -> ", c)
print("tag -> ", print_matrix_in_hexa_line(t))
print()
print("##### RESULT OF ENCRE DONE #####")
print()
print("##### RESULT OF DECRE START #####")
print()

# this one will be incorrect -> (wrong key)
print("TEST 1 -> wrong key : ")
p_, a = compute_decre(c, t, "You can't see m1", auth_data, iv_)
print()
print("TEST 2 -> right key : ")
p_1, a1 = compute_decre(c, t, key_in_text, auth_data, iv_)
if a1:
    print("plaintext : ", p_1)
print()
print("##### RESULT OF DECRE DONE #####")


# malheureusement il y a une erreur quelque part, j'ai essayé de découvrir, mais c'était pas réussit
# mais tout le reste 'marche' comme voulu (si j'ai bien compris les consignes)