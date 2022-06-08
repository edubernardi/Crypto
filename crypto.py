#Alunos participantes: Eduardo Bernardi e Guilherme Spohr Rabelo
import CBC
import sys
import numpy as np

if len(sys.argv) == 3:
    file_name = sys.argv[1]
    key = sys.argv[2]
    if ".crypto" in file_name:
        CBC.decrypt(file_name, key, True)
    else:
        CBC.encrypt(file_name, key, False)
else:
    print("Usage: crypto.py [input file (.crypto to decode)] [key (4 bytes long)]")
