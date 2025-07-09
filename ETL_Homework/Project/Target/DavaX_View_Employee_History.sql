CREATE OR REPLACE VIEW VW_EMPLOYEE_HISTORY AS

-- Pontaj zilnic
SELECT 
  a.nume,
  p.data_pontaj AS data_eveniment,            -- ziua pontajului
  'PONTAJ' AS tip_eveniment,                  -- tip de eveniment
  TO_CHAR(p.activitate) AS detalii,          -- activitatea desfasurata
  TO_CHAR(p.ore_lucrate) AS valoare          -- nr de ore lucrate (format text)
FROM TGT_ANGAJAT a
JOIN TGT_PONTAJ p ON a.id_angajat = p.id_angajat

UNION ALL

-- Absente complete
SELECT 
  a.nume,
  ab.data_start AS data_eveniment,           -- prima zi de absenta
  'ABSENTA' AS tip_eveniment,
  TO_CHAR(ab.motiv) AS detalii,              -- tipul absentei (medical, concediu etc.)
  TO_CHAR(ab.zile * 8) AS valoare            -- transformare zile -> ore
FROM TGT_ANGAJAT a
JOIN TGT_ABSENCES ab ON a.id_angajat = ab.id_angajat

UNION ALL

-- Examene programate
SELECT 
  a.nume,
  ex.data_absenta AS data_eveniment,
  'EXAMEN' AS tip_eveniment,
  'Examen oficial' AS detalii,               -- descriere statica
  TO_CHAR(ex.ore_absenta) AS valoare         -- durata absentei
FROM TGT_ANGAJAT a
JOIN TGT_EXAM_ABSENCES ex ON a.id_angajat = ex.id_angajat

UNION ALL

-- Prezenta la sesiuni/cursuri
SELECT 
  a.nume,
  at.data_sesiune AS data_eveniment,
  'PREZENTA' AS tip_eveniment,
  TO_CHAR(at.titlu_meeting) AS detalii,      -- titlul cursului
  TO_CHAR(at.durata_participare) AS valoare  -- durata participarii efective
FROM TGT_ANGAJAT a
JOIN TGT_ATTENDANCE at ON a.id_angajat = at.id_angajat;




-- Istoricul complet al unui angajat
SELECT *
FROM VW_EMPLOYEE_HISTORY
WHERE INITCAP(nume) = 'Tiberiu Gabriel Suditu'
ORDER BY data_eveniment;

-- Doar zilele de absenta
SELECT *
FROM VW_EMPLOYEE_HISTORY
WHERE INITCAP(nume) = 'Tiberiu Gabriel Suditu'
  AND tip_eveniment = 'ABSENTA'
ORDER BY data_eveniment;

-- Total ore lucrate
SELECT 
  nume,
  SUM(TO_NUMBER(TRIM(valoare))) AS total_ore_lucrate
FROM VW_EMPLOYEE_HISTORY
WHERE tip_eveniment = 'PONTAJ'
  AND REGEXP_LIKE(TRIM(valoare), '^\d+(\.\d+)?$')  -- versiune robusta -- filtreaza doar valorile numerice
GROUP BY nume;

-- Conversie din format ora:minut:sec
SELECT 
  nume,
  SUM(
    EXTRACT(HOUR FROM TO_DSINTERVAL('0 ' || valoare)) * 60 +
    EXTRACT(MINUTE FROM TO_DSINTERVAL('0 ' || valoare)) +
    EXTRACT(SECOND FROM TO_DSINTERVAL('0 ' || valoare)) / 60
  ) AS total_ore_lucrate
FROM VW_EMPLOYEE_HISTORY
WHERE tip_eveniment = 'PONTAJ'
GROUP BY nume;







