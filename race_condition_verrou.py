import threading
import time
nb = 0

verrou = threading.Lock()

def compteur():
    global nb
    
    for _ in range(100):
        with verrou:
            valeur_actuelle = nb
            time.sleep(0.0001)
            nb = valeur_actuelle + 1


if __name__ == "__main__":
    for _ in range(5):
        compteur()
    print(f"valeur avec exécution séquentielle : {nb}")

    nb = 0
    threads = []
    for _ in range(5):
        t = threading.Thread(target=compteur)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"valeur avec exécution parallèle : {nb}")
