import sqlite3
from flask import flash


class User:
    def __init__(self, email, password, nome, admin=0):
        self.email = email
        self.password = password
        self.nome = nome
        self.admin = admin

    @staticmethod
    def create_table(db):
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS utenti (
                email TEXT PRIMARY KEY,
                pass TEXT NOT NULL,
                nome TEXT NOT NULL,
                admin INTEGER NOT NULL
            )
        ''')
        db.commit()

    def save(self, db):
        cursor = db.cursor()
        try:
            # Verifica se l'indirizzo email esiste già nel database
            cursor.execute("SELECT email FROM utenti WHERE email = ?", (self.email,))
            existing_email = cursor.fetchone()

            if existing_email:
                flash('Questo indirizzo email è già stato registrato.')
                return

            # Se l'indirizzo email non esiste, procedi con l'inserimento
            cursor.execute('''
                INSERT INTO utenti (email, pass, nome, admin)
                VALUES (?, ?, ?, ?)
            ''', (self.email, self.password, self.nome, self.admin))
            db.commit()
            flash('Registrazione effettuata con successo. Adesso puoi fare il login.')
        except sqlite3.IntegrityError as e:
            db.rollback()
            flash('Errore durante la registrazione.')
        finally:
            cursor.close()

        
class Review:
    def __init__(self, id, nome, titolo, info, email_utente, link, articolo_id, valutazione):
        self.id = id
        self.nome = nome
        self.titolo = titolo
        self.info = info
        self.email_utente = email_utente
        self.link = link
        self.artID = articolo_id
        self.valutazione = valutazione

    @staticmethod
    def create_table(db):
        # Creazione della tabella recensioni
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recensioni (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                titolo TEXT,
                info TEXT,
                email_utente TEXT,
                link TEXT,
                articolo_id INT,
                valutazione TEXT,
                FOREIGN KEY (articolo_id) REFERENCES Articolo(id),
                FOREIGN KEY (email_utente) REFERENCES utenti(email)
            )
        ''')
        db.commit()

    def save(self, db):
        # Inserimento dei dati della recensione nella tabella
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO recensioni (nome, titolo, info, email_utente, link, articolo_id, valutazione)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.nome, self.titolo, self.info, self.email_utente, self.link, self.artID, self.valutazione))
        db.commit()
        cursor.close()


    @staticmethod
    def get_all_reviews(db):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM recensioni")
            reviews_data = cursor.fetchall()

            reviews = []
            for review_data in reviews_data:
                review = Review(*review_data[0:8])
                reviews.append(review)

            return reviews
        finally:
            cursor.close()

    @staticmethod
    def get_reviews_by_email(db, email):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM recensioni WHERE email_utente = ?", (email,))
            reviews_data = cursor.fetchall()

            reviews = []
            for review_data in reviews_data:
                review = Review(*review_data[0:8])
                reviews.append(review)

            return reviews
        finally:
            cursor.close()

    @staticmethod
    def delete_review(db, review_id):
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM recensioni WHERE id = ?", (review_id,))
            db.commit()
        except sqlite3.Error as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
    
    @staticmethod
    def get_reviews_by_articolo_id(db, articolo_id):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM recensioni WHERE articolo_id = ?", (articolo_id,))
            reviews_data = cursor.fetchall()

            reviews = []
            for review_data in reviews_data:
                review = Review(*review_data)
                reviews.append(review)

            return reviews
        finally:
            cursor.close()
            
    #Ottenere il link della recensione
    @staticmethod
    def get_first_review_link_by_articolo_id(db, articolo_id):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM recensioni WHERE articolo_id = ? LIMIT 1", (articolo_id,))
            review_data = cursor.fetchone()

            if review_data is not None:
                review = Review(*review_data)
                return review.link
            else:
                return None
        finally:
            cursor.close()

    @staticmethod
    def count_reviews_by_email(db, email):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(id) FROM recensioni WHERE email_utente = ?", (email,))
            count = cursor.fetchone()[0]
            return count
        finally:
            cursor.close()

    @staticmethod
    def get_reviews_by_email_paged(db, email, page, limit):
        offset = (page - 1) * limit
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM recensioni WHERE email_utente = ? ORDER BY id DESC LIMIT ? OFFSET ?", (email, limit, offset))
            reviews_data = cursor.fetchall()

            reviews = []
            for review_data in reviews_data:
                review = Review(*review_data[0:8])
                reviews.append(review)

            return reviews
        finally:
            cursor.close()

            

class Articolo:
    def __init__(self, id, nomeart, data, url_img, categoria=None):
        self.id = id
        self.nomeart = nomeart
        self.data = data
        self.url_img = url_img
        self.categoria = categoria

    @staticmethod
    def create_table(db):
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articoli (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nomeart TEXT,
                data TEXT,
                url_img TEXT,
                categoria TEXT
            )
        ''')
        db.commit()

    def save(self, db):
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO articoli (id, nomeart, data, url_img, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.id, self.nomeart, self.data, self.url_img, self.categoria)) 
        db.commit()


    @staticmethod
    def get_all_article(db):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM articoli")
            articoli_data = cursor.fetchall()

            articoli = []
            for articolo_data in articoli_data:
                articolo = Articolo(*articolo_data[0:4])
                articoli.append(articolo)

            return articoli
        finally:
            cursor.close()

    @staticmethod
    def get_id_article(db, articolo_id):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM articoli WHERE id = ?", (articolo_id,))
            articoli_data = cursor.fetchall()

            articoli = []
            for articolo_data in articoli_data:
                articolo = Articolo(*articolo_data[0:4])
                articoli.append(articolo)

            return articoli
        finally:
            cursor.close()

    @staticmethod
    def ottieni_id(db, url):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT id FROM articoli WHERE nomeart = ?", (url,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        finally:
            cursor.close()
    
    @staticmethod
    def search_by_name(db, query):
        cursor = db.cursor()
        try:
            # Utilizzo del segnaposto "%" per permettere una ricerca "LIKE"
            cursor.execute("SELECT * FROM articoli WHERE nomeart LIKE ?", ('%' + query + '%',))
            articoli_data = cursor.fetchall()

            articoli = []
            for articolo_data in articoli_data:
                articolo = Articolo(*articolo_data[0:4])
                articoli.append(articolo)

            return articoli
        finally:
            cursor.close()

    @staticmethod
    def get_article_count(db):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM articoli")
            count = cursor.fetchone()[0]
            return count
        finally:
            cursor.close()
    
    @staticmethod
    def get_paginated_articles(db, page, per_page):
        cursor = db.cursor()
        try:
            # Calcola l'offset per la query SQL
            offset = (page - 1) * per_page

            # Esegue la query per ottenere gli articoli per la pagina specifica
            cursor.execute("SELECT * FROM articoli LIMIT ? OFFSET ?", (per_page, offset))
            articoli_data = cursor.fetchall()

            articoli = []
            for articolo_data in articoli_data:
                articolo = Articolo(*articolo_data[0:4])
                articoli.append(articolo)

            return articoli
        finally:
            cursor.close()



class Dettaglio:
    def __init__(self, affidabilita, id, tipologia, mediaamaz):
        self.affidabilita = affidabilita
        self.articolo_id = id
        self.tipologia = tipologia
        self.mediaamaz = mediaamaz

    @staticmethod
    def create_table(db):
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dettagli (
                tipologia TEXT,
                affidabilita INTEGER,
                id INTEGER,
                mediaamaz INTEGER,
                FOREIGN KEY (id) REFERENCES articoli(id)
            )
        ''')
        db.commit()

    def save(self, db):
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO dettagli (tipologia, affidabilita, id, mediaamaz)
            VALUES (?, ?, ?, ?)
        ''', (self.tipologia, self.affidabilita, self.articolo_id, self.mediaamaz))
        db.commit()
        cursor.close()

    @staticmethod
    def get_affidabilita_by_article_id(db, article_id):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT affidabilita FROM dettagli WHERE id = ?", (article_id,))
            result = cursor.fetchone()

            return result[0] if result else None
        finally:
            cursor.close()

    @staticmethod
    def get_articolo_by_id(db, article_id):
        cursor = db.cursor()
        try:
            cursor.execute("SELECT affidabilita, mediaamaz FROM dettagli WHERE id = ?", (article_id,))
            result = cursor.fetchone()

            # Restituisce l'intera riga come tuple, o None se non viene trovato nessun risultato
            return result if result else None
        finally:
            cursor.close()

    @staticmethod
    def delete_details_by_article_id(db, article_id):
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM dettagli WHERE id = ?", (article_id,))
            db.commit()
        except sqlite3.Error as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
