# gonna sha it up


# ######################################################################## useful functions that aren't specific to one step -> START


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
    L_b = decimal_binary(L)[2:]
    while len(L_b) < 64:
        L_b = '0' + L_b

    # finally we add L (binary of size 64) to the end of b
    b = b + L_b

    # b is now the binary padded message of size multiple to 512
    return b


# ######################################################################## first step : message padding -> DONE

# ######################################################################## second step : merkle damgard structure -> START
# ######################################################################## second step : merkle damgard structure -> DONE
# ######################################################################## third step : global outline -> START


# function that does right rotate or right shift depending on f (true = rotate)
def right_rotate_shift(w, f):  # VERIFIED
    a = '0'
    # if f is set to true, then it is a rotate, if f is set to true, it is a shift
    if f:
        a = w[-1]
    return a + w[:-1]


# computes xor of two 32 bit words
def xor_32bit_word(w1, w2):  # VERIFIED
    w_res = ''
    for i in range(len(w1)):
        if w1[i] == w2[i]:
            w_res = w_res + '0'
        else:
            w_res = w_res + '1'
    return w_res


# function that takes as input a 512 bit message block - and 256 bit cipher(previous step) or iv
# outputs 256 bit hash
def sha_compression(m, c):
    words = []
    # split message of 512 bits into 16 words of 32 bits each
    for i in range(16):
        words.append(m[:32])
        m = m[32:]

    return


# ######################################################################## third step : global outline -> DONE

message = "Salut"
bi = generate_binary_message(message)
sha_compression(bi, message)
