import os
import sys
import csv
from openai import OpenAI
import constants


os.environ["OPENAI_API_KEY"] = constants.APIKEY
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)



def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        reviews = [row['review_text'] for row in reader]
    return reviews

def analyze_review(review):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": review}
        ]
    )

    # Ottieni l'ultima risposta dell'assistente
    last_message = completion.choices[-1].message['content']
    return last_message.strip()



