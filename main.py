from email_fetch import get_daily_email
from email_remove import tldr_cleanup
from ai_categorizer_1 import categorize_1
from ai_categorizer_2 import categorize_2
from ai_categorizer_3 import categorize_3
from auto_updating import updating
from add_application import add_application
import torch
import gc
import sys

def clear_gpu_memory():
    torch.cuda.empty_cache()  
    gc.collect()              
    print("GPU memory cleared.")

while(True):
    choice = input("""Welcome to Internship manager. Please choose an action: \n 
                   1. Check for Intership progress\n
                   2. Add a new application\n
                   3. Exit\n
                   Input your choice (1, 2 or 3): """)
    if int(choice) == 1:
        get_daily_email()
        tldr_cleanup("mails.csv")
        categorize_1()
        clear_gpu_memory()
        categorize_2()
        clear_gpu_memory
        categorize_3()
        updating()
    if int(choice) == 2:
        add_application()
    if int(choice) == 3:
        print("Exitting...")
        sys.exit()
    else:
        print("Unknown option picked. Resetting...")
        continue
