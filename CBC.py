import random
import numpy as np

expansion_table = [32, 1 , 2 , 3 , 4 , 5 , 4 , 5,
                 6 , 7 , 8 , 9 , 8 , 9 , 10, 11,
                 12, 13, 12, 13, 14, 15, 16, 17,
                 16, 17, 18, 19, 20, 21, 20, 21,
                 22, 23, 24, 25, 24, 25, 26, 27,
                 28, 29, 28, 29, 30, 31, 32, 1]

s_box = [[11, 14, 7, 3],
         [5, 2, 12, 8],
         [10, 6, 13, 1],
         [9, 4, 0, 15]]

s_box_inverted = [[11, 7, 13, 9],
                  [14, 1, 3, 10],
                  [5, 6, 2, 4],
                  [12, 8, 0, 15]]

def encrypt(input_file, key, decrypt):
    if len(key) >= 4:
        key = key[0: 4]
    else:
        return
    file = open(input_file, "rb")
    extension = ".crypto"
    if decrypt:
        extension = ".decrypt"
    output = open(input_file + extension, "wb")

    end_of_file = False
    original_key = key
    while not end_of_file:
        buffer = file.read(6)
        if len(buffer) < 1:
            end_of_file = True
        else:
            buffer = bytearray(buffer)
            while len(buffer) < 6:
                buffer.append(0)

            buffer_bits = np.unpackbits(buffer)

            round = 1
            max_rounds = 15
            key = original_key
            while round < max_rounds:
                key = key_schedule(key, round)
                key_bytes = bytearray()
                for char in key:
                    key_bytes.append(ord(char))

                #Caesar Cipher
                i = 0
                while i < 4:
                    key_bytes[i] = (key_bytes[i] + round) % 256
                    i += 1

                key_bits = expand(np.unpackbits(key_bytes), 48)

                #XOR
                i = 0
                while i < 48:
                    if buffer_bits[i] == key_bits[i]:
                        buffer_bits[i] = 0
                    else:
                        buffer_bits[i] = 1
                    i += 1

                #Substitution
                buffer_bits = substitution(buffer_bits, decrypt)
                round += 1

            buffer = bytearray(np.packbits(buffer_bits))

            for byte in buffer:
                output.write(bytes([byte]))


def decrypt(input_file, key, decrypt):
    if len(key) >= 4:
        key = key[0: 4]
    else:
        return
    file = open(input_file, "rb")
    extension = ".crypto"
    if decrypt:
        extension = ".decrypt"
    output = open(input_file + extension, "wb")

    end_of_file = False
    original_key = key
    while not end_of_file:
        buffer = file.read(6)
        if len(buffer) < 1:
            end_of_file = True
        else:
            buffer = bytearray(buffer)
            while len(buffer) < 6:
                end_of_file = True
                buffer.append(0)

            buffer_bits = np.unpackbits(buffer)

            round = 1
            max_rounds = 15
            key = original_key
            while round < max_rounds:
                key = reverse_key_schedule(original_key, round, max_rounds) #generating keys backwards
                key_bytes = bytearray()
                for char in key:
                    key_bytes.append(ord(char))

                #Caesar Cipher
                i = 0
                while i < 4:
                    key_bytes[i] = (key_bytes[i] + (max_rounds - round)) % 256
                    i += 1

                key_bits = expand(np.unpackbits(key_bytes), 48)

                #Decrypt substitution
                buffer_bits = substitution(buffer_bits, decrypt)

                #XOR
                i = 0
                while i < 48:
                    if buffer_bits[i] == key_bits[i]:
                        buffer_bits[i] = 0
                    else:
                        buffer_bits[i] = 1
                    i += 1

                round += 1



            #final permutation
            buffer = bytearray(np.packbits(buffer_bits))

            #check if last block
            next = file.read(1)
            if len(next) > 0:
                file.seek(-1, 1)
            else:
                end_of_file = True

            #remove padding
            if end_of_file:
                i = 5
                while i >= 0:
                    if int(buffer[i]) == 0:
                        buffer.pop(i)
                    else:
                        break
                    i -= 1

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


def reverse_key_schedule(key, round, max_rounds):
    original_rounds = round
    new_key = list(key)
    round = 1
    while round < (max_rounds - (original_rounds - 1)):
        fibonacci = [0, 1]
        while len(fibonacci) < round * 4:
            fibonacci.append(fibonacci[len(fibonacci) - 1] + fibonacci[len(fibonacci) - 2])
        i = 0
        while i < 4:
            new_key[i] = chr((ord(new_key[i]) + fibonacci[4 * (round - 1) + i] + ord(new_key[(i - 1) % 4])) % 256)
            i += 1
        round += 1
    return "".join(new_key)


def expand(buffer, size):
    expanded = np.ndarray(size, int)
    for i in range(0, size):
        expanded[i] = buffer[expansion_table[i] - 1]
    return expanded


def substitution(original, inverted):
    i = 0
    result = []
    while i < 48:
        column = bits_to_decimal(original[i: i + 2])
        line = bits_to_decimal(original[i + 2: i + 4])
        if inverted:
            new_values = decimal_to_bits(s_box_inverted[line][column])
        else:
            new_values = decimal_to_bits(s_box[line][column])
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


def decimal_to_bits(value):
    result = [0, 0, 0, 0]
    i = 3
    while 0 < value < 16:
        if value % 2 == 0:
            result[i] = 0
        else:
            result[i] = 1
            value -= 1
        i -= 1
        value = int(value / 2)
    return result
