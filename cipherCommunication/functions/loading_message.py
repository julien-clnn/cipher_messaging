import os, threading, time
from functions.colors import RESET, CYAN

def display_loading_message(loading_done_event):
    """
    Display a loading animation until a specified event is set.

    Args:
        loading_done_event (threading.Event): An event object that controls when the loading animation should stop.

    Returns:
        threading.Thread: The thread running the loading animation.
    """
    def loading_animation():
        loading_message = "Please wait"
        while not loading_done_event.is_set():
            for i in range(4): 
                os.system('clear')  
                print(f"{CYAN}{loading_message}{'.' * i}{RESET}")
                time.sleep(0.5) 
            os.system('clear') 

    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()
    
    return loading_thread