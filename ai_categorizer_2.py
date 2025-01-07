from transformers import pipeline
import pandas as pd
import re

def extract_main_content_batch(email_bodies, generator):
    prompts = [
        (
        """The following is an email body with a lot of noise, including HTML tags, weird elements, greetings, signatures, and irrelevant content. The email is about an internship application process. Your task is to decide if the email is about:
        1. A confirmation that the application process has started or that the application process is still ongoing.
        2. A positive answer about my application such as an intership offer, or an interview offer.
        3. A refusal for my application.
        Return either 1, if it's a confirmation that my application process has started or that the process is still ongoing. 2 if it's positive answer about my application such as an intership offer, or an interview offer. And 3 if it's a refusal for my application.
        Please only return 1, 2, or 3 based on the instructions i gave you and nothing else.\n\n"""
        f"Email body:\n{email_body}\n\n1, 2, or 3:"
        )
        for email_body in email_bodies
    ]

    responses = generator(prompts, max_new_tokens=2, temperature=0.4)

    flat_responses = [response['generated_text'] for batch in responses for response in batch]
    return flat_responses


def categorize_2(batch_size=4):
    print("Second categorization phase starting...")
    df = pd.read_csv('mails.csv')
    df['Application progress'] = None
    generator = pipeline("text-generation", model="unsloth/Llama-3.2-3B-Instruct", device=0)

    email_bodies = df.loc[df["Internship?"] == "Yes", "Body"].tolist()
    email_indices = df.loc[df["Internship?"] == "Yes"].index
    num_emails = len(email_bodies)
    results = []

    for i in range(0, num_emails, batch_size):
        batch = email_bodies[i:i + batch_size]
        batch_results = extract_main_content_batch(batch, generator)

        for response in batch_results:
            match = re.search(r"1, 2, or 3: (\d+)", response)  
            if match:
                results.append(match.group(1)) 
            else:
                results.append(None)
        
        print(f"Processed batch {i // batch_size + 1}/{(num_emails + batch_size - 1) // batch_size}")

    for idx, result in zip(email_indices, results):
        df.at[idx, 'Application progress'] = result

    df.to_csv('mails.csv', index=False)
    print("Second categorization phase completed.")

