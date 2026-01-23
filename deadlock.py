import threading
import time

# Create two locks
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1_function():
    """Thread 1 acquires lock1 then lock2"""
    print("Thread 1: Trying to acquire lock1")
    lock1.acquire()
    print("Thread 1: Acquired lock1")
    
    time.sleep(0.1)  # Small delay to increase chance of deadlock
    
    print("Thread 1: Trying to acquire lock2")
    lock2.acquire()  # This will wait forever for lock2 (deadlock!)
    print("Thread 1: Acquired lock2")
    
    # Critical section
    print("Thread 1: Doing work...")
    
    lock2.release()
    lock1.release()
    print("Thread 1: Released both locks")

def thread2_function():
    """Thread 2 acquires lock2 then lock1"""
    print("Thread 2: Trying to acquire lock2")
    lock2.acquire()
    print("Thread 2: Acquired lock2")
    
    time.sleep(0.1)  # Small delay to increase chance of deadlock
    
    print("Thread 2: Trying to acquire lock1")
    lock1.acquire()  # This will wait forever for lock1 (deadlock!)
    print("Thread 2: Acquired lock1")
    
    # Critical section
    print("Thread 2: Doing work...")
    
    lock1.release()
    lock2.release()
    print("Thread 2: Released both locks")

# Create and start threads
thread1 = threading.Thread(target=thread1_function)
thread2 = threading.Thread(target=thread2_function)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Program completed (this won't print due to deadlock)")