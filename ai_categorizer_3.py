from transformers import pipeline
import pandas as pd
import re

def extract_main_content_batch(email_bodies, generator):
    prompts = [
        (
        """The following is an email body with a lot of noise, including HTML tags, weird elements, greetings, signatures, and irrelevant content. The email is about an internship application process. Your task is to determine what company the application is about. 
        Please return the name of the company for which the email is about, and nothing. Only the name of the company.\n\n"""
        f"Email body:\n{email_body}\n\nCompany name:"
        )
        for email_body in email_bodies
    ]

    responses = generator(prompts, max_new_tokens=5, temperature=0.4)

    flat_responses = [response['generated_text'] for batch in responses for response in batch]
    return flat_responses


def categorize_3(batch_size=4):
    print("Defining company phase starting...")
    df = pd.read_csv('mails.csv')
    df['Company name'] = None
    generator = pipeline("text-generation", model="google-bert/bert-base-uncased", device=0)

    email_bodies = df.loc[df["Internship?"] == "Yes", "Body"].tolist()
    email_indices = df.loc[df["Internship?"] == "Yes"].index
    num_emails = len(email_bodies)
    results = []

    for i in range(0, num_emails, batch_size):
        batch = email_bodies[i:i + batch_size]
        batch_results = extract_main_content_batch(batch, generator)

        for response in batch_results:
            match = re.search(r"Company name: (\w+)", response)  
            if match:
                results.append(match.group(1)) 
            else:
                results.append(None)
        
        print(f"Processed batch {i // batch_size + 1}/{(num_emails + batch_size - 1) // batch_size}")

    for idx, result in zip(email_indices, results):
        df.at[idx, 'Company name'] = result

    df.to_csv('mails.csv', index=False)
    print("Company name phase completed.")

