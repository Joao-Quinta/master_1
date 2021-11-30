# gonna sha it up
# Costa da Quinta, Joao Filipe
import SHAConstants


# ######################################################################## useful functions that aren't specific to one step -> START


# binary to hex convertor
def binary_str_to_hex(binary):  # VERIFIED
    return hex(int(binary, 2))[2:]


# cette fonction fait l'addition binnaire, elle additionne 'add_this' chez 'add_here'
# si 'add_here' dépasse les 32 bits apres l'addition, on fait directement l'opération mod
def bin_str_sum(add_here, add_this):  # VERIFIED
    carry = []
    while len(carry) < len(add_here) + 1:
        carry.append('0')
    add_here = list(add_here)
    add_this = list(add_this)
    add_here.reverse()
    add_this.reverse()
    for j in range(len(add_this)):
        s = int(add_here[j]) + int(add_this[j]) + int(carry[j])
        if s == 1:
            add_here[j] = '1'
        elif s == 2:
            add_here[j] = '0'
            carry[j + 1] = '1'
        elif s == 3:
            add_here[j] = '1'
            carry[j + 1] = '1'
    # s il y a besoinde de calculer le mod, alors on le code va aller dans ce if, en gros si le carry à tjrs une valuer à 1 comme dernièrer valeur
    if carry[len(add_this)] == '1':
        add_here.append('1')
        b = []
        c = []
        carry = []
        for i in range(32):
            b.append('0')
            c.append('0')
            carry.append('0')
        b.append('1')
        carry.append('0')
        for i in range(len(c)):
            if carry[i] == '1':
                if add_here[i] == '1':
                    c[i] = '0'
                elif add_here[i] == '0':
                    c[i] = '1'
                    carry[i + 1] = '1'
            elif carry[i] == '0':
                if add_here[i] == '0':
                    c[i] = '0'
                elif add_here[i] == '1':
                    c[i] = '1'
        c.reverse()
        c = ''.join(c)
        return c
    # sil y a pas besoin de mod, alors on va directement la, et on a fini
    add_here.reverse()
    add_here = ''.join(add_here)
    return add_here


# computes sum of all the words in words to sum
# en gros plutot que calculer (a+b+c)%d, on fait (((a+b)%d)+c)%d
def compute_sum(words_to_sum):  # VERIFIED
    total = '00000000000000000000000000000000'
    total = list(total)
    for t in range(len(words_to_sum)):
        total = bin_str_sum(total, words_to_sum[t])
    return total


# function that does right rotate or right shift depending on f (true = rotate), n = nb of rotates/shifts
def right_rotate_shift(w, f, n):  # VERIFIED
    for i in range(n):
        a = '0'
        # if f is set to true, then it is a rotate, if f is set to false, it is a shift
        if f:
            a = w[-1]
        w = a + w[:-1]
    return w


# computes xor of two 32 bit words
def xor_32bit_word(w1, w2):  # VERIFIED
    w_res = ''
    for i in range(len(w1)):
        if w1[i] == w2[i]:
            w_res = w_res + '0'
        else:
            w_res = w_res + '1'
    return w_res


# computes and of two 32 bit words
def and_32bit_word(w1, w2):
    w_res = ''
    for i in range(len(w1)):
        if w1[i] == w2[i] == '1':
            w_res = w_res + '1'
        else:
            w_res = w_res + '0'
    return w_res


# computes not3 of 32 bit word
def not_32bit_word(w1):
    w_res = ''
    for i in range(len(w1)):
        if w1[i] == '1':
            w_res = w_res + '0'
        else:
            w_res = w_res + '1'
    return w_res


# input decimal -> transforms to binary of 8 bits -> utilisé pour la conversion de texte en binaire
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


# fill binary with 0's -> en gros c'est pour assurer que tout est écrit sous forme de 4 bits, -> valeur 1 devient 0001
def fill_binary(bin_to_fill):  # VERIFIED
    while len(bin_to_fill) < 6:
        bin_to_fill = bin_to_fill[0:2] + "0" + bin_to_fill[2:]
    return bin_to_fill


# input : k hexadecimal values (str -> "0xa1"), output : a str of bits (-> "0b10100001")
def hex_to_binary_str(x):  # VERIFIED
    b = fill_binary(bin(int(x, 16)))
    return b[2:]  # [2:] -> pour enlever 0b


# loads ki in binary form
def load_ki():  # VERIFIED
    k = SHAConstants.K
    Ki_b = []
    for i in range(len(k)):
        binary_32 = ''
        for j in range(len(k[i][2:])):
            binary_32 = binary_32 + hex_to_binary_str(k[i][2 + j])
        Ki_b.append(binary_32)
    return Ki_b


# loads iv in binary form
def load_iv():  # VERIFIED
    iv = SHAConstants.IV
    iv_b = ''
    for i in range(len(iv)):
        for j in range(len(iv[i][2:])):
            iv_b = iv_b + hex_to_binary_str(iv[i][2 + j])
    return iv_b


# ######################################################################## useful functions that aren't specific to one step -> DONE


# ######################################################################## first step : message padding -> START


# generates padded binary message from m
def generate_binary_message(m):  # VERIFIED
    b = ''
    for i in range(len(m)):
        b = b + decimal_binary(ord(m[i]))[2:]
    L = len(b)  # L ils the length of the binary conversion of the message (before padding) L = len(m) * 8
    b = b + '1'  # add a bit that is equal to 1

    # with this simple while loop, we can get the total size of the padded message (we are looking for the smallest multiple of 512 that is larger than L)
    # we have to already factor in the 64 bits that will contain the final integer, as well as the bit set to 1 added previously
    # we don't need to factor in K, as it can be 0 if necessary
    total_size = 512
    while len(b) + 64 > total_size:
        total_size = total_size + 512

    # now we can easily compute K
    K = total_size - (len(b) + 64)

    # we add as many bits set to 0 as necessary (K bits)
    for i in range(K):
        b = b + '0'

    # now we only need to convert L into a 64 bit int, and add it to b
    L_b = bin(L)[2:]
    while len(L_b) < 64:
        L_b = '0' + L_b

    # finally we add L (binary of size 64) to the end of b
    b = b + L_b

    # b is now the binary padded message of size multiple to 512
    blocks = []
    while len(b) > 0:
        blocks.append(b[:512])
        b = b[512:]
    return blocks


# ######################################################################## first step : message padding -> DONE

# ######################################################################## second step : merkle damgard structure -> START

# donc comme décrit dans le pdf qui explique les étapes, on fait une première étape pour le premier bloc de message,
# si y a tjrs des bloques de messages, alors le hash deivent le input de la sha compression, et on le fait tant qu il y a des blocs
# au dernier on retorune le hash résultant
def merkle_damgard(message_blocks):
    iv_1_it = load_iv()  # all good
    c = sha_compression(message_blocks[0], iv_1_it)
    for i in range(1, len(message_blocks)):
        c = sha_compression(message_blocks[i], c)
    return c


# ######################################################################## second step : merkle damgard structure -> DONE


# ######################################################################## third step : global outline -> START


# function that takes as input a 512 bit message block - and 256 bit cipher(previous step) or iv
# outputs 256 bit hash
def sha_compression(m, c):
    words = []
    # split message of 512 bits into 16 words of 32 bits each
    for i in range(16):
        words.append(m[:32])
        m = m[32:]

    # now for the rest of the words !
    while len(words) < 64:
        i = len(words)

        # compute s0
        left = words[i - 15]  # 7 right rotates required
        left = right_rotate_shift(left, True, 7)
        middle = words[i - 15]  # 18 right rotates required
        middle = right_rotate_shift(middle, True, 18)
        right = words[i - 15]  # 3 right shifts required
        right = right_rotate_shift(right, False, 3)
        s0 = xor_32bit_word(xor_32bit_word(left, middle), right)

        # compute s1
        left = words[i - 2]  # 17 right rotates required
        left = right_rotate_shift(left, True, 17)
        middle = words[i - 2]  # 19 right rotates required
        middle = right_rotate_shift(middle, True, 19)
        right = words[i - 2]  # 10 right shifts required
        right = right_rotate_shift(right, False, 10)
        s1 = xor_32bit_word(xor_32bit_word(left, middle), right)

        sum_words = compute_sum([words[i - 16], s0, words[i - 7], s1])
        words.append(sum_words)

    # GENERATING OF WORDS IS CORRECT
    return compression_part(words, c)


# ######################################################################## third step : global outline -> DONE

# ######################################################################## fourth step : compression part -> START


# does the compression part (last step)
def compression_part(w, iv_hash):
    # on crée les valeurs a ... h
    a = iv_hash[:32]
    b = iv_hash[32:64]
    c = iv_hash[64:96]
    d = iv_hash[96:128]
    e = iv_hash[128:160]
    f = iv_hash[160:192]
    g = iv_hash[192:224]
    h = iv_hash[224:256]
    ki = load_ki()  # good
    for i in range(64):
        # on calcule les différentes valeurs selon les formules
        X1 = xor_32bit_word(xor_32bit_word(right_rotate_shift(e, True, 6), right_rotate_shift(e, True, 11)),
                            right_rotate_shift(e, True, 25))
        CH = xor_32bit_word(and_32bit_word(e, f), and_32bit_word(not_32bit_word(e), g))
        X2 = xor_32bit_word(xor_32bit_word(right_rotate_shift(a, True, 2), right_rotate_shift(a, True, 13)),
                            right_rotate_shift(a, True, 22))
        MAJ = xor_32bit_word(xor_32bit_word(and_32bit_word(a, b), and_32bit_word(a, c)), and_32bit_word(b, c))
        temp1 = compute_sum([h, X1, CH, ki[i], w[i]])
        temp2 = compute_sum([X2, MAJ])
        # TEMP 1 AND TEMP 2 ARE CORRECT
        h = g
        g = f
        f = e
        e = compute_sum([d, temp1])
        d = c
        c = b
        b = a
        a = compute_sum([temp1, temp2])
        # on reasigne les valuers selon les formules

    # on calcule new_h = h + a -> en mod 32 bits
    # ...
    # iv_hash = load_iv()
    a = compute_sum([iv_hash[:32], a])
    b = compute_sum([iv_hash[32:64], b])
    c = compute_sum([iv_hash[64:96], c])
    d = compute_sum([iv_hash[96:128], d])
    e = compute_sum([iv_hash[128:160], e])
    f = compute_sum([iv_hash[160:192], f])
    g = compute_sum([iv_hash[192:224], g])
    h = compute_sum([iv_hash[224:256], h])

    # on retourne la concaténation de tous les mots a .. h
    return a + b + c + d + e + f + g + h


# ######################################################################## fourth step : compression part -> DONE

# simple print du message et son hash
def print_hash(m, h):
    print("message : ", m)
    hash_x = '0x'
    while len(h) > 0:
        hash_x = hash_x + binary_str_to_hex(h[:4])
        h = h[4:]
    print("corresponding hash : ", hash_x)
    print()



# les 3 exemples du pdf
message = ""
message_blocks_ = generate_binary_message(message)
hash_ = merkle_damgard(message_blocks_)
print_hash(message, hash_)

message = "Welcome to Wrestlemania!"
message_blocks_ = generate_binary_message(message)
hash_ = merkle_damgard(message_blocks_)
print_hash(message, hash_)

message = "Fight for your dreams, and your dreams will fight for you!"
message_blocks_ = generate_binary_message(message)
hash_ = merkle_damgard(message_blocks_)
print_hash(message, hash_)
