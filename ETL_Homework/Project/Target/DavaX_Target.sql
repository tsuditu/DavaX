CREATE TABLE TGT_DEPARTAMENT (
    id_departament    NUMBER PRIMARY KEY CHECK (MOD(id_departament, 10) = 0), -- doar coduri multiple de 10
    nume              VARCHAR2(100) NOT NULL,
    cod_unic          VARCHAR2(10) NOT NULL UNIQUE
);

CREATE TABLE TGT_ANGAJAT (
    id_angajat        NUMBER PRIMARY KEY,
    nume              VARCHAR2(100) NOT NULL,
    email             VARCHAR2(100) NOT NULL UNIQUE,
    salariu           NUMBER(8,2),
    gen               VARCHAR2(10) NOT NULL,
    functie           VARCHAR2(50) NOT NULL,
    data_angajare     DATE,
    status            VARCHAR2(10) NOT NULL,
    id_departament    NUMBER,
    CONSTRAINT fk_angajat_departament FOREIGN KEY (id_departament)
        REFERENCES TGT_DEPARTAMENT(id_departament),
    loading_timestamp  TIMESTAMP,                  -- cand s-a importat inregistrarea
    dataset_nume       VARCHAR2(50)                -- eticheta pentru batch-ul de import
);


CREATE TABLE TGT_PONTAJ (
    id_pontaj         NUMBER PRIMARY KEY,
    id_angajat        NUMBER,
    data_pontaj       DATE NOT NULL,
    activitate        VARCHAR2(100) NOT NULL,
    ore_lucrate       NUMBER(4,2) NOT NULL CHECK (ore_lucrate BETWEEN 0 AND 24),
    CONSTRAINT fk_pontaj_angajat FOREIGN KEY (id_angajat)
        REFERENCES TGT_ANGAJAT(id_angajat),
    loading_timestamp  TIMESTAMP,                  -- cand s-a importat inregistrarea
    dataset_nume       VARCHAR2(50)                -- eticheta pentru batch-ul de import
);

-- Corectie: modifica coloana ore_lucrate sa accepte format ora:minut:sec
ALTER TABLE TGT_PONTAJ DROP CONSTRAINT SYS_C008291;
ALTER TABLE TGT_PONTAJ MODIFY ORE_LUCRATE VARCHAR2(20);

CREATE TABLE TGT_ATTENDANCE (
    id_attendance         NUMBER PRIMARY KEY,
    id_angajat            NUMBER,
    data_sesiune          DATE NOT NULL,
    ora_intrare           VARCHAR2(30),
    ora_iesire            VARCHAR2(30),
    durata_sesiune        NUMBER(6,2) NOT NULL,
    durata_participare    NUMBER(6,2) NOT NULL,
    titlu_meeting         VARCHAR2(100),
    loading_timestamp  TIMESTAMP,                  -- cand s-a importat inregistrarea
    dataset_nume       VARCHAR2(50)                -- eticheta pentru batch-ul de import
);

-- Convertire durate in text pt compatibilitate
ALTER TABLE TGT_ATTENDANCE MODIFY DURATA_SESIUNE VARCHAR2(20);
ALTER TABLE TGT_ATTENDANCE MODIFY DURATA_PARTICIPARE VARCHAR2(20);

-- Adauga constraint pe FK
ALTER TABLE TGT_ATTENDANCE
ADD CONSTRAINT fk_att_angajat
FOREIGN KEY (id_angajat)
REFERENCES TGT_ANGAJAT(id_angajat);


CREATE TABLE TGT_ABSENCES (
    id_absenta       NUMBER PRIMARY KEY,
    id_angajat       NUMBER,
    data_start       DATE NOT NULL,
    data_sfarsit     DATE NOT NULL,
    zile             NUMBER(3),
    motiv            VARCHAR2(50) NOT NULL,
    CONSTRAINT fk_abs_angajat FOREIGN KEY (id_angajat)
        REFERENCES TGT_ANGAJAT(id_angajat),
    CONSTRAINT chk_interval_valid CHECK (data_sfarsit >= data_start),
    loading_timestamp  TIMESTAMP,                  -- cand s-a importat inregistrarea
    dataset_nume       VARCHAR2(50)                -- eticheta pentru batch-ul de import
);


CREATE TABLE TGT_EXAM_ABSENCES (
    id_exam_absenta  NUMBER PRIMARY KEY,
    id_angajat       NUMBER,
    data_absenta     DATE NOT NULL,
    ore_absenta      NUMBER(4,2) NOT NULL CHECK (ore_absenta BETWEEN 1 AND 8),
    CONSTRAINT fk_exam_angajat FOREIGN KEY (id_angajat)
        REFERENCES TGT_ANGAJAT(id_angajat),
    loading_timestamp  TIMESTAMP,                  -- cand s-a importat inregistrarea
    dataset_nume       VARCHAR2(50)                -- eticheta pentru batch-ul de import
);

-- Adauga coloane metadata lipsa pentru departamente
ALTER TABLE TGT_DEPARTAMENT
ADD (
    loading_timestamp TIMESTAMP,
    dataset_nume      VARCHAR2(50)
);

-- Idem pentru restul tabelelor
ALTER TABLE TGT_ANGAJAT
ADD (
    loading_timestamp TIMESTAMP,
    dataset_nume      VARCHAR2(50)
);

ALTER TABLE TGT_PONTAJ
ADD (
    loading_timestamp TIMESTAMP,
    dataset_nume      VARCHAR2(50)
);

ALTER TABLE TGT_ATTENDANCE
ADD (
    loading_timestamp TIMESTAMP,
    dataset_nume      VARCHAR2(50)
);

ALTER TABLE TGT_ABSENCES
ADD (
    loading_timestamp TIMESTAMP,
    dataset_nume      VARCHAR2(50)
);

ALTER TABLE TGT_EXAM_ABSENCES
ADD (
    loading_timestamp TIMESTAMP,
    dataset_nume      VARCHAR2(50)
);


CREATE OR REPLACE TRIGGER trg_set_metadata_src_departament
BEFORE INSERT ON TGT_DEPARTAMENT
FOR EACH ROW
BEGIN
  :NEW.loading_timestamp := SYSTIMESTAMP;
  :NEW.dataset_nume := 'src_departamente_' || TO_CHAR(SYSTIMESTAMP, 'DD-MM-YY');
END;
/

CREATE OR REPLACE TRIGGER trg_set_metadata_src_angajat
BEFORE INSERT ON TGT_ANGAJAT
FOR EACH ROW
BEGIN
  :NEW.loading_timestamp := SYSTIMESTAMP;
  :NEW.dataset_nume := 'src_angajati_' || TO_CHAR(SYSTIMESTAMP, 'DD-MM-YY');
END;
/

CREATE OR REPLACE TRIGGER trg_set_metadata_src_pontaj
BEFORE INSERT ON TGT_PONTAJ
FOR EACH ROW
BEGIN
  :NEW.loading_timestamp := SYSTIMESTAMP;
  :NEW.dataset_nume := 'src_pontaj_' || TO_CHAR(SYSTIMESTAMP, 'DD-MM-YY');
END;
/

CREATE OR REPLACE TRIGGER trg_set_metadata_src_absences
BEFORE INSERT ON TGT_ABSENCES
FOR EACH ROW
BEGIN
  :NEW.loading_timestamp := SYSTIMESTAMP;
  :NEW.dataset_nume := 'src_absente_' || TO_CHAR(SYSTIMESTAMP, 'DD-MM-YY');
END;
/

CREATE OR REPLACE TRIGGER trg_set_metadata_src_attendance
BEFORE INSERT ON TGT_ATTENDANCE
FOR EACH ROW
BEGIN
  :NEW.loading_timestamp := SYSTIMESTAMP;
  :NEW.dataset_nume := 'src_attendance_' || TO_CHAR(SYSTIMESTAMP, 'DD-MM-YY');
END;
/

CREATE OR REPLACE TRIGGER trg_set_metadata_src_exam_absences
BEFORE INSERT ON TGT_EXAM_ABSENCES
FOR EACH ROW
BEGIN
  :NEW.loading_timestamp := SYSTIMESTAMP;
  :NEW.dataset_nume := 'src_exam_absences_' || TO_CHAR(SYSTIMESTAMP, 'DD-MM-YY');
END;
/

COMMIT;