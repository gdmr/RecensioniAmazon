# Progetto Recensioni Amazon

Questo è un progetto universitario progettato per sperimentare l'uso dell'intelligenza artificiale all'interno di una piattaforma web.

<img width="1030" alt="Schermata articoli" src="https://github.com/gdmr/RecensioniAmazon/assets/94682493/2edeeaa9-ad62-45cd-a1b2-ec9cc4af871d">



# Descrizione

Il progetto si basa sull'idea di creare una piattaforma di recensioni web verificate e offire altri servizi quali raccogliere recensioni di prodotti(scraping delle recensioni) e utilizzare più modelli di intelligenza artificiale per estrarre informazioni. Tra le funzionalità principali ci sono:

Analisi del sentiment delle recensioni lasciate sul portale, richiede token d'utilizzo richiedibile sulla piattaforma hugging face link: https://huggingface.co/settings/tokens . Da inserire nel file --> fakereviewai.py
![token hugging face](https://github.com/gdmr/RecensioniAmazon/assets/94682493/a29fab0d-6c63-42b5-aa40-bfd588db9cfe)


Classificazione delle recensioni di amazon
Chatbot con tutte le recensioni (Questa funzione richiede **l'APIKEY di OPENAI** richiedibile qui: **https://openai.com/blog/openai-api**) Da inserire nel file --> constants.py

Risolutore di captcha

Per installare le dipendenze necessarie per eseguire questo progetto, è possibile utilizzare il seguente comando pip:

pip install -r install.txt

Assicurati di eseguire questo comando nella directory del progetto, dove si trova il file install.txt.

# Utilizzo

Una volta installate tutte le dipendenze, è possibile eseguire il progetto digitano python app.py


Licenza

Questo progetto è rilasciato sotto la licenza GNU General Public License v3.0, il che significa che è possibile utilizzarlo, modificarlo e distribuirlo liberamente, purché venga mantenuta l'attribuzione appropriata e la licenza originale.

