import socket
import os
import sys

class Server():
    def __init__(self):
        # Vérifie qu'un argument est bien passé
        if len(sys.argv) != 3:
            print("Usage : python server.py <port> <nom_du_fichier>")
            sys.exit(1)

        self.nom_fichier = sys.argv[2]
        #verifie que le fichier existe
        try:
            with open(self.nom_fichier, 'rb') as f:
                pass
        except FileNotFoundError:
            print(f"{self.nom_fichier} : fichier introuvable")
            sys.exit(1)
        #verifie que le port est bien un nombre
        try:
            self.port = int(sys.argv[1])
        except:
            print("Usage : python server.py <port> <nom_du_fichier>")
            sys.exit(1)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #timeout pour les connections d'une seconde, permet d'arreter le server manuellement
        self.server_socket.settimeout(1.0)
        self.contenu = []

    def lire_fichier(self):
        #vide le contenu precedent
        self.contenu.clear()
        #découpage du fichier en blocs de 1024 bytes
        try:
            with open(self.nom_fichier, 'rb') as f:
                while (bloc := f.read(1024)):
                    self.contenu.append(bloc)
        except FileNotFoundError:
            print(f"{self.nom_fichier} : fichier introuvable")
            sys.exit(1)
        #On recupere la taille du fichier en nombre de blocs pour pouvoir l'envoyer au client
        self.taille = str(len(self.contenu))

    def boucle_server(self):
        #lance le server
        self.server_socket.bind(('127.0.0.1', self.port))
        print(f"Server en attente d'une connection sur le port {self.port}...")
        self.server_socket.listen(1)
        try:
            while True:
                try:
                    conn, addr = self.server_socket.accept()
                    print(f"{addr} connecté")
                    #envoi du nom du fichier
                    print(f"\nenvoi de {self.nom_fichier} vers {addr}\n")
                    conn.send(self.nom_fichier.encode())
                    #on recupere le contenu du fichier
                    self.lire_fichier()
                    #envoi de la taille du fichier au client en nombre de blocs de 1024 bytes
                    conn.send(self.taille.encode())
                    #envoi de chaque bloc un par un
                    for b in self.contenu:
                        conn.send(b)
                        

                    conn.close()
                except socket.timeout:
                    pass

        except KeyboardInterrupt:
            print("\nInterruption clavier détectée. Fin du programme.")
            self.server_socket.close()
            sys.exit(1)

if __name__ == "__main__":
    server = Server()
    server.boucle_server()
