import CBC
import sys

#file_name = input("Insira o nome do arquivo")
#chave = input("Insira a chave")

if len(sys.argv) == 3:
    file_name = sys.argv[0]
    key = sys.argv[1]
    if ".crpyto" in file_name:
        CBC.decrypt(file_name, key)
    else:
        CBC.encrypt(file_name, key)
else:
    print("Usage: crypto.py [input file] [key (4 bytes recommended)]")
