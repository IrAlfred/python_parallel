from multiprocessing import Process, Pipe
import os

# Créer un pipe avec deux connexions
parent_conn, child_conn = Pipe()

# Processus parent : envoyer et recevoir
def processus_parent(conn):
    conn.send(f"message du parent PID {os.getpid()}")  # Envoyer un message
    #reponse = conn.recv()  # Recevoir la réponse
    #print(reponse)

# Processus enfant : recevoir et envoyer
def processus_enfant(conn):
    message = conn.recv()  # Recevoir le message
    print(message)
    #conn.send(f"réponse de l'enfant, PID {os.getpid()}")  # Envoyer une réponse

# Utilisation
p = Process(target=processus_enfant, args=(child_conn,))
p.start()
p_parent = Process(target=processus_parent, args=(parent_conn,))
p_parent.start()
p.join()
p_parent.join()