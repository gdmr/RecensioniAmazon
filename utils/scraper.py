from playwright.sync_api import sync_playwright
import os
import csv
import sys
import re
import torch
from torchvision import transforms
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from utils.ocrsolver import solve_captcha
from utils.crnn import CRNN
from utils.ocr import OCR




def clean_text(text):
    """Clean text by removing unwanted characters and whitespace."""
    # Rimuove gli spazi multipli e sostituiscili con un singolo spazio
    text = re.sub(r'\s+', ' ', text)
    # Rimuove gli spazi all'inizio e alla fine della stringa
    return text.strip()

def run(playwright, url, start_page, end_page, save_dir, nome):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    print("Run avviato")

    page.goto(url)

     # Cerca l'elemento del captcha
    captcha_img = page.query_selector("img[src*='captcha']")

    # Se il captcha è presente, ottieni l'URL
    if captcha_img:
        captcha_url = captcha_img.get_attribute("src")
        # Ottieni il percorso assoluto del file del tuo script Python
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print("script dir ", script_dir)
        # Costruisci il percorso relativo al file "model.pth"
        model_path = os.path.join(script_dir, "model15.pth")
        print("model path ", model_path)
        # Utilizza il percorso relativo nella tua funzione
        solution = solve_captcha(model_path, captcha_url)
        #solution = solve_captcha("/Users/gionata/Desktop/gpt4a/model.pth", image_path)
        print("solutin", solution)
        captcha_input_selector = '#captchacharacters'
        page.fill(captcha_input_selector, solution)
        # Simula la pressione del tasto "Enter"
        page.press(captcha_input_selector, 'Enter')

     # Attendi che il pulsante di accettazione dei cookie sia visibile e cliccabile
    try:
        cookie_accept_button = page.wait_for_selector("#sp-cc-accept", timeout=10000)  # Timeout in millisecondi

        # Se il pulsante esiste e è visibile, cliccalo
        if cookie_accept_button and cookie_accept_button.is_visible():
            cookie_accept_button.click()
    except Exception as e:
        print(f"Errore durante la gestione dei cookie: {e}")

    all_results = []

    # Ciclo per le pagine delle recensioni
    for page_num in range(start_page, end_page + 1):
        page.goto(f"{url}&pageNumber={page_num}")
        page.wait_for_load_state("load")

        reviews = page.query_selector_all(".a-section.review.aok-relative")

        for single_review in reviews:
            review_text_element = single_review.query_selector("span[data-hook='review-body']")
            review_date_element = single_review.query_selector(".review-date")
            review_title_element = single_review.query_selector(".review-title")
            review_stars_element = single_review.query_selector(".a-icon-alt")
            review_flavor_element = single_review.query_selector(".a-color-secondary")

            review_text = clean_text(review_text_element.text_content()) if review_text_element else "Testo non disponibile"
            review_date = clean_text(review_date_element.text_content()) if review_date_element else "Data non disponibile"
            review_title = clean_text(review_title_element.text_content()) if review_title_element else "Titolo non disponibile"
            review_stars = clean_text(review_stars_element.text_content()) if review_stars_element else "Stelle non disponibili"
            review_flavor = clean_text(review_flavor_element.text_content()) if review_flavor_element else "Sapore non disponibile"

            data = {
                "review_text": review_text,
                "review_date": review_date,
                "review_title": review_title,
                "review_stars": review_stars,
                "review_flavor": review_flavor,
            }
            all_results.append(data)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, f"{nome}.csv")
    with open(save_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["review_text", "review_date", "review_title", "review_stars", "review_flavor"])
        writer.writeheader()
        writer.writerows(all_results)

    browser.close()

"""with sync_playwright() as playwright:
    run(playwright, "Your Amazon URL here", 1, 5, "Your Save Directory", "Your Filename")"""

def modify_url(url: str) -> str:
    base_url, parameters = url.split("/ref=")
    parameters = parameters.replace("cm_cr_dp_d_show_all_btm?", "cm_cr_arp_d_paging_btm_next_{}?")
    return "/ref=".join([base_url, parameters]) + "&pageNumber={}"