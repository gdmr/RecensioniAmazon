DROP TABLE IF EXISTS utenti;

CREATE TABLE utenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    pass TEXT NOT NULL
);

INSERT INTO utenti(email, pass) VALUES(
    'franco@libero.it',
    'pass'
);
