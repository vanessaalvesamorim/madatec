DROP TABLE IF EXISTS aluno;

CREATE TABLE aluno (
    ra INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_aluno TEXT NOT NULL,
    nascimento INTEGER NOT NULL,
    num_ser TEXT,
    turma TEXT,
    sexo TEXT,
    situacao TEXT,
    nome_mae TEXT,
    profissao_mae TEXT,
    localtrab_mae TEXT,
    nasc_mae INTEGER DEFAULT 0,
    fone_mae INTEGER DEFAULT 0,
    nome_pai TEXT,
    profissao_pai TEXT,
    localtrab_pai TEXT,
    nasc_pai INTEGER DEFAULT 0,
    fone_pai INTEGER DEFAULT 0,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);