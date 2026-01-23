import multiprocessing
import time

def calculs():
    result = 0  
    time.sleep(0.2)  # Simule un calcul intensif
    for i in range(1, 1001):
        result += i

    return result

if __name__ == "__main__":
    print("Début exécution séquentielle")
    start_time = time.time()
    for _ in range(3):
        calculs()
    end_time = time.time()
    print(f"Temps pris en séquentiel: {end_time - start_time} secondes")

    print("Début exécution en multiprocessing")


    start_time = time.time()
    processes = []
    for _ in range(3):
        p = multiprocessing.Process(target=calculs)
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    end_time = time.time()
    print(f"Temps pris en multiprocessing: {end_time - start_time} secondes")