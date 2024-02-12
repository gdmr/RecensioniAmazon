import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def calcola_percentuale_veri(file_csv):
    try:
        print(file_csv)
        # Leggi il file csv
        df = pd.read_csv(file_csv)
        
        # Prendi le recensioni
        recensioni = df['review_text'].tolist()[:11]

        model = AutoModelForSequenceClassification.from_pretrained("Sarwar242/autotrain-fake-reviews-labelling-37433101195", token="INSERIRE LA PROPRIA APIKEY")
        tokenizer = AutoTokenizer.from_pretrained("Sarwar242/autotrain-fake-reviews-labelling-37433101195", token="INSERIRE LA PROPRIA APIKEY")
        # Trasforma le recensioni in input per il modello
        inputs = tokenizer(recensioni, return_tensors="pt", padding=True, truncation=True, max_length=512)

        # Ottieni l'output del modello
        outputs = model(**inputs)
        # Prendi i logits dal tuo output
        logits = outputs.logits

        # Applica la funzione softmax ai logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)

        # Conta quante volte la probabilità per la seconda categoria è superiore a 0.5
        count = (probabilities[:, 1] > 0.5).sum()

        # Calcola la percentuale di volte in cui la probabilità per la seconda categoria è superiore a 0.5
        percentage = count.item() / probabilities.shape[0] * 100

        return percentage
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        # Potresti voler restituire un valore speciale o sollevare nuovamente l'eccezione
        # raise e
        return None
