from PIL import Image
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from utils.crnn import CRNN
from utils.ocr import OCR
import requests
import io

def solve_captcha(model_path, img_url):
    # Carica il modello salvato
    loaded_model = torch.load(model_path, map_location=torch.device('cpu'))

    # Crea un'istanza OCR e carica il modello
    ocr = OCR()
    ocr.crnn = loaded_model

    # Scarica l'immagine dall'URL e la apre
    response = requests.get(img_url)
    img = Image.open(io.BytesIO(response.content)).convert('RGB')

    # Trasforma l'immagine
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    img_tensor = transform(img)

    # Aggiungi una dimensione batch
    img_tensor = img_tensor.unsqueeze(0)

    # Esegui la predizione
    logits = ocr.predict(img_tensor)

    # Decodifica la predizione
    pred_text = ocr.decode(logits.cpu())
    
    return pred_text

