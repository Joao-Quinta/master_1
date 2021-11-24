def bin_str_sum(add_here, add_this):
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
    add_here.reverse()
    add_here = ''.join(add_here)
    return add_here


s1 = '01101000011001010110110001101100'
s2 = '11001110111000011001010111001011'
s3 = '00000000000000000000000000000000'
s4 = '00000000000000000000000000000000'

print(s1 == '01101000011001010110110001101100')
print(s2 == '11001110111000011001010111001011')
print(s3 == '00000000000000000000000000000000')
print(s4 == '00000000000000000000000000000000')

to_sum = [s1, s2, s3, s4]

total = '00000000000000000000000000000000'
total = list(total)

for i in range(len(to_sum)):
    total = bin_str_sum(total, to_sum[i])
    print(i, ' : ', total)

print(total)
print(len(total))

print('aaa -> ', total == '00110111010001110000001000110111')

