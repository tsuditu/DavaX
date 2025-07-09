import oracledb as cx_Oracle
import pandas as pd

# Conectare la Oracle ca SOURCE (pentru a putea citi datele din SRC_ANGAJAT)
dsn = cx_Oracle.makedsn("localhost", 1522, service_name="xepdb1")
conn_source = cx_Oracle.connect(user="Source", password="Source_123", dsn=dsn)
cursor_source = conn_source.cursor()

# Citire date din tabela Source.SRC_ANGAJAT (cu schema specificata)
query = """
SELECT id_angajat, nume, email, salariu, gen, functie,
       data_angajare, status, id_departament
FROM Source.SRC_ANGAJAT
"""
df = pd.read_sql(query, con=conn_source)

# Normalizeaza numele coloanelor
df.columns = [col.lower() for col in df.columns]

# Transformari
df["nume"] = df["nume"].str.title()
df["email"] = df["email"].str.lower()
df["gen"] = df["gen"].str.upper()
df["functie"] = df["functie"].str.title()
df["status"] = df["status"].str.upper()

# Eliminam randuri invalide
df = df.dropna(subset=["email", "nume", "gen", "functie", "status", "id_angajat", "salariu", "data_angajare", "id_departament"])

# Eliminam duplicate (email unic)
df = df.drop_duplicates(subset=["email"])

# Conversie in tuple Python native
rows = [tuple(row) for row in df.itertuples(index=False, name=None)]

# Conectare la Oracle ca TARGET (pentru a insera datele in TGT_ANGAJAT)
conn_target = cx_Oracle.connect(user="Target", password="Target_123", dsn=dsn)
cursor_target = conn_target.cursor()

# INSERT in TGT_ANGAJAT
insert_sql = """
INSERT INTO TGT_ANGAJAT (
    ID_ANGAJAT, NUME, EMAIL, SALARIU, GEN,
    FUNCTIE, DATA_ANGAJARE, STATUS, ID_DEPARTAMENT
) VALUES (
    :1, :2, :3, :4, :5, :6, :7, :8, :9
)
"""

cursor_target.executemany(insert_sql, rows)
conn_source.commit()

print(f"{cursor_target.rowcount} randuri inserate in TGT_ANGAJAT.")

# Cleanup
cursor_source.close()
cursor_target.close()
conn_target.commit()
