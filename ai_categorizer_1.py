from transformers import pipeline
import pandas as pd
import re
import sys

def extract_main_content_batch(email_bodies, generator):
    
    prompts = [
        (
            "The following is an email body with a lot of noise, including HTML tags, weird elements, greetings, "
            "signatures, and irrelevant content. Your task is to decide if the email concerns one of my internship "
            "applications. If it is about an internship application process, return Yes, for anything else return No.\n\n"
            f"Email body:\n{email_body}\n\nIs it internship related?:"
        )
        for email_body in email_bodies
    ]

    responses = generator(prompts, max_new_tokens=2, temperature=0.4)

    flat_responses = [response['generated_text'] for batch in responses for response in batch]
    return flat_responses

def categorize_1(batch_size=4):
    
    print("First categorization phase starting...")
    df = pd.read_csv('mails.csv')
    df['Internship?'] = None
    generator = pipeline("text-generation", model="unsloth/Llama-3.2-3B-Instruct", device=0)

    email_bodies = df['Body'].tolist()
    num_emails = len(email_bodies)
    results = []

    for i in range(0, num_emails, batch_size):
        batch = email_bodies[i:i + batch_size]
        batch_results = extract_main_content_batch(batch, generator)
        
        for response in batch_results:
            match = re.search(r"Is it internship related\?: (\w+)", response)
            if match:
                results.append(match.group(1))
            else:
                results.append(None)
        
        print(f"Processed batch {i // batch_size + 1}/{(num_emails + batch_size - 1) // batch_size}")

    df['Internship?'] = results

    internship_emails_count = sum(1 for result in results if result == "Yes")
    if internship_emails_count == 0:
        df.to_csv('mails.csv', index=False)
        print("No emails received about internship")
        sys.exit()

    df.to_csv('mails.csv', index=False)
    print("Categorization phase completed.")
