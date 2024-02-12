from playwright.sync_api import sync_playwright
import os
import torch
from torchvision import transforms
from PIL import Image
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
from utils.crnn import CRNN
from utils.ocr import OCR
from utils.ocrsolver import solve_captcha

def scrape_product_details(url: str):
    with sync_playwright() as p:
        # Avvia il browser in modalità headless
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        # Vai alla URL del prodotto
        page.goto(url)

        # Cerca l'elemento del captcha
        captcha_img = page.query_selector("img[src*='captcha']")

        # Se il captcha è presente, ottieni l'URL
        if captcha_img:
            captcha_url = captcha_img.get_attribute("src")
            # Ottieni il percorso assoluto del file del tuo script Python
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Costruisci il percorso relativo al file "model.pth"
            model_path = os.path.join(script_dir, "model15.pth")
            print("model path ", model_path)
            # Utilizza il percorso relativo nella tua funzione
            solution = solve_captcha(model_path, captcha_url)
            print("solutin", solution)
            captcha_input_selector = '#captchacharacters'
            page.fill(captcha_input_selector, solution)
            # Simula la pressione del tasto "Enter"
            page.press(captcha_input_selector, 'Enter')
       

        all_results = []


        product_link_selector = 'a[data-hook="product-link"]'
        page.wait_for_selector(product_link_selector)
        page.click(product_link_selector)
        page.mouse.wheel(0, 100)
        page.wait_for_load_state("load")

        # titolo
        product_title_selector = 'span#productTitle'
        page.wait_for_selector(product_title_selector)
        product_title = page.inner_text(product_title_selector).strip()

        # url img
        product_image_selector = 'img#landingImage'
        page.wait_for_selector(product_image_selector)
        product_image_url = page.get_attribute(product_image_selector, 'src')

        # voto
        # Seleziona il div contenitore basato sull'ID
        rating_xpath = '//*[@id="averageCustomerReviews_feature_div"]//span[contains(text(), "su 5 stelle")]'
        # All'interno di quel contenitore, cerca uno span che contiene il testo della valutazione
        # Qui assumiamo che la valutazione sia sempre seguita da "su 5 stelle"
        rating = page.inner_text(f'xpath={rating_xpath}')


        """rating_selector = 'span.a-size-base.a-color-base'
        page.wait_for_selector(rating_selector)
        rating = page.inner_text(rating_selector).strip()"""

         # categoria
        category_selector = 'a.a-link-normal.a-color-tertiary'
        page.wait_for_selector(category_selector)
        category = page.inner_text(category_selector).strip()

        
        # Restituisce titolo e URL dell'immagine del prodotto
        return {
            "product_title": product_title,
            "product_image_url": product_image_url,
            "rating": rating,
            "category": category
        }
