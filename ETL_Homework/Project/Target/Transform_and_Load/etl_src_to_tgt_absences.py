import oracledb as cx_Oracle
import pandas as pd

# Conectare la Oracle ca SOURCE (pentru a putea citi datele din SRC_ABSENCES)
dsn = cx_Oracle.makedsn("localhost", 1522, service_name="xepdb1")
conn_source = cx_Oracle.connect(user="Source", password="Source_123", dsn=dsn)
cursor_source = conn_source.cursor()

# Citire date din tabela Source.SRC_ABSENCES (cu schema specificata)
query = """
SELECT id_absenta, id_angajat, nume_complet, data_start, data_sfarsit, zile,
       motiv
FROM Source.SRC_ABSENCES
"""
df = pd.read_sql(query, con=conn_source)

# Normalizeaza numele coloanelor
df.columns = [col.lower() for col in df.columns]

# Nu este nevoie de transformari suplimentare

# Eliminam randuri invalide
df = df.dropna(subset=["id_absenta", "id_angajat", "nume_complet", "data_start", "data_sfarsit",
                       "zile", "motiv"])

# Conversie in tuple Python native
rows = [
    (row.id_absenta, row.id_angajat, row.data_start, row.data_sfarsit, row.zile,
     row.motiv)
    for row in df.itertuples(index=False)
]

# Conectare la Oracle ca TARGET (pentru a insera datele in TGT_ABSENCES)
conn_target = cx_Oracle.connect(user="Target", password="Target_123", dsn=dsn)
cursor_target = conn_target.cursor()

# INSERT in TGT_ABSENCES
insert_sql = """
INSERT INTO TGT_ABSENCES (
    ID_ABSENTA, ID_ANGAJAT, DATA_START, DATA_SFARSIT, ZILE, MOTIV
) VALUES (
    :1, :2, :3, :4, :5, :6
)
"""

cursor_target.executemany(insert_sql, rows)
conn_source.commit()

print(f"{cursor_target.rowcount} randuri inserate in TGT_ABSENCES.")

# Cleanup
cursor_source.close()
cursor_target.close()
conn_target.commit()
