from time import sleep
from threading import Event, Thread

condition = Event()

def do_sth(ab):
    return (f"printing {ab}")

def check_sth(ab):
    while not condition.is_set():
        sleep(0.25)
        do_sth(ab)  # Do something everytime the condition is not set.

    return ("Condition met, ending.")

def start_thread(ab):
    s=Thread(target=check_sth, args=(ab)).start()
    return s
def close_thread():
    global condition
    condition.set()  # End while loop.
    return