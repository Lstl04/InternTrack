import pandas as pd
def tldr_cleanup(file):
    df = pd.read_csv(file)

    for index, row in df.iterrows():
        if 'TLDR' in row['From']:
            df.drop(index, inplace=True)

    df.reset_index(drop=True, inplace=True)
    df.to_csv('mails.csv', index=False)
    print("TLDR emails removed")

