import threading

semaphore = threading.Semaphore(3)  # Limite à 3 threads simultanés

def task(thread_id):
    with semaphore:
        print(f"Thread {thread_id} is running")


if __name__ == "__main__":
    threads = []
    for i in range(10):
        t = threading.Thread(target=task, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()