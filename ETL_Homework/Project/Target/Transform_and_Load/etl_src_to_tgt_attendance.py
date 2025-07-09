from re import match as re_match
from datetime import datetime 
import oracledb as cx_Oracle
import pandas as pd


def durata_text_to_hms(durata):
    if not isinstance(durata, str):
        return "00:00:00"
    durata = durata.strip().lower().replace(" ", "")
    match = re_match(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", durata)
    h = int(match.group(1)) if match and match.group(1) else 0
    m = int(match.group(2)) if match and match.group(2) else 0
    s = int(match.group(3)) if match and match.group(3) else 0
    return f"{h:02}:{m:02}:{s:02}"

def extract_data_sesiune(val):
    if isinstance(val, str):
        try:
            dt = datetime.strptime(val.split(",")[0].strip(), "%m/%d/%y")
            return dt.date()
        except:
            return None
    return None

# Conectare la Oracle ca SOURCE (pentru a putea citi datele din SRC_ATTENDANCE)
dsn = cx_Oracle.makedsn("localhost", 1522, service_name="xepdb1")
conn_source = cx_Oracle.connect(user="Source", password="Source_123", dsn=dsn)
cursor_source = conn_source.cursor()

# Citire date din tabela Source.SRC_ATTENDANCE (cu schema specificata)
query = """
SELECT id_attendance, nume_complet, email, durata_minute, durata_participare, ora_intrare,
       ora_iesire, titlu_meeting, id_angajat
FROM Source.SRC_ATTENDANCE
"""
df = pd.read_sql(query, con=conn_source)

# Normalizeaza numele coloanelor
df.columns = [col.lower() for col in df.columns]

# Transformari
df["data_sesiune"] = df["ora_intrare"].apply(extract_data_sesiune)
df["durata_sesiune"] = df["durata_minute"].apply(durata_text_to_hms)
df["durata_participare"] = df["durata_participare"].apply(durata_text_to_hms)


# Eliminam randuri invalide
df = df.dropna(subset=["id_attendance", "nume_complet", "email", "durata_minute", "durata_participare",
                   "ora_intrare", "ora_iesire", "titlu_meeting", "id_angajat"])

# Eliminam duplicate (email unic)
df = df.drop_duplicates(subset=["email"])

# Conversie in tuple Python native
rows = [
    (row.id_attendance, row.id_angajat, row.data_sesiune, row.ora_intrare, row.ora_iesire,
     row.durata_sesiune, row.durata_participare, row.titlu_meeting)
    for row in df.itertuples(index=False)
]

# Conectare la Oracle ca TARGET (pentru a insera datele in TGT_ATTENDANCE)
conn_target = cx_Oracle.connect(user="Target", password="Target_123", dsn=dsn)
cursor_target = conn_target.cursor()

# INSERT in TGT_ATTENDANCE
insert_sql = """
INSERT INTO TGT_ATTENDANCE (
    ID_ATTENDANCE, ID_ANGAJAT, DATA_SESIUNE, ORA_INTRARE, ORA_IESIRE, DURATA_SESIUNE,
    DURATA_PARTICIPARE, TITLU_MEETING
) VALUES (
    :1, :2, :3, :4, :5, :6, :7, :8
)
"""

cursor_target.executemany(insert_sql, rows)
conn_source.commit()

print(f"{cursor_target.rowcount} randuri inserate in TGT_ATTENDANCE.")

# Cleanup
cursor_source.close()
cursor_target.close()
conn_target.commit()
