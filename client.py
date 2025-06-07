import os
import sys
import socket
import ipaddress

def ip(valeur):
    try:
        ipaddress.ip_address(valeur)
        return True
    except ValueError:
        return False
#verifie les paramètre spécifiés
if len(sys.argv) != 3:
    print("Usage : python client.py <ip server> <port>")
    sys.exit(1)
if ip(sys.argv[1]) == False:
    #si l'ip specifie est incorrecte
    print("Usage : python client.py <ip server> <port>")
    sys.exit(1)
try:
    port = int(sys.argv[2])
except:
    print("Usage : python server.py <port> <nom_du_fichier>")
    sys.exit(1)

ipServer = sys.argv[1]
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ipServer, port))

nom_fichier = client_socket.recv(1024).decode()

taille_recue = client_socket.recv(1024)
taille = int(taille_recue.decode())
contenu = b''


#reception de chaque bloc
for i in range(taille):
    b = client_socket.recv(1024)
    contenu += b

client_socket.close()

#ecriture du fichier
with open(nom_fichier, "wb") as f:
    f.write(contenu)
print(f"\n{nom_fichier} reçu du server\n")
