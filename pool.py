from multiprocessing import Pool
import time

def calcul_carre(n):
    """Calcule le carré d'un nombre."""
    time.sleep(0.1)  # Simule un calcul
    return n * n

if __name__ == "__main__":
    nombres = list(range(1, 11))
    
    print("Calcul séquentiel...")
    debut = time.time()
    resultats_seq = [calcul_carre(n) for n in nombres]
    temps_seq = time.time() - debut
    print(f"Temps: {temps_seq:.2f}s")
    
    print("\nCalcul parallèle avec Pool...")
    debut = time.time()
    with Pool(processes=8) as pool:
        resultats_par = pool.map(calcul_carre, nombres)
    temps_par = time.time() - debut
    print(f"Temps: {temps_par:.2f}s")
    print(f"Accélération: {temps_seq/temps_par:.2f}x")
    
    print(f"\nRésultats: {resultats_par}")