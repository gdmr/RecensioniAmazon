import os

def trova_file(nome, cartella='.'):
    """
    Trova il file specificato nella cartella data e nelle sue sottodirectory.
    
    :param nome: Il nome del file da cercare.
    :param cartella: La cartella in cui cercare. Default è la cartella corrente.
    :return: Il percorso relativo del file trovato o None se non viene trovato.
    """
    for root, dirs, files in os.walk(cartella):
        for file in files:
            if file == nome:
                return os.path.relpath(os.path.join(root, file))
    return None
