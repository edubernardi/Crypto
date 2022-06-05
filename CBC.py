import random
import numpy as np

expansion_table = [24, 1 , 2 , 3 , 4 , 5 ,
                   4 , 5, 6 , 7 , 8 , 9 ,
                   8 , 9 , 10, 11, 12, 13,
                   12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21,
                   20, 21, 22, 23, 24, 1]

s_box = [[0, 1, 7, 3],
         [5, 2, 4, 7],
         [2, 6, 3, 1],
         [6, 4, 0, 5]]

def encrypt(input_file, key):
    if len(key) > 4:
        key = key[0: 4]
    while len(key) < 4:
        key += chr(random.randint(0, 256))
    file = open(input_file, "rb")
    output = open(input_file + ".crypto", "wb")

    end_of_file = False

    while not end_of_file:
        buffer = file.read(6)
        if len(buffer) < 1:
            end_of_file = True
        else:
            buffer = bytearray(buffer)
            while len(buffer) < 6:
                buffer.append(0)
            # permutacoes
            buffer_bits = np.unpackbits(buffer)

            buffer_bits1 = expand(buffer_bits[0: 24], 32)
            buffer_bits2 = expand(buffer_bits[24: 48], 32)
            buffer_bits3 = np.ndarray(64, int)
            round = 1
            while round < 2:
                key = key_schedule(key, round)
                key_bytes = bytearray(4)
                for char in key:
                    key_bytes.append(ord(char))
                key_bits = np.unpackbits(key_bytes)
                i = 0
                while i < 64:
                    if i < 32:
                        if buffer_bits1[i] == key_bits[i]:
                            buffer_bits3[i] = 0
                        else:
                            buffer_bits3[i] = 1
                        i += 1
                    else:
                        if buffer_bits2[i - 32] == key_bits[i]:
                            buffer_bits3[i] = 0
                        else:
                            buffer_bits3[i] = 1
                        i += 1
                buffer_bits4 = substitution(buffer_bits3)


                round += 1

            print(buffer_bits4)
            buffer = bytearray(np.packbits(buffer_bits4))
            for byte in buffer:
                output.write(bytes([byte]))

def decrypt(input_file, key):
    if len(key) > 4:
        key = key[0: 4]
    while len(key) < 4:
        key += chr(random.randint(0, 256))
    file = open(input_file, "rb")
    output = open(input_file + ".decrypt", "wb")

    end_of_file = False

    while not end_of_file:
        buffer = file.read(6)
        if len(buffer) < 1:
            end_of_file = True
        else:
            buffer = bytearray(buffer)
            while len(buffer) < 6:
                buffer.append(0)
            # permutacoes
            buffer_bits = np.unpackbits(buffer)

            buffer_bits1 = expand(buffer_bits[0: 24], 32)
            buffer_bits2 = expand(buffer_bits[24: 48], 32)
            buffer_bits3 = np.ndarray(64, int)
            round = 1
            while round < 2:
                key = key_schedule(key, round)
                key_bytes = bytearray(4)
                for char in key:
                    key_bytes.append(ord(char))
                key_bits = np.unpackbits(key_bytes)
                i = 0
                while i < 64:
                    if i < 32:
                        if buffer_bits1[i] == key_bits[i]:
                            buffer_bits3[i] = 0
                        else:
                            buffer_bits3[i] = 1
                        i += 1
                    else:
                        if buffer_bits2[i - 32] == key_bits[i]:
                            buffer_bits3[i] = 0
                        else:
                            buffer_bits3[i] = 1
                        i += 1
                buffer_bits4 = substitution(buffer_bits3)
                round += 1

            print(buffer_bits4)
            buffer = bytearray(np.packbits(buffer_bits4))
            for byte in buffer:
                output.write(bytes([byte]))


def key_schedule(key, round):
    fibonacci = [0, 1]
    while len(fibonacci) < round * 4:
        fibonacci.append(fibonacci[len(fibonacci) - 1] + fibonacci[len(fibonacci) - 2])
    new_key = list(key)
    i = 0
    while i < 4:
        new_key[i] = chr((ord(new_key[i]) + fibonacci[4 * (round - 1) + i] + ord(new_key[(i - 1) % 4])) % 256)
        i += 1

    return "".join(new_key)


def expand(buffer, size):
    expanded = np.ndarray(32, int)
    for i in range(0, size):
        expanded[i] = buffer[expansion_table[i] - 1]
    return expanded


def substitution(original):
    i = 0
    result = []
    while i < 64:
        column = bits_to_decimal(original[i: i + 2])
        line = bits_to_decimal(original[i + 2: i + 4])
        new_values = decimal_to_3bits(s_box[column][line])
        for bit in new_values:
            result.append(bit)
        i += 4
    return result

def bits_to_decimal(bits):
    sum = 0
    exponent = len(bits) - 1
    for bit in bits:
        if bit == 1:
            sum += 2 ** exponent
        exponent -= 1
    return sum

def decimal_to_3bits(value):
    result = [0, 0, 0]
    i = 2
    while 0 < value < 8:
        if value % 2 == 0:
            result[i] = 0
        else:
            result[i] = 1
            value -= 1
        i -= 1
        value = int(value / 2)
    return result