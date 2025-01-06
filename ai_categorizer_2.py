from transformers import pipeline
import pandas as pd
import re

def extract_main_content(email_body, generator):
    prompt = (
        """The following is an email body with a lot of noise, including HTML tags, weird elements, greetings, signatures, and irrelevant content. The email is about an internship application process. Your task is to decide if the email is about:
        1. A confirmation that the application process has started or that the application process is still ongoing.
        2. A positive answer about my application such as an intership offer, or an interview offer.
        3. A refusal for my application.
        Return either 1, if it's a confirmation that my application process has started. 2 if it's positive answer about my application such as an intership offer, or an interview offer. And 3 if it's a refusal for my application.
        Please only return 1, 2, or 3 based on the instructions i gave you and nothing else.\n\n"""
        f"Email body:\n{email_body}\n\n1, 2, or 3:"
    )
    response = generator(prompt, max_new_tokens=3, temperature=0.4)
    return response[0]['generated_text']

def categorize_2():
    print("Second categorization phase starting...")
    df = pd.read_csv('mails.csv')
    df['Application progress'] = None
    generator = pipeline("text-generation", model="unsloth/Llama-3.2-3B-Instruct", device=0)
    count = 1
    for index, row in df.iterrows():
        if row["Internship?"] == "No":
            continue
        email = row['Body']
        main_content = extract_main_content(email, generator)
        match = re.search(r"1, 2, or 3: (\w+)", main_content)

        if match:
            word_after = match.group(1)
            df['Application progress'] = word_after
        else:
            df['Application progress'] = None
        print(f"Email {count} categorized")
        count += 1
    df.to_csv('mails.csv', index=False)


