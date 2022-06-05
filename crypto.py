import CBC
import sys
import numpy as np

#file_name = input("Insira o nome do arquivo")
#chave = input("Insira a chave")

if len(sys.argv) == 3:
    file_name = sys.argv[1]
    key = sys.argv[2]
    if ".crypto" in file_name:
        CBC.decrypt(file_name, key)
    else:
        CBC.encrypt(file_name, key)
else:
    print("Usage: crypto.py [input file] [key (4 bytes recommended)]")
