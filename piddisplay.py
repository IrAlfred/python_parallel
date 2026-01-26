import os
import multiprocessing
import threading

def display_pidThread():
    print(f"PID dans [thread]: {os.getpid()}")

def display_pidProcess():
    print(f"PID dans [process]: {os.getpid()}")

if __name__ == "__main__":
    print(f"PID dans [main]: {os.getpid()}")

    thread = threading.Thread(target=display_pidThread)
    thread.start()
    thread.join()  

    process = multiprocessing.Process(target=display_pidProcess)
    process.start()
    process.join()

    process2 = multiprocessing.Process(target=display_pidProcess)
    process2.start()
    process2.join()
