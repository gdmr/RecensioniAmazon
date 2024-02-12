import csv

# Inizializza una variabile per la somma dei punteggi
somma_punteggi = 0

# Conta il numero totale di recensioni
numero_recensioni = 0

# Leggi il file CSV
with open('tuo_file.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    # Itera attraverso le righe del file CSV
    for row in reader:
        # Estrai il punteggio dalla colonna 'review_stars' e convertilo in un float
        punteggio = float(row['review_stars'].split()[0].replace(',', '.'))
        
        # Aggiungi il punteggio alla somma
        somma_punteggi += punteggio
        
        # Incrementa il numero di recensioni
        numero_recensioni += 1


