import oracledb as cx_Oracle
import pandas as pd

# Conectare la Oracle ca SOURCE (pentru a putea citi datele din SRC_DEPARTAMENT)
dsn = cx_Oracle.makedsn("localhost", 1522, service_name="xepdb1")
conn_source = cx_Oracle.connect(user="Source", password="Source_123", dsn=dsn)
cursor_source = conn_source.cursor()

# Citire date din tabela Source.SRC_DEPARTAMENT (cu schema specificata)
query = """
SELECT id_departament, nume, cod_unic
FROM Source.SRC_DEPARTAMENT
"""
df = pd.read_sql(query, con=conn_source)

# Normalizeaza numele coloanelor
df.columns = [col.lower() for col in df.columns]

# Transformari
df["nume"] = df["nume"].str.title()
df["cod_unic"] = df["cod_unic"].str.upper()

# Eliminam randuri invalide
df = df.dropna(subset=["id_departament", "nume", "cod_unic"])

# Conversie in tuple Python native
rows = [tuple(row) for row in df.itertuples(index=False, name=None)]

# Conectare la Oracle ca TARGET (pentru a insera datele in TGT_DEPARTAMENT)
conn_target = cx_Oracle.connect(user="Target", password="Target_123", dsn=dsn)
cursor_target = conn_target.cursor()

# INSERT in TGT_DEPARTAMENT
insert_sql = """
INSERT INTO TGT_DEPARTAMENT (
    ID_DEPARTAMENT, NUME, COD_UNIC
) VALUES (
    :1, :2, :3
)
"""

cursor_target.executemany(insert_sql, rows)
conn_source.commit()

print(f"{cursor_target.rowcount} randuri inserate in TGT_DEPARTAMENT.")

# Cleanup
cursor_source.close()
cursor_target.close()
conn_target.commit()
