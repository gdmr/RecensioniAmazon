from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from flask import flash, get_flashed_messages
from flask import g, abort
import random
import json
import sqlite3
import math
import os
from MODEL.models import User, Review, Articolo, Dettaglio
from utils.scraper import run, modify_url
from utils.chatgptbk import chat_model
from utils.scraperdetail import scrape_product_details
from utils.fakereviewai import calcola_percentuale_veri
from werkzeug.utils import secure_filename
from datetime import datetime
from multiprocessing import Process
from utils.media import calcola_media_stelle
from utils.valutazione import get_valutazione
from playwright.sync_api import sync_playwright
from utils.sentimentrecensioni import analyze_review




ITEMS_PER_PAGE = 3
controller = Blueprint("controller", __name__)

@controller.route("/")
def home():
    return render_template("index.html", session=session)

@controller.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor = g.db.cursor()

    try:
        cursor.execute("SELECT * FROM utenti WHERE email = ? AND pass = ?", (email, password))
        user = cursor.fetchone()

        if user is None:
            flash('Email o password errata.')
            return redirect(url_for('controller.loginpage'))

        session['logged_in'] = True
        session['email'] = user[0]
        session['nome'] = user[2]

        
        if user[3] == 1:
            session['is_admin'] = True
            flash('Login amministratore effettuato con successo.')
            return redirect(url_for('controller.admin_page'))

        session['is_admin'] = False
        flash('Login effettuato con successo.')
    finally:
        cursor.close()

    return redirect(url_for('controller.home'))

@controller.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('nome', None)

    flash('Logout effettuato con successo.')
    return redirect(url_for('controller.home'))


@controller.route("/loginpage")
def loginpage():
    return render_template("loginpage.html")


@controller.route("/contattaci")
def contattaci():
    return render_template("contattaci.html")


@controller.route("/invia-messaggio", methods=["POST"])
def invia_messaggio():
    nome = request.form.get("name")
    email = request.form.get("email")
    messaggio = request.form.get("message")
    # eventuali operazioni
    flash("Messaggio inviato con successo!", "success")
    return redirect(url_for("controller.home"))

@controller.route("/registrati")
def registrati():
    return render_template("registrati.html")

@controller.route('/register', methods=['POST'])
def register():
    nome = request.form.get('nome')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirm = request.form.get('passwordConfirm')
    captcha_response = request.form.get('captcha_response')
    captcha_image_path = request.form.get('captcha_image_path')

    # Verfica CAPTCHA
    if captcha_image_path:
        captcha_image_path = captcha_image_path.split('/static/')[-1]
        captcha_image_path = 'static/' + captcha_image_path

        if captcha_data.get(captcha_image_path) != captcha_response:
            flash('CAPTCHA errato.')
            return redirect(url_for('controller.registrati'))

    if password != password_confirm:
        flash('Le password non corrispondono.')
        return redirect(url_for('controller.registrati'))

    user = User(email, password, nome)
    user.create_table(g.db)
    user.save(g.db)

    return redirect(url_for('controller.home'))


@controller.route("/articoli")
def articoli():
    articoli = Articolo.get_all_article(g.db)
    return render_template("articoli.html", articoli=articoli)

@controller.route("/articolicerca", methods=['GET'])
def articolicerca():
    query = request.args.get('q')
    if not query:
        articoli = Articolo.get_all_article(g.db)
    else:
        articoli = Articolo.search_by_name(g.db, query)
    return render_template("articoli.html", articoli=articoli)

@controller.route("/cercarandom", methods=['GET'])
def articolicercarandom():
    articoli = Articolo.get_all_article(g.db)
    if not articoli:
        return "Nessun articolo nel database."
    indice_randomico = random.randint(0, len(articoli) - 1)
    articolo_randomico = articoli[indice_randomico]
    return render_template("articoli.html", articoli=[articolo_randomico])

@controller.route("/vedisuamazon", methods=['GET'])
def vedisuamazon():
    articolo_id = request.args.get('articolo_id') 
    link = Review.get_first_review_link_by_articolo_id(g.db, articolo_id)
    return redirect(link)

@controller.route("/dettagli", methods=['GET'])
def dettagli():
    id = request.args.get('id')
    articoli = Articolo.get_id_article(g.db, id)
    articolo = articoli[0]
    dt = articolo.data
    basepath = os.path.dirname(os.path.realpath(__file__))
    relative_path = os.path.join(basepath, "..", "data", f"{dt}.csv")
    path = os.path.abspath(relative_path)
    media = calcola_media_stelle(path)
    recensioni_mioportale = Review.get_reviews_by_articolo_id(g.db, id)
    somma_valutazioni = 0
    numero_recensioni = len(recensioni_mioportale)
    for recensione in recensioni_mioportale:
        somma_valutazioni += recensione.valutazione
    media_valutazioni = somma_valutazioni / numero_recensioni if numero_recensioni > 0 else 0
    basepath = os.path.dirname(os.path.realpath(__file__))
    save_dir = os.path.join(basepath, "prova")
    recensione = recensioni_mioportale[0]
    dettagli = Dettaglio.get_articolo_by_id(g.db, id)
    val = dettagli[0]
    mediaamazon = dettagli[1]
    soddisfazione = 90
    extra = None
    dati = [
        {'mediasito': media, 'mediaamazon': mediaamazon},
        {'mioportale': media_valutazioni, 'fake': val},
        {'data':relative_path},
        {'extra':extra}
    ]
    return render_template("dettagliate.html", dati=dati, soddisfazione=soddisfazione)


@controller.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    print("data", data)
    question = data.get("message", "")
    print("question", question)
    aggiunta = data.get("doc", "")
    print("aggiunta", aggiunta)
    trovaqui = aggiunta
    print("TROVA QUII------->>>>>>>>>>")
    print(trovaqui)
    if question:
        response = chat_model(trovaqui,question)
        return jsonify({"generated_text": response})

    return jsonify({"generated_text": "No question provided."})

@controller.route("/recensioni")
def recensioni():
    reviews = Review.get_all_reviews(g.db)
    return render_template("recensioni.html", recensioni=reviews)

@controller.route("/recensionearticolo", methods=["GET"])
def recensionearticolo():
    articolo_id = request.args.get('articolo_id')
    reviews = Review.get_reviews_by_articolo_id(g.db, articolo_id)
    return render_template("recensioni.html", recensioni=reviews)


@controller.route("/scrivirecensione", defaults={'page': 1})
@controller.route("/scrivirecensione/page/<int:page>")
def scrivirecensione(page):
    if not session.get('logged_in'):
        flash('Effettua il login per accedere alla pagina.')
        return redirect(url_for('controller.loginpage'))

    email_utente = session.get('email')
    total_reviews = Review.count_reviews_by_email(g.db, email_utente)
    total_pages = math.ceil(total_reviews / ITEMS_PER_PAGE)
    reviews = Review.get_reviews_by_email_paged(g.db, email_utente, page, ITEMS_PER_PAGE)

    return render_template("recensioniscrivi.html", reviews=reviews, current_page=page, total_pages=total_pages)

@controller.route('/immettirecensione', methods=['POST'])
def immettirecensione():           
    data_directory = "source_documents"
    save_dir = os.path.join(os.getcwd(), data_directory)
    if not session.get('logged_in'):
        flash('Effettua il login per accedere alla pagina.')
        return redirect(url_for('controller.loginpage'))
    email_utente = session['email']

    
    nome = request.form['nome'] 
    titolo = request.form['titolo']
    info = request.form['info']
    link = request.form['link']
    valutazione = get_valutazione(titolo)
    product_details = scrape_product_details(link)
    url = product_details["product_title"]
    url_img = product_details["product_image_url"] 
    rating = product_details["rating"]
    categoria = product_details["category"]
    articoli = Articolo.get_all_article(g.db)
    cursor = g.db.cursor()
    try:
        articolo_id = None
        for articolo in articoli:
            if articolo.nomeart == url:
                articolo_id = articolo.id
                break

        if articolo_id is None:
            data = datetime.now().strftime('%Y-%m-%d-%H-%M')
            articolo = Articolo(None, url, data, url_img, categoria)
            print("salvo articolo")
            articolo.save(g.db)
            articolo_id = Articolo.ottieni_id(g.db, url)
            save_dir = os.path.join(os.getcwd(), "data") 
            try:
                with sync_playwright() as playwright:
                    run(playwright, link, 1, 5, save_dir, data)
            except Exception as e:
                flash('Errore playwright: ' + str(e))
        review = Review(None, nome, titolo, info, email_utente, link, articolo_id, valutazione)
        review.save(g.db)
        basepath = os.path.dirname(os.path.realpath(__file__))
        dt = articolo.data
        relative_path = os.path.join(basepath, "..", "data", f"{dt}.csv")
        path = os.path.abspath(relative_path)
        val = calcola_percentuale_veri(path)
        Dettaglio.create_table(g.db)
        tipologia="prova"
        dettaglio = Dettaglio(val,articolo_id,tipologia,rating)
        dettaglio.save(g.db)
        flash('Recensione inserita con successo.')

    except sqlite3.Error as e:
        flash('Si è verificato un errore: ' + str(e))
        return redirect(url_for('controller.recensioni'))
    except Exception as e:
        flash('Errore generico: ' + str(e))
        g.db.rollback()
    finally:
        cursor.close()

    return jsonify({"redirect_url": url_for('controller.scrivirecensione')})

@controller.route("/eliminarecensione/<int:review_id>", methods=['POST'])
def eliminarecensione(review_id):
    if not session.get('logged_in'):
        flash('Effettua il login per accedere alla pagina.')
        return redirect(url_for('controller.loginpage'))
    Review.delete_review(g.db, review_id)
    flash('Recensione eliminata con successo.')

    return redirect(url_for('controller.scrivirecensione'))

captcha_data = {
    "static/captcha/face.jpeg": "ma io che cavolo ne so",
    "static/captcha/face2.jpeg": "ho visto un rumore",
    "static/captcha/face3.jpeg": "è molto bello",
    "static/captcha/face4.jpeg": "entra?",
}

# Funzione per mischiare le parole di una frase
def shuffle_sentence(sentence):
    words = sentence.split()
    random.shuffle(words)
    return words


@controller.route('/get_captcha', methods=['GET'])
def get_captcha():
    image_path, sentence = random.choice(list(captcha_data.items()))
    shuffled_sentence = shuffle_sentence(sentence)
    return jsonify({"image": image_path, "words": shuffled_sentence})

@controller.route('/verify_captcha', methods=['POST'])
def verify_captcha():
    data = request.json
    try:
        # Ottieni solo la parte del percorso dall'URL completo
        image_path = data['image'].split('/static/')[-1]
        image_path = 'static/' + image_path  # Aggiungi 'static/' all'inizio

        user_response = " ".join(data['response'])
        print("stampa")
        print("Frase attesa:", captcha_data[image_path].lower())
        print("Risposta dell'utente:", user_response.lower())

        if captcha_data[image_path] == user_response:
            return jsonify({"success": True, "message": "CAPTCHA corretto!"})
        else:
            return jsonify({"success": False, "message": "CAPTCHA errato."})
    except KeyError as e:
        return jsonify({"success": False, "message": f"Chiave mancante o errata: {e}"})
