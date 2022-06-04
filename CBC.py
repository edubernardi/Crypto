import random
import numpy as np

def encrypt(input_file, key):
    if len(key) > 4:
        key = key[0: 4]
    while len(key) < 4:
        key += chr(random.randint(0, 256))

    file = open(input_file, "rb")
    output = open(input_file + ".crypto", "w")

    key_schedule(key, 20)

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
            round = 1
            while round < 18:
                key = key_schedule(key, round)

                round += 1
            buffer = np.packbits(buffer_bits)
            for byte in buffer:
                output.write(chr(byte))



def key_schedule(key, round):
    fibonacci = [0, 1]
    while len(fibonacci) < round * 4:
        fibonacci.append(fibonacci[len(fibonacci) - 1] + fibonacci[len(fibonacci) - 2])