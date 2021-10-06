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


# input : k hexadecimal values (str -> "0xa1"), output : a str of bits (-> "0b10100001")
def hex_to_binary_list(hex):
    return bin(int(hex, 16))  # [2:] -> pour enlever 0b


# input : a srt of n bits (-> "0b10100001"), output : hexadecimal values (str -> "0xa1")
def binary_list_to_hex(binary):
    return hex(int(binary, 2))  # [2:] -> pour enlever 0x


# generate [k_{0}, k_{1}, .... , k_{N-1}]
def generate_k_n_1(key_input, n):
    k = []

    for i in range(n):
        ki = []
        for j in range(4):
            s = i * len(k)
            ki.append(key_input[s + j])
        k.append(ki)
    return k


# key expansion, key is in hex -> need to create nb of rounds + 1 key -> 11 keys
def key_expansion(key_):
    return null
