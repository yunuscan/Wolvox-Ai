# -*- coding: utf-8 -*-
"""
Wolvox Firebird Veritabanı - Faz 1-5 Kapsamlı Analiz Scripti
SADECE SELECT sorguları kullanır.
"""
import fdb
import os
import sys
import json
from datetime import datetime
from collections import defaultdict

# Bağlantı bilgileri
FB_CLIENT = r"C:\Users\yunuscan\Desktop\WolvoxDBSeması\fb25_x64\bin\fbclient.dll"
DB_PATH = r"C:\AKINSOFT\Wolvox9\Database_FB\DEMOWOLVOX\2026\WOLVOX.fdb"
HOST = "localhost"
PORT = 3050
USER = "RAPORCU"
PASSWORD = "Raporcu2"
CHARSET = "WIN1254"

OUTPUT_DIR = r"C:\Users\yunuscan\Desktop\WolvoxDBSeması\wolvox-docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Analiz tarihi
ANALYSIS_DATE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def connect():
    return fdb.connect(
        host=HOST, port=PORT, database=DB_PATH,
        user=USER, password=PASSWORD,
        fb_library_name=FB_CLIENT, charset=CHARSET
    )

def safe_strip(val):
    """Firebird CHAR alanlarından trailing boşlukları temizle"""
    if val is None:
        return None
    if isinstance(val, str):
        return val.strip()
    if isinstance(val, bytes):
        try:
            return val.decode('cp1254').strip()
        except:
            try:
                return val.decode('utf-8').strip()
            except:
                return str(val).strip()
    return val

def decode_field_type(field_type, field_sub_type, field_length, field_precision, field_scale, char_length):
    """Firebird alan tiplerini okunabilir isimlere çevir"""
    type_map = {
        7: 'SMALLINT',
        8: 'INTEGER',
        9: 'QUAD',
        10: 'FLOAT',
        12: 'DATE',
        13: 'TIME',
        14: 'CHAR',
        16: 'BIGINT',
        23: 'BOOLEAN',
        27: 'DOUBLE PRECISION',
        35: 'TIMESTAMP',
        37: 'VARCHAR',
        40: 'CSTRING',
        261: 'BLOB',
    }
    
    base = type_map.get(field_type, f'UNKNOWN({field_type})')
    
    # Numeric/Decimal alt tipleri
    if field_type in (7, 8, 16) and field_scale and field_scale < 0:
        if field_sub_type == 1:
            return f'NUMERIC({field_precision},{-field_scale})'
        elif field_sub_type == 2:
            return f'DECIMAL({field_precision},{-field_scale})'
        else:
            return f'{base}(scale={field_scale})'
    
    # CHAR/VARCHAR uzunluk
    if field_type in (14, 37) and char_length:
        return f'{base}({char_length})'
    
    # BLOB alt tipleri
    if field_type == 261:
        if field_sub_type == 0:
            return 'BLOB SUB_TYPE BINARY'
        elif field_sub_type == 1:
            return 'BLOB SUB_TYPE TEXT'
        else:
            return f'BLOB SUB_TYPE {field_sub_type}'
    
    return base

# ===== FAZ 1: GENEL ŞEMA ENVANTERİ =====
print("=" * 60)
print("FAZ 1: Genel Şema Envanteri çıkarılıyor...")
print("=" * 60)

con = connect()
cur = con.cursor()

# 1.1 — Tüm kullanıcı tabloları
print("\n[1.1] Kullanıcı tabloları çıkarılıyor...")
cur.execute("""
    SELECT RDB$RELATION_NAME 
    FROM RDB$RELATIONS 
    WHERE RDB$SYSTEM_FLAG = 0 
    AND RDB$VIEW_BLR IS NULL
    ORDER BY RDB$RELATION_NAME
""")
all_tables = [safe_strip(row[0]) for row in cur.fetchall()]
print(f"  Toplam {len(all_tables)} tablo bulundu.")

# 1.2 — Tablo kolonları ve veri tipleri
print("\n[1.2] Kolon bilgileri çıkarılıyor...")
table_columns = {}
for tbl in all_tables:
    cur.execute("""
        SELECT
            rf.RDB$FIELD_NAME,
            f.RDB$FIELD_TYPE,
            f.RDB$FIELD_SUB_TYPE,
            f.RDB$FIELD_LENGTH,
            f.RDB$FIELD_PRECISION,
            f.RDB$FIELD_SCALE,
            f.RDB$CHARACTER_LENGTH,
            rf.RDB$NULL_FLAG,
            rf.RDB$DEFAULT_SOURCE,
            rf.RDB$FIELD_POSITION
        FROM RDB$RELATION_FIELDS rf
        JOIN RDB$FIELDS f ON rf.RDB$FIELD_SOURCE = f.RDB$FIELD_NAME
        WHERE rf.RDB$RELATION_NAME = ?
        ORDER BY rf.RDB$FIELD_POSITION
    """, (tbl,))
    
    cols = []
    for row in cur.fetchall():
        col_name = safe_strip(row[0])
        field_type = row[1]
        field_sub = row[2]
        field_len = row[3]
        field_prec = row[4]
        field_scale = row[5]
        char_len = row[6]
        null_flag = row[7]
        default_src = safe_strip(row[8])
        
        type_name = decode_field_type(field_type, field_sub, field_len, field_prec, field_scale, char_len)
        nullable = "NOT NULL" if null_flag == 1 else "NULL"
        
        cols.append({
            'name': col_name,
            'type': type_name,
            'nullable': nullable,
            'default': default_src
        })
    table_columns[tbl] = cols

print(f"  Toplam {sum(len(v) for v in table_columns.values())} kolon işlendi.")

# 1.3 — Primary Key'ler
print("\n[1.3] Primary key'ler çıkarılıyor...")
cur.execute("""
    SELECT
        rc.RDB$RELATION_NAME,
        rc.RDB$CONSTRAINT_NAME,
        sg.RDB$FIELD_NAME
    FROM RDB$RELATION_CONSTRAINTS rc
    JOIN RDB$INDEX_SEGMENTS sg ON rc.RDB$INDEX_NAME = sg.RDB$INDEX_NAME
    WHERE rc.RDB$CONSTRAINT_TYPE = 'PRIMARY KEY'
    ORDER BY rc.RDB$RELATION_NAME, sg.RDB$FIELD_POSITION
""")
primary_keys = defaultdict(list)
for row in cur.fetchall():
    tbl = safe_strip(row[0])
    col = safe_strip(row[2])
    primary_keys[tbl].append(col)
print(f"  {len(primary_keys)} tabloda PK tanımlı.")

# 1.4 — Foreign Key'ler
print("\n[1.4] Foreign key'ler çıkarılıyor...")
cur.execute("""
    SELECT
        rc.RDB$RELATION_NAME AS FK_TABLE,
        rc.RDB$CONSTRAINT_NAME AS FK_NAME,
        sg_fk.RDB$FIELD_NAME AS FK_COLUMN,
        refc.RDB$CONST_NAME_UQ AS REF_CONSTRAINT,
        rc2.RDB$RELATION_NAME AS REF_TABLE,
        sg_pk.RDB$FIELD_NAME AS REF_COLUMN
    FROM RDB$RELATION_CONSTRAINTS rc
    JOIN RDB$REF_CONSTRAINTS refc ON rc.RDB$CONSTRAINT_NAME = refc.RDB$CONSTRAINT_NAME
    JOIN RDB$RELATION_CONSTRAINTS rc2 ON refc.RDB$CONST_NAME_UQ = rc2.RDB$CONSTRAINT_NAME
    JOIN RDB$INDEX_SEGMENTS sg_fk ON rc.RDB$INDEX_NAME = sg_fk.RDB$INDEX_NAME
    JOIN RDB$INDEX_SEGMENTS sg_pk ON rc2.RDB$INDEX_NAME = sg_pk.RDB$INDEX_NAME
    WHERE rc.RDB$CONSTRAINT_TYPE = 'FOREIGN KEY'
    ORDER BY rc.RDB$RELATION_NAME
""")
foreign_keys = []
for row in cur.fetchall():
    fk = {
        'fk_table': safe_strip(row[0]),
        'fk_name': safe_strip(row[1]),
        'fk_column': safe_strip(row[2]),
        'ref_table': safe_strip(row[4]),
        'ref_column': safe_strip(row[5])
    }
    foreign_keys.append(fk)
print(f"  {len(foreign_keys)} foreign key ilişkisi bulundu.")

# 1.5 — Index'ler
print("\n[1.5] Index'ler çıkarılıyor...")
cur.execute("""
    SELECT
        i.RDB$RELATION_NAME,
        i.RDB$INDEX_NAME,
        i.RDB$UNIQUE_FLAG,
        i.RDB$INDEX_INACTIVE,
        sg.RDB$FIELD_NAME,
        sg.RDB$FIELD_POSITION
    FROM RDB$INDICES i
    JOIN RDB$INDEX_SEGMENTS sg ON i.RDB$INDEX_NAME = sg.RDB$INDEX_NAME
    WHERE i.RDB$SYSTEM_FLAG = 0
    ORDER BY i.RDB$RELATION_NAME, i.RDB$INDEX_NAME, sg.RDB$FIELD_POSITION
""")
indices = defaultdict(list)
for row in cur.fetchall():
    tbl = safe_strip(row[0])
    idx_name = safe_strip(row[1])
    unique = row[2]
    inactive = row[3]
    field = safe_strip(row[4])
    indices[tbl].append({
        'index_name': idx_name,
        'unique': unique == 1,
        'inactive': inactive == 1 if inactive else False,
        'field': field
    })
print(f"  {len(indices)} tabloda index tanımlı.")

# 1.6 — Generator'lar
print("\n[1.6] Generator/Sequence'ler çıkarılıyor...")
cur.execute("""
    SELECT RDB$GENERATOR_NAME
    FROM RDB$GENERATORS
    WHERE RDB$SYSTEM_FLAG = 0
    ORDER BY RDB$GENERATOR_NAME
""")
generators = []
for row in cur.fetchall():
    gen_name = safe_strip(row[0])
    try:
        cur2 = con.cursor()
        cur2.execute(f"SELECT GEN_ID({gen_name}, 0) FROM RDB$DATABASE")
        gen_val = cur2.fetchone()[0]
        cur2.close()
    except:
        gen_val = "N/A"
    generators.append({'name': gen_name, 'current_value': gen_val})
print(f"  {len(generators)} generator bulundu.")

# 1.7 — Trigger'lar
print("\n[1.7] Trigger'lar çıkarılıyor...")
cur.execute("""
    SELECT
        RDB$TRIGGER_NAME,
        RDB$RELATION_NAME,
        RDB$TRIGGER_TYPE,
        RDB$TRIGGER_SEQUENCE,
        RDB$TRIGGER_INACTIVE,
        RDB$TRIGGER_SOURCE
    FROM RDB$TRIGGERS
    WHERE RDB$SYSTEM_FLAG = 0
    ORDER BY RDB$RELATION_NAME, RDB$TRIGGER_NAME
""")
triggers = []
for row in cur.fetchall():
    trig = {
        'name': safe_strip(row[0]),
        'table': safe_strip(row[1]),
        'type': row[2],
        'sequence': row[3],
        'inactive': row[4] == 1 if row[4] else False,
        'source': safe_strip(row[5])
    }
    triggers.append(trig)
print(f"  {len(triggers)} trigger bulundu.")

# 1.8 — Stored Procedure'ler
print("\n[1.8] Stored procedure'ler çıkarılıyor...")
cur.execute("""
    SELECT
        RDB$PROCEDURE_NAME,
        RDB$PROCEDURE_SOURCE,
        RDB$PROCEDURE_INPUTS,
        RDB$PROCEDURE_OUTPUTS
    FROM RDB$PROCEDURES
    ORDER BY RDB$PROCEDURE_NAME
""")
procedures = []
for row in cur.fetchall():
    proc = {
        'name': safe_strip(row[0]),
        'source': safe_strip(row[1]),
        'inputs': row[2] if row[2] else 0,
        'outputs': row[3] if row[3] else 0
    }
    procedures.append(proc)
print(f"  {len(procedures)} stored procedure bulundu.")

# SP parametreleri
print("  SP parametreleri çıkarılıyor...")
sp_params = defaultdict(list)
cur.execute("""
    SELECT
        RDB$PROCEDURE_NAME,
        RDB$PARAMETER_NAME,
        RDB$PARAMETER_TYPE,
        RDB$PARAMETER_NUMBER,
        RDB$FIELD_SOURCE
    FROM RDB$PROCEDURE_PARAMETERS
    ORDER BY RDB$PROCEDURE_NAME, RDB$PARAMETER_TYPE, RDB$PARAMETER_NUMBER
""")
for row in cur.fetchall():
    sp_params[safe_strip(row[0])].append({
        'name': safe_strip(row[1]),
        'type': 'INPUT' if row[2] == 0 else 'OUTPUT',
        'position': row[3]
    })

# ===== FAZ 2: İŞ ALANLARINA GÖRE TABLOLARI SINIFLANDIRMA =====
print("\n" + "=" * 60)
print("FAZ 2: İş alanlarına göre tablo sınıflandırması...")
print("=" * 60)

business_keywords = {
    'STOK': ['STOK', 'STK', 'URUN', 'BARKOD', 'BARCODE'],
    'CARI': ['CARI', 'CRI', 'MUSTERI', 'TEDARIK'],
    'FATURA': ['FATURA', 'FAT', 'IRSALIYE', 'IRS'],
    'KASA': ['KASA', 'KAS'],
    'BANKA': ['BANKA', 'BNK', 'BANK'],
    'CEK_SENET': ['CEK', 'SENET', 'SNT'],
    'DEPO': ['DEPO', 'DPO'],
    'PERSONEL': ['PERSONEL', 'PRS', 'PERS'],
    'SIPARIS': ['SIPARIS', 'SIP', 'ORDER'],
    'MUHASEBE': ['MUHASEBE', 'MUH', 'HESAP'],
    'KDV_VERGI': ['KDV', 'VERGI', 'TAX'],
    'GRUP': ['GRUP', 'GRP', 'CATEGORY', 'KATEGORI'],
    'BIRIM': ['BIRIM', 'BRM', 'OLCU'],
    'FIYAT': ['FIYAT', 'FYT', 'PRICE'],
    'RAPOR': ['RAPOR', 'RPR', 'REPORT'],
    'KULLANICI': ['KULLANICI', 'USER', 'KUL'],
    'PARAMETRELER': ['PARAMETRE', 'PARAM', 'PRM', 'AYAR'],
}

business_tables = defaultdict(list)
uncategorized = []

for tbl in all_tables:
    categorized = False
    for category, keywords in business_keywords.items():
        for kw in keywords:
            if kw in tbl.upper():
                business_tables[category].append(tbl)
                categorized = True
                break
        if categorized:
            break
    if not categorized:
        uncategorized.append(tbl)

for cat, tables in sorted(business_tables.items()):
    print(f"  {cat}: {len(tables)} tablo")
print(f"  Sınıflandırılamayan: {len(uncategorized)} tablo")

# ===== FAZ 3: REFERANS/LOOKUP TABLOLARI =====
print("\n" + "=" * 60)
print("FAZ 3: Referans/Lookup tabloları çıkarılıyor...")
print("=" * 60)

# Küçük referans tablolarını bul (< 500 satır ve az kolon)
reference_tables_data = {}
potential_ref_tables = []

for tbl in all_tables:
    cols = table_columns.get(tbl, [])
    # Referans tablosu ipuçları: az kolon (< 10), adında GRUP, TIP, TUR, KOD, BIRIM, KDV vb.
    ref_keywords = ['GRUP', 'TIP', 'TUR', 'KOD', 'BIRIM', 'KDV', 'OLCU', 'DEPARTMAN', 'BOLUM', 
                    'SEHIR', 'ILCE', 'ULKE', 'PARA_BIRIMI', 'DOVIZ', 'SEKTOR', 'MESLEK',
                    'SINIF', 'KATEGORI', 'DURUM']
    is_ref = False
    for kw in ref_keywords:
        if kw in tbl.upper():
            is_ref = True
            break
    
    if is_ref or len(cols) <= 8:
        potential_ref_tables.append(tbl)

print(f"  {len(potential_ref_tables)} potansiyel referans tablosu tespit edildi.")
print("  İçerikleri çıkarılıyor (max 500 satır)...")

for tbl in potential_ref_tables:
    try:
        cur.execute(f'SELECT COUNT(*) FROM "{tbl}"')
        count = cur.fetchone()[0]
        if count > 0 and count <= 500:
            cur.execute(f'SELECT FIRST 500 * FROM "{tbl}"')
            rows = cur.fetchall()
            col_names = [safe_strip(d[0]) for d in cur.description]
            
            # Kişisel veri içerebilecek kolonları anonimleştir
            pii_keywords = ['TELEFON', 'ADRES', 'TC', 'TCKIMLIK', 'EPOSTA', 'EMAIL', 'GSM', 'CEP']
            pii_cols = set()
            for i, cn in enumerate(col_names):
                if cn:
                    for pk in pii_keywords:
                        if pk in cn.upper():
                            pii_cols.add(i)
            
            clean_rows = []
            for row in rows:
                clean_row = []
                for i, val in enumerate(row):
                    if i in pii_cols:
                        clean_row.append("[ANONİMLEŞTİRİLDİ]")
                    else:
                        clean_row.append(safe_strip(val) if isinstance(val, (str, bytes)) else val)
                clean_rows.append(clean_row)
            
            reference_tables_data[tbl] = {
                'columns': col_names,
                'row_count': count,
                'data': clean_rows
            }
    except Exception as e:
        reference_tables_data[tbl] = {'error': str(e), 'row_count': 0}

print(f"  {len(reference_tables_data)} tablodan veri çekildi.")

# ===== FAZ 4: ÖRNEK VERİ İLE DOĞRULAMA =====
print("\n" + "=" * 60)
print("FAZ 4: Örnek veri ile doğrulama...")
print("=" * 60)

# Ana tablolardan örnek satırlar
sample_data = {}
important_tables_keywords = ['STOK', 'CARI', 'FATURA', 'KASA', 'BANKA', 'SIPARIS', 'DEPO']
pii_table_keywords = ['CARI', 'MUSTERI', 'PERSONEL', 'PERS']

for tbl in all_tables:
    is_important = False
    for kw in important_tables_keywords:
        if kw in tbl.upper():
            is_important = True
            break
    
    if not is_important:
        continue
    
    # PII içerebilecek tablolarda sadece şema bilgisi
    is_pii = False
    for kw in pii_table_keywords:
        if kw in tbl.upper():
            is_pii = True
            break
    
    try:
        cur.execute(f'SELECT COUNT(*) FROM "{tbl}"')
        count = cur.fetchone()[0]
        
        if is_pii:
            sample_data[tbl] = {
                'row_count': count,
                'note': 'Kişisel veri içerebilir - sadece şema bilgisi verildi',
                'columns': [c['name'] + ' (' + c['type'] + ', ' + c['nullable'] + ')' for c in table_columns.get(tbl, [])]
            }
        else:
            if count > 0:
                cur.execute(f'SELECT FIRST 5 * FROM "{tbl}"')
                rows = cur.fetchall()
                col_names = [safe_strip(d[0]) for d in cur.description]
                
                clean_rows = []
                for row in rows:
                    clean_row = []
                    for val in row:
                        v = safe_strip(val) if isinstance(val, (str, bytes)) else val
                        # Çok uzun BLOB'ları kısalt
                        if isinstance(v, str) and len(v) > 200:
                            v = v[:200] + "...[TRUNCATED]"
                        clean_row.append(v)
                    clean_rows.append(clean_row)
                
                sample_data[tbl] = {
                    'row_count': count,
                    'columns': col_names,
                    'sample_rows': clean_rows
                }
            else:
                sample_data[tbl] = {
                    'row_count': 0,
                    'note': 'Tablo boş'
                }
    except Exception as e:
        sample_data[tbl] = {'error': str(e)}

print(f"  {len(sample_data)} ana tablodan veri/şema bilgisi çıkarıldı.")

# ===== FAZ 5: YAZMA İŞLEMLERİ RİSK ANALİZİ =====
print("\n" + "=" * 60)
print("FAZ 5: Yazma işlemleri risk analizi...")
print("=" * 60)

# Stok ve Cari tabloları için NOT NULL kolon analizi
write_analysis = {}

for category in ['STOK', 'CARI']:
    relevant_tables = business_tables.get(category, [])
    analysis = {}
    for tbl in relevant_tables:
        cols = table_columns.get(tbl, [])
        required_cols = [c for c in cols if c['nullable'] == 'NOT NULL']
        
        # Bu tabloya referans veren FK'ler
        referencing_fks = [fk for fk in foreign_keys if fk['ref_table'] == tbl]
        # Bu tablodan referans edilen FK'ler
        referenced_fks = [fk for fk in foreign_keys if fk['fk_table'] == tbl]
        
        # İlişkili trigger'lar
        related_triggers = [t for t in triggers if t['table'] == tbl]
        
        # İlişkili generator (tahmin: tablo adına benzer generator)
        related_generators = []
        for gen in generators:
            if tbl.replace(' ', '') in gen['name'].replace(' ', '') or \
               gen['name'].replace('GEN_', '').replace('_ID', '') in tbl:
                related_generators.append(gen)
        
        analysis[tbl] = {
            'total_columns': len(cols),
            'required_columns': required_cols,
            'referencing_fks': referencing_fks,
            'referenced_fks': referenced_fks,
            'related_triggers': related_triggers,
            'related_generators': related_generators,
            'row_count': sample_data.get(tbl, {}).get('row_count', 'N/A')
        }
    write_analysis[category] = analysis

print("  Stok ve Cari tabloları için yazma analizi tamamlandı.")

cur.close()
con.close()
print("\nVeritabanı bağlantısı kapatıldı.")

# ===== ÇIKTI DOSYALARI OLUŞTURMA =====
print("\n" + "=" * 60)
print("ÇIKTI DOSYALARI OLUŞTURULUYOR...")
print("=" * 60)

header = f"""---
**Analiz Tarihi:** {ANALYSIS_DATE}  
**Firebird Sürümü:** 2.5.6 (WI-V6.3.6.27020 Firebird 2.5)  
**Veritabanı:** DEMOWOLVOX (Wolvox 9)  
**Veritabanı Yolu:** `C:\\AKINSOFT\\Wolvox9\\Database_FB\\DEMOWOLVOX\\2026\\WOLVOX.fdb`  
**Charset:** WIN1254  
**Not:** Bu dokümantasyon salt-okunur analiz ile oluşturulmuştur. Wolvox güncellemelerinde şema değişebilir.

---

"""

# ===== 01-genel-bakis.md =====
print("\n[1/7] 01-genel-bakis.md oluşturuluyor...")
with open(os.path.join(OUTPUT_DIR, "01-genel-bakis.md"), "w", encoding="utf-8") as f:
    f.write("# Wolvox Firebird Veritabanı — Genel Bakış\n\n")
    f.write(header)
    f.write("## Özet İstatistikler\n\n")
    f.write(f"| Metrik | Değer |\n")
    f.write(f"|--------|-------|\n")
    f.write(f"| Toplam Kullanıcı Tablosu | **{len(all_tables)}** |\n")
    f.write(f"| Toplam Kolon | **{sum(len(v) for v in table_columns.values())}** |\n")
    f.write(f"| Primary Key Tanımlı Tablo | **{len(primary_keys)}** |\n")
    f.write(f"| Foreign Key İlişkisi | **{len(foreign_keys)}** |\n")
    f.write(f"| Generator/Sequence | **{len(generators)}** |\n")
    f.write(f"| Trigger | **{len(triggers)}** |\n")
    f.write(f"| Stored Procedure | **{len(procedures)}** |\n")
    f.write(f"| View | **0** |\n\n")
    
    f.write("## Tespit Edilen İş Modülleri\n\n")
    for cat, tables in sorted(business_tables.items()):
        f.write(f"### {cat} ({len(tables)} tablo)\n")
        for t in sorted(tables):
            count = sample_data.get(t, {}).get('row_count', '?')
            f.write(f"- `{t}` ({count} satır)\n")
        f.write("\n")
    
    if uncategorized:
        f.write(f"### Sınıflandırılamayan Tablolar ({len(uncategorized)} adet)\n")
        for t in sorted(uncategorized):
            f.write(f"- `{t}`\n")
        f.write("\n")

print("  01-genel-bakis.md [OK]")

# ===== 02-tablo-sozlugu.md =====
print("[2/7] 02-tablo-sozlugu.md oluşturuluyor...")
with open(os.path.join(OUTPUT_DIR, "02-tablo-sozlugu.md"), "w", encoding="utf-8") as f:
    f.write("# Wolvox Firebird Veritabanı — Tablo Sözlüğü\n\n")
    f.write(header)
    
    for tbl in all_tables:
        f.write(f"## {tbl}\n\n")
        
        # Tahmini amaç
        purpose = "Bilinmiyor"
        for cat, tables in business_tables.items():
            if tbl in tables:
                purpose = f"{cat} modülü tablosu"
                break
        f.write(f"**Tahmini Amaç:** {purpose}  \n")
        
        pk = primary_keys.get(tbl, [])
        if pk:
            f.write(f"**Primary Key:** {', '.join(pk)}  \n")
        
        # FK'ler
        tbl_fks = [fk for fk in foreign_keys if fk['fk_table'] == tbl]
        if tbl_fks:
            f.write(f"**Foreign Key'ler:**\n")
            for fk in tbl_fks:
                f.write(f"  - `{fk['fk_column']}` → `{fk['ref_table']}.{fk['ref_column']}` ({fk['fk_name']})\n")
        
        f.write(f"\n")
        
        cols = table_columns.get(tbl, [])
        if cols:
            f.write(f"| # | Kolon Adı | Veri Tipi | Null | Default |\n")
            f.write(f"|---|-----------|-----------|------|--------|\n")
            for i, col in enumerate(cols, 1):
                default = col['default'] if col['default'] else ""
                # Markdown tablo kırılmalarını önle
                default = default.replace("|", "\\|").replace("\n", " ") if default else ""
                f.write(f"| {i} | `{col['name']}` | {col['type']} | {col['nullable']} | {default} |\n")
        f.write(f"\n---\n\n")

print("  02-tablo-sozlugu.md [OK]")

# ===== 03-iliski-haritasi.md =====
print("[3/7] 03-iliski-haritasi.md oluşturuluyor...")
with open(os.path.join(OUTPUT_DIR, "03-iliski-haritasi.md"), "w", encoding="utf-8") as f:
    f.write("# Wolvox Firebird Veritabanı — İlişki Haritası\n\n")
    f.write(header)
    
    if foreign_keys:
        f.write("## Foreign Key İlişkileri Listesi\n\n")
        f.write("| FK Tablo | FK Kolon | → Referans Tablo | Referans Kolon | FK Adı |\n")
        f.write("|----------|----------|-----------------|----------------|--------|\n")
        for fk in sorted(foreign_keys, key=lambda x: x['fk_table']):
            f.write(f"| `{fk['fk_table']}` | `{fk['fk_column']}` | `{fk['ref_table']}` | `{fk['ref_column']}` | {fk['fk_name']} |\n")
        f.write("\n")
        
        # Mermaid ER diyagramı
        f.write("## ER Diyagramı (Mermaid)\n\n")
        f.write("```mermaid\nerDiagram\n")
        
        # FK'lerden benzersiz tablo çiftleri
        seen_relations = set()
        for fk in foreign_keys:
            key = (fk['fk_table'], fk['ref_table'], fk['fk_column'])
            if key not in seen_relations:
                seen_relations.add(key)
                fk_tbl_safe = fk['fk_table'].replace(' ', '_').replace('-', '_')
                ref_tbl_safe = fk['ref_table'].replace(' ', '_').replace('-', '_')
                f.write(f'    {ref_tbl_safe} ||--o{{ {fk_tbl_safe} : "{fk["fk_column"]}"\n')
        
        f.write("```\n\n")
    else:
        f.write("**Not:** Bu veritabanında tanımlı foreign key ilişkisi bulunamadı.\n")
        f.write("Bu, Wolvox'un ilişkileri uygulama katmanında (trigger veya kod ile) yönetiyor olabileceğini gösterir.\n\n")
    
    # Tablo adlarından tahmin edilen ilişkiler
    f.write("## Tablo Adlarından Tahmin Edilen İlişkiler\n\n")
    f.write("Aşağıdaki ilişkiler, tablo ve kolon adlarından çıkarım yapılarak listelenmiştir. ")
    f.write("Gerçek ilişkiler doğrulanmalıdır.\n\n")
    
    # Kolon adlarından FK tahmini (ID ile biten kolonlar)
    guessed_relations = []
    for tbl in all_tables:
        cols = table_columns.get(tbl, [])
        for col in cols:
            name = col['name'].upper() if col['name'] else ''
            # _ID, _KODU, _NO gibi biten kolonlar potansiyel FK
            if name.endswith('_ID') or name.endswith('_KODU') or name.endswith('_NO'):
                # Muhtemel referans tablo
                prefix = name.rsplit('_', 1)[0] if '_' in name else name
                for ref_tbl in all_tables:
                    if ref_tbl != tbl and prefix in ref_tbl.upper():
                        guessed_relations.append({
                            'table': tbl,
                            'column': col['name'],
                            'probable_ref': ref_tbl
                        })
                        break
    
    if guessed_relations:
        f.write("| Tablo | Kolon | Muhtemel Referans Tablo |\n")
        f.write("|-------|-------|------------------------|\n")
        for gr in guessed_relations[:100]:  # Max 100 
            f.write(f"| `{gr['table']}` | `{gr['column']}` | `{gr['probable_ref']}` |\n")
    f.write("\n")

print("  03-iliski-haritasi.md [OK]")

# ===== 04-referans-tablolari.md =====
print("[4/7] 04-referans-tablolari.md oluşturuluyor...")
with open(os.path.join(OUTPUT_DIR, "04-referans-tablolari.md"), "w", encoding="utf-8") as f:
    f.write("# Wolvox Firebird Veritabanı — Referans/Lookup Tabloları\n\n")
    f.write(header)
    f.write("Bu dosya, grup kodları, KDV oranları, birimler, departmanlar gibi referans ")
    f.write("tablolarının tam içeriğini (kod → açıklama eşleşmesi) içerir.\n\n")
    
    for tbl, data in sorted(reference_tables_data.items()):
        if 'error' in data:
            f.write(f"## {tbl}\n\n**Hata:** {data['error']}\n\n---\n\n")
            continue
        
        if data['row_count'] == 0:
            f.write(f"## {tbl} (Boş tablo)\n\n---\n\n")
            continue
        
        f.write(f"## {tbl} ({data['row_count']} satır)\n\n")
        
        columns = data.get('columns', [])
        rows = data.get('data', [])
        
        if columns and rows:
            # Markdown tablo
            f.write("| " + " | ".join(str(c) for c in columns) + " |\n")
            f.write("|" + "|".join(["---" for _ in columns]) + "|\n")
            
            for row in rows:
                cells = []
                for val in row:
                    s = str(val) if val is not None else ""
                    s = s.replace("|", "\\|").replace("\n", " ")
                    if len(s) > 100:
                        s = s[:100] + "..."
                    cells.append(s)
                f.write("| " + " | ".join(cells) + " |\n")
        
        f.write(f"\n---\n\n")

print("  04-referans-tablolari.md [OK]")

# ===== 05-generator-ve-trigger-envanteri.md =====
print("[5/7] 05-generator-ve-trigger-envanteri.md oluşturuluyor...")
with open(os.path.join(OUTPUT_DIR, "05-generator-ve-trigger-envanteri.md"), "w", encoding="utf-8") as f:
    f.write("# Wolvox Firebird Veritabanı — Generator ve Trigger Envanteri\n\n")
    f.write(header)
    
    f.write("## Generator / Sequence Listesi\n\n")
    f.write("| # | Generator Adı | Mevcut Değer |\n")
    f.write("|---|--------------|---------------|\n")
    for i, gen in enumerate(generators, 1):
        f.write(f"| {i} | `{gen['name']}` | {gen['current_value']} |\n")
    f.write("\n")
    
    f.write("## Trigger Listesi\n\n")
    if triggers:
        # Trigger type açıklamaları
        trigger_type_map = {
            1: 'BEFORE INSERT',
            2: 'AFTER INSERT',
            3: 'BEFORE UPDATE',
            4: 'AFTER UPDATE',
            5: 'BEFORE DELETE',
            6: 'AFTER DELETE',
        }
        
        for trig in triggers:
            trig_type = trigger_type_map.get(trig['type'], f"TYPE {trig['type']}")
            status = "🔴 İNAKTİF" if trig['inactive'] else "🟢 AKTİF"
            
            f.write(f"### {trig['name']}\n\n")
            f.write(f"- **Tablo:** `{trig['table']}`\n")
            f.write(f"- **Tip:** {trig_type}\n")
            f.write(f"- **Sıra:** {trig['sequence']}\n")
            f.write(f"- **Durum:** {status}\n\n")
            
            if trig['source']:
                f.write(f"**Kaynak Kodu:**\n```sql\n{trig['source']}\n```\n\n")
            else:
                f.write("**Kaynak Kodu:** Okunamadı veya boş.\n\n")
            
            f.write("---\n\n")
    else:
        f.write("Kullanıcı tanımlı trigger bulunamadı.\n\n")
    
    # Stored Procedures
    f.write("## Stored Procedure Listesi\n\n")
    f.write("| # | Procedure Adı | Input Param | Output Param |\n")
    f.write("|---|--------------|-------------|---------------|\n")
    for i, proc in enumerate(procedures, 1):
        f.write(f"| {i} | `{proc['name']}` | {proc['inputs']} | {proc['outputs']} |\n")
    f.write("\n")
    
    for proc in procedures:
        f.write(f"### {proc['name']}\n\n")
        
        params = sp_params.get(proc['name'], [])
        if params:
            f.write("**Parametreler:**\n")
            for p in params:
                f.write(f"- {p['type']}: `{p['name']}`\n")
            f.write("\n")
        
        if proc['source']:
            f.write(f"**Kaynak Kodu:**\n```sql\n{proc['source']}\n```\n\n")
        else:
            f.write("**Kaynak Kodu:** Okunamadı veya boş.\n\n")
        f.write("---\n\n")

print("  05-generator-ve-trigger-envanteri.md [OK]")

# ===== 06-yazma-islemi-risk-notu.md =====
print("[6/7] 06-yazma-islemi-risk-notu.md oluşturuluyor...")
with open(os.path.join(OUTPUT_DIR, "06-yazma-islemi-risk-notu.md"), "w", encoding="utf-8") as f:
    f.write("# Wolvox Firebird Veritabanı — Yazma İşlemi Risk ve Yöntem Notu\n\n")
    f.write(header)
    
    f.write("> ⚠️ **ÖNEMLİ UYARI:** Bu dokümandaki tüm çıkarımlar, trigger ve FK analizine ")
    f.write("dayanmaktadır. Gerçek Wolvox arayüzünden manuel bir kayıt eklenip, ")
    f.write("before-after veri karşılaştırması yapılarak doğrulanması **ZORUNLUDUR**. ")
    f.write("Wolvox, uygulama katmanında ek iş mantığı yürütüyor olabilir.\n\n")
    
    for category, analysis in write_analysis.items():
        f.write(f"## {category} Tabloları — Yazma Analizi\n\n")
        
        for tbl, info in sorted(analysis.items()):
            f.write(f"### {tbl}\n\n")
            f.write(f"- **Toplam Kolon:** {info['total_columns']}\n")
            f.write(f"- **Mevcut Satır:** {info['row_count']}\n\n")
            
            if info['required_columns']:
                f.write("**Zorunlu Alanlar (NOT NULL, Default'suz):**\n\n")
                f.write("| Kolon | Tip | Default |\n")
                f.write("|-------|-----|--------|\n")
                for col in info['required_columns']:
                    default = col['default'] if col['default'] else "YOK"
                    default = default.replace("|", "\\|").replace("\n", " ")
                    f.write(f"| `{col['name']}` | {col['type']} | {default} |\n")
                f.write("\n")
            
            if info['related_triggers']:
                f.write("**İlişkili Trigger'lar:**\n")
                for t in info['related_triggers']:
                    f.write(f"- `{t['name']}` (Tip: {t['type']})\n")
                f.write("\n")
            
            if info['related_generators']:
                f.write("**Muhtemel Generator'lar:**\n")
                for g in info['related_generators']:
                    f.write(f"- `{g['name']}` (Mevcut değer: {g['current_value']})\n")
                f.write("\n")
            
            if info['referenced_fks']:
                f.write("**Bu Tablonun Referans Ettiği (FK ile) Tablolar:**\n")
                for fk in info['referenced_fks']:
                    f.write(f"- `{fk['fk_column']}` → `{fk['ref_table']}.{fk['ref_column']}`\n")
                f.write("\n")
            
            if info['referencing_fks']:
                f.write("**Bu Tabloya Referans Veren Tablolar:**\n")
                for fk in info['referencing_fks']:
                    f.write(f"- `{fk['fk_table']}.{fk['fk_column']}` → bu tablo\n")
                f.write("\n")
            
            f.write("---\n\n")
    
    f.write("## Doğrulama Adımları (Manuel)\n\n")
    f.write("Aşağıdaki adımlar, yukarıdaki analizin doğrulanması için **gereklidir**:\n\n")
    f.write("1. Wolvox arayüzünden test veritabanında bir **test stok kartı** oluşturun.\n")
    f.write("2. İşlemden önce ve sonra ilgili tablolardan `SELECT COUNT(*)` çalıştırın.\n")
    f.write("3. Hangi tablolara kaç satır eklendiğini karşılaştırın.\n")
    f.write("4. Generator değerlerinin değişimini kontrol edin:\n")
    f.write("   ```sql\n")
    for gen in generators:
        f.write(f"   SELECT GEN_ID({gen['name']}, 0) FROM RDB$DATABASE;\n")
    f.write("   ```\n")
    f.write("5. Aynı adımları **cari kart ekleme** için de tekrarlayın.\n")
    f.write("6. Sonuçları bu dokümana ekleyin veya AI ajanına geri bildirin.\n\n")

print("  06-yazma-islemi-risk-notu.md [OK]")

# ===== 07-acik-sorular.md =====
print("[7/7] 07-acik-sorular.md oluşturuluyor...")
with open(os.path.join(OUTPUT_DIR, "07-acik-sorular.md"), "w", encoding="utf-8") as f:
    f.write("# Wolvox Firebird Veritabanı — Açık Sorular ve Doğrulanması Gerekenler\n\n")
    f.write(header)
    
    f.write("## Genel Açık Sorular\n\n")
    
    # PK'sı olmayan tablolar
    tables_without_pk = [t for t in all_tables if t not in primary_keys]
    if tables_without_pk:
        f.write(f"### 1. Primary Key Tanımlı Olmayan Tablolar ({len(tables_without_pk)} adet)\n\n")
        f.write("Aşağıdaki tablolarda tanımlı PK bulunamadı. Bu, Wolvox'un PK yerine ")
        f.write("unique index veya uygulama katmanı mantığı kullanıyor olabileceğini gösterir:\n\n")
        for t in sorted(tables_without_pk):
            f.write(f"- `{t}`\n")
        f.write("\n")
    
    # FK'si az — uygulama katmanı referansları
    if len(foreign_keys) < 20:
        f.write(f"### 2. Az Sayıda Foreign Key ({len(foreign_keys)} adet)\n\n")
        f.write("421 tabloluk bir veritabanında sadece {0} FK ilişkisi bulunması, ".format(len(foreign_keys)))
        f.write("Wolvox'un tablo ilişkilerini büyük ölçüde **uygulama katmanında** ")
        f.write("(Delphi/C++ kodu veya trigger'larla) yönettiğini güçlü şekilde gösterir.\n\n")
        f.write("**Risk:** Harici bir uygulamadan yazma yapılırken, FK constraint'leri ")
        f.write("eksik olduğundan, yanlış veri girişini veritabanı engellemeyecektir. ")
        f.write("Uygulama katmanında ek doğrulama yapılmalıdır.\n\n")
    
    # Sınıflandırılamayan tablolar
    if uncategorized:
        f.write(f"### 3. Sınıflandırılamayan Tablolar ({len(uncategorized)} adet)\n\n")
        f.write("Aşağıdaki tabloların iş alanı, isimlerinden anlaşılamadı. ")
        f.write("Manuel inceleme gereklidir:\n\n")
        for t in sorted(uncategorized):
            cols = table_columns.get(t, [])
            f.write(f"- `{t}` ({len(cols)} kolon)\n")
        f.write("\n")
    
    # Trigger kaynak kodu okunamayanlar
    triggers_no_source = [t for t in triggers if not t['source']]
    if triggers_no_source:
        f.write(f"### 4. Kaynak Kodu Okunamayan Trigger'lar ({len(triggers_no_source)} adet)\n\n")
        for t in triggers_no_source:
            f.write(f"- `{t['name']}` (Tablo: `{t['table']}`)\n")
        f.write("\n")
    
    # SP kaynak kodu okunamayanlar
    procs_no_source = [p for p in procedures if not p['source']]
    if procs_no_source:
        f.write(f"### 5. Kaynak Kodu Okunamayan Stored Procedure'ler ({len(procs_no_source)} adet)\n\n")
        for p in procs_no_source:
            f.write(f"- `{p['name']}`\n")
        f.write("\n")
    
    # Referans tablosu verileri okunamayanlar
    ref_errors = {t: d for t, d in reference_tables_data.items() if 'error' in d}
    if ref_errors:
        f.write(f"### 6. Verisi Okunamayan Referans Tabloları ({len(ref_errors)} adet)\n\n")
        for t, d in sorted(ref_errors.items()):
            f.write(f"- `{t}`: {d['error']}\n")
        f.write("\n")
    
    f.write("## Doğrulanması Gereken Konular\n\n")
    f.write("1. **Yazma işlemleri sırası:** Faz 5'teki stok/cari ekleme analizi, ")
    f.write("Wolvox arayüzünden gerçek bir kayıt eklenerek doğrulanmalıdır.\n")
    f.write("2. **Trigger davranışları:** Trigger'ların gerçekte hangi ek işlemleri ")
    f.write("yaptığı, test kayıtları ile doğrulanmalıdır.\n")
    f.write("3. **Uygulama katmanı mantığı:** Wolvox'un Delphi/C++ kodunda yapılan ")
    f.write("ek iş mantığı (varsayılan değerler, hesaplamalar, validasyonlar) ")
    f.write("bu analizle tespit edilemez.\n")
    f.write("4. **Kolon anlamları:** Bazı kolon isimleri Türkçe kısaltmalarla ")
    f.write("yazıldığından, gerçek anlamları Wolvox arayüzündeki etiketlerle ")
    f.write("karşılaştırılarak doğrulanmalıdır.\n")
    f.write("5. **Çoklu veritabanı yapısı:** Wolvox'un farklı yıllar veya şirketler ")
    f.write("için ayrı veritabanı dosyaları (.fdb) kullanıp kullanmadığı kontrol edilmelidir ")
    f.write("(yol: `DEMOWOLVOX\\2026\\WOLVOX.fdb` — yıl bazlı yapı olabilir).\n")

print("  07-acik-sorular.md [OK]")

print("\n" + "=" * 60)
print("TÜM ÇIKTI DOSYALARI OLUŞTURULDU!")
print(f"Çıktı klasörü: {OUTPUT_DIR}")
print("=" * 60)
