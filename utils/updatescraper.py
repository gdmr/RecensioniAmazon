from utils.scraper import run_scraper
import logging
import os

def avvia_scraper_se_file_esiste(url: str, start_page: int, end_page: int, save_dir: str, nome_base: str):
    nome_file = f"{nome_base}.csv"
    file_precedente = cerca_file_esistente(save_dir, nome_file)

    if file_precedente:
        logging.info(f"Il file {nome_file} esiste già nel percorso {file_precedente}")
        run_scraper(url, start_page, end_page, save_dir, nome_base)
    else:
        logging.info(f"Il file {nome_file} non esiste. Scraper non avviato.")

def cerca_file_esistente(cartella, nome_file):
    for root, dirs, files in os.walk(cartella):
        if nome_file in files:
            return os.path.join(root, nome_file)
    return None
