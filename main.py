import sys
import torch
import gc
from email_fetch import get_daily_email
from email_remove import tldr_cleanup
from ai_categorizer_1 import categorize_1
from ai_categorizer_2 import categorize_2
from ai_categorizer_3 import categorize_3
from auto_updating import updating
from add_application import add_application

def clear_gpu_memory():
    torch.cuda.empty_cache()
    gc.collect()
    print("GPU memory cleared.")

def daily_check():
    print("Running daily check...")
    get_daily_email()
    tldr_cleanup("mails.csv")
    categorize_1()
    clear_gpu_memory()
    categorize_2()
    clear_gpu_memory()
    categorize_3()
    updating()
    print("Daily check completed.")

def interactive_mode():
    while True:
        choice = input("""Welcome to Internship Manager. Please choose an action:
                   1. Check for Internship Progress
                   2. Add a New Application
                   3. Exit
                   Input your choice (1, 2, or 3): """)
        if choice == "1":
            daily_check()
        elif choice == "2":
            add_application()
        elif choice == "3":
            print("Exiting...")
            sys.exit()
        else:
            print("Unknown option picked. Please try again.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "daily_check":
        daily_check()
    else:
        interactive_mode()
