ALTER TABLE recensioni ADD COLUMN id_utente INTEGER;

-- Aggiungi il vincolo di chiave esterna per legare la tabella utenti con la tabella recensioni
ALTER TABLE recensioni ADD CONSTRAINT fk_utenti_recensioni FOREIGN KEY (id_utente) REFERENCES utenti(id);