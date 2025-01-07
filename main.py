from email_fetch import get_daily_email
from email_remove import tldr_cleanup
from ai_categorizer_1 import categorize_1
from ai_categorizer_2 import categorize_2
import torch
import gc

def clear_gpu_memory():
    torch.cuda.empty_cache()  
    gc.collect()              
    print("GPU memory cleared.")

get_daily_email()
tldr_cleanup("mails.csv")
categorize_1()
clear_gpu_memory()
categorize_2()
