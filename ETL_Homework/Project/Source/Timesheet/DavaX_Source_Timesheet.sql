CREATE TABLE SRC_ANGAJAT (
    id_angajat        NUMBER PRIMARY KEY,
    nume              VARCHAR2(100),
    email             VARCHAR2(100),
    salariu           NUMBER(8,2),
    gen               VARCHAR2(15),
    id_departament    NUMBER,
    functie           VARCHAR2(50),
    data_angajare     DATE,
    status            VARCHAR2(10),
    loading_timestamp TIMESTAMP,                       -- metadata: cand s-a importat
    dataset_nume      VARCHAR2(50)                     -- metadata: ce fisier a fost importat
);

-- Trigger pentru completarea automata a metadatelor la INSERT
CREATE OR REPLACE TRIGGER trg_set_metadata_angajat
BEFORE INSERT ON SRC_ANGAJAT
FOR EACH ROW
BEGIN
  :NEW.loading_timestamp := SYSTIMESTAMP;
  :NEW.dataset_nume := 'angajati_' || TO_CHAR(SYSTIMESTAMP, 'DD-MM-YY');
END;
/


CREATE TABLE SRC_DEPARTAMENT (
    id_departament NUMBER PRIMARY KEY
        CHECK (MOD(id_departament, 10) = 0), 
    nume VARCHAR2(100),                  
    cod_unic VARCHAR2(10) UNIQUE,
    loading_timestamp TIMESTAMP,                       -- metadata: cand s-a importat
    dataset_nume      VARCHAR2(50)                     -- metadata: ce fisier a fost importat
);

-- Trigger pentru completarea automata a metadatelor la INSERT
CREATE OR REPLACE TRIGGER trg_set_metadata_departament
BEFORE INSERT ON SRC_DEPARTAMENT
FOR EACH ROW
BEGIN
  :NEW.loading_timestamp := SYSTIMESTAMP;
  :NEW.dataset_nume := 'departamente_' || TO_CHAR(SYSTIMESTAMP, 'DD-MM-YY');
END;
/


CREATE TABLE SRC_PONTAJ (
    id_pontaj NUMBER PRIMARY KEY,
    id_angajat NUMBER,
    data_pontaj DATE,
    ore_lucrate NUMBER(4,2) CHECK (ore_lucrate BETWEEN 0 AND 24), -- nr. de ore lucrate (max 24)
    activitate VARCHAR2(100),
    loading_timestamp TIMESTAMP,                                  -- metadata: cand s-a importat
    dataset_nume      VARCHAR2(50)                                -- metadata: ce fisier a fost importat
);

-- Trigger pentru completarea automata a metadatelor la INSERT
CREATE OR REPLACE TRIGGER trg_set_metadata_pontaj
BEFORE INSERT ON SRC_PONTAJ
FOR EACH ROW
BEGIN
  :NEW.loading_timestamp := SYSTIMESTAMP;
  :NEW.dataset_nume := 'pontaj_' || TO_CHAR(SYSTIMESTAMP, 'DD-MM-YY');
END;
/


-- ==============================
-- CONSTRANGERI FK
-- ==============================

-- Legatura dintre SRC_PONTAJ si SRC_ANGAJAT
ALTER TABLE SRC_PONTAJ
ADD CONSTRAINT fk_pontaj_angajat
FOREIGN KEY (id_angajat)
REFERENCES SRC_ANGAJAT(id_angajat);

-- Legatura dintre SRC_ANGAJAT si SRC_DEPARTAMENT
ALTER TABLE SRC_ANGAJAT
ADD CONSTRAINT fk_angajat_departament
FOREIGN KEY (id_departament)
REFERENCES SRC_DEPARTAMENT(id_departament);

-- COMMIT pentru salvare permanenta
COMMIT;


