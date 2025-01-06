from email_fetch import get_daily_email
from email_remove import tldr_cleanup
from ai_categorizer_1 import categorize_1
from ai_categorizer_2 import categorize_2
import torch
import gc

def clear_gpu_memory():
    """
    Clears GPU memory by deleting unused variables and invoking garbage collection.
    """
    torch.cuda.empty_cache()  # Free up unused GPU memory
    gc.collect()              # Force garbage collection to release CPU memory
    print("GPU memory cleared.")

get_daily_email()
tldr_cleanup("mails.csv")
categorize_1()
clear_gpu_memory()
categorize_2()