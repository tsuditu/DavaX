CREATE OR REPLACE VIEW VW_EMPLOYEE_UPDATE AS
SELECT 
  a.id_angajat,                              -- identificatorul unic al angajatului
  a.nume AS nume_complet,                    -- numele complet
  a.email AS email,                          -- emailul
  a.gen,                                     -- genul: Masculin / Feminin / Altul
  a.functie AS functie,                      -- pozitia curenta
  a.salariu,                                 -- salariul actual
  a.status,                                  -- activ / inactiv
  d.nume AS departament,                     -- denumirea departamentului (din FK)
  a.data_angajare AS data_angajare           -- cand a fost angajat
FROM TGT_ANGAJAT a
LEFT JOIN TGT_DEPARTAMENT d ON a.id_departament = d.id_departament;


-- Lista angajatilor activi
SELECT id_angajat, nume_complet, functie, email
FROM VW_EMPLOYEE_UPDATE
WHERE status = 'ACTIV';

-- Angajati din departamentul Finante
SELECT nume_complet, functie, salariu
FROM VW_EMPLOYEE_UPDATE
WHERE LOWER(departament) = 'finante';

-- Femei cu salariu peste 5000
SELECT nume_complet, functie, gen, salariu
FROM VW_EMPLOYEE_UPDATE
WHERE gen = 'FEMININ' AND salariu > 5000;

-- Top angajati dupa salariu
SELECT nume_complet, functie, salariu
FROM VW_EMPLOYEE_UPDATE
ORDER BY salariu DESC;


