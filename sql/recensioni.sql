DROP TABLE IF EXISTS recensioni;

CREATE TABLE recensioni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titolo TEXT,
    info TEXT
);

INSERT INTO recensioni(titolo, info) VALUES(
    'Grande prodotto',
    'Mi sono trovato molto bene, ottimo package'
);
