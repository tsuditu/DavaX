from datetime import timedelta

import oracledb as cx_Oracle
import pandas as pd


def ore_lucrate_to_time(ore_lucrate):
    total_minutes = int(round(ore_lucrate * 60))
    return str(timedelta(minutes=total_minutes))

# Conectare la Oracle ca SOURCE (pentru a putea citi datele din SRC_PONTAJ)
dsn = cx_Oracle.makedsn("localhost", 1522, service_name="xepdb1")
conn_source = cx_Oracle.connect(user="Source", password="Source_123", dsn=dsn)
cursor_source = conn_source.cursor()

# Citire date din tabela Source.SRC_PONTAJ (cu schema specificata)
query = """
SELECT id_pontaj, id_angajat, data_pontaj, ore_lucrate, activitate
FROM Source.SRC_PONTAJ
"""
df = pd.read_sql(query, con=conn_source)

# Normalizeaza numele coloanelor
df.columns = [col.lower() for col in df.columns]

# Transformari
df["ore_lucrate"] = df["ore_lucrate"].apply(ore_lucrate_to_time)
df["activitate"] = df["activitate"].str.upper()

# Eliminam randuri invalide
df = df.dropna(subset=["id_pontaj", "id_angajat", "data_pontaj", "activitate", "ore_lucrate"])

# Conversie in tuple Python native
rows = [
    (row.id_pontaj, row.id_angajat, row.data_pontaj, row.activitate, row.ore_lucrate)
    for row in df.itertuples(index=False)
]

# Conectare la Oracle ca TARGET (pentru a insera datele in TGT_PONTAJ)
conn_target = cx_Oracle.connect(user="Target", password="Target_123", dsn=dsn)
cursor_target = conn_target.cursor()

# INSERT in TGT_PONTAJ
insert_sql = """
INSERT INTO TGT_PONTAJ (
    ID_PONTAJ, ID_ANGAJAT, DATA_PONTAJ, ACTIVITATE, ORE_LUCRATE
) VALUES (
    :1, :2, :3, :4, :5
)
"""

cursor_target.executemany(insert_sql, rows)
conn_source.commit()

print(f"{cursor_target.rowcount} randuri inserate in TGT_PONTAJ.")

# Cleanup
cursor_source.close()
cursor_target.close()
conn_target.commit()
