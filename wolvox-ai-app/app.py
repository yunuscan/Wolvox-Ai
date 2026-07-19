# -*- coding: utf-8 -*-
"""
Wolvox AI Stok Yönetimi - Flask Backend
Groq API + Firebird veritabanı entegrasyonu (Akıllı Tahmin, Çoklu Eylem, Grup Silme & Stok Adıyla Silme)
"""
from flask import Flask, render_template, request, jsonify
from groq import Groq
import fdb
import json
import re
import os
from datetime import datetime
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)

# ===== YAPILANDIRMA =====
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

FB_CLIENT = r"C:\Users\yunuscan\Desktop\WolvoxDBSeması\fb25_x64\bin\fbclient.dll"
DB_PATH = r"C:\AKINSOFT\Wolvox9\Database_FB\DEMOWOLVOX\2026\WOLVOX.fdb"
DB_HOST = "localhost"
DB_PORT = 3050
DB_USER = "SYSDBA"
DB_PASS = "masterkey"
DB_CHARSET = "WIN1254"

groq_client = Groq(api_key=GROQ_API_KEY)


def get_db():
    """Firebird veritabanı bağlantısı oluştur"""
    return fdb.connect(
        host=DB_HOST, port=DB_PORT, database=DB_PATH,
        user=DB_USER, password=DB_PASS,
        fb_library_name=FB_CLIENT, charset=DB_CHARSET
    )


def get_db_definitions():
    """Veritabanındaki mevcut stok gruplarını ve birim tanımlarını getir"""
    groups = []
    units = []
    try:
        con = get_db()
        cur = con.cursor()
        
        # Grupları çek
        cur.execute("SELECT DISTINCT GRUP_ADI FROM GRUP WHERE MODUL = 'STOK' AND GRUP_ADI IS NOT NULL ORDER BY GRUP_ADI")
        groups = [row[0].strip() for row in cur.fetchall()]
        
        # Birimleri çek
        cur.execute("SELECT DISTINCT BIRIMI FROM STOK_BIRIMLERI WHERE BIRIMI IS NOT NULL ORDER BY BIRIMI")
        units = [row[0].strip() for row in cur.fetchall()]
        
        cur.close()
        con.close()
    except Exception as e:
        print(f"Tanımlar alınırken hata oluştu: {e}")
    
    return groups, units


def build_system_prompt():
    """Dinamik olarak veritabanı durumuna göre AI system prompt'u oluşturur (Grup Silme ve Stok Adıyla Silme Destekli)"""
    groups, units = get_db_definitions()
    
    groups_str = ", ".join([f"'{g}'" for g in groups]) if groups else "'Genel'"
    units_str = ", ".join([f"'{u}'" for u in units]) if units else "'ADET', 'KG'"

    prompt = f"""Sen bir Wolvox ERP stok yönetim asistanısın. Kullanıcı sana doğal dilde bir veya birden fazla talimat verecek.
Görevin, kullanıcının mesajındaki TÜM talimatları analiz edip bir eylem listesi (actions) olarak JSON formatında döndürmektir.

VERİTABANINDA MEVCUT TANIMLAR:
- Tanımlı Stok Grupları: [{groups_str}]
- Tanımlı Birimler: [{units_str}]

DESTEKLENEN EYLEMLER VE FORMATLARI:

1. Stok Ekleme (stok_ekle):
   - Ürün adından KDV, grup ve birimi akıllıca tahmin et (kullanıcı belirtmemişse).
   - KDV tahminleri: Gıda ürünlerinde %10, temizlik/hijyen/elektronik ürünlerinde %20.
   - Birim tahminleri: KG, ADET, Litre vb. veritabanında tanımlı olanlardan seç.
   - Format: {{"action":"stok_ekle","stok_adi":"...","grubu":"...","birimi":"...","kdv_orani":0,"satis_fiyati_1":0,"alis_fiyati_1":0,"aciklama":"..."}}

2. Grup Ekleme (grup_ekle):
   - Kullanıcı yeni bir grup tanımlamak istediğinde tetiklenir (örn: "Şarküteri grubu oluştur", "Yeni grup ekle: Manav").
   - Format: {{"action":"grup_ekle","grup_adi":"..."}}

3. Grup Silme (grup_sil):
   - Kullanıcı mevcut bir grubu silmek istediğinde tetiklenir (örn: "Şarküteri grubunu sil", "Manav grubunu iptal et").
   - Format: {{"action":"grup_sil","grup_adi":"..."}}

4. Stok Silme (stok_sil):
   - Kullanıcı belirli bir stok kodunu veya stok ADINI silmek istediğinde tetiklenir (örn: "ST00001 kodlu ürünü sil", "Muz stoğunu sil", "Nohut ürününü sil").
   - Kullanıcı kodu belirtmediyse sadece stok_adi alanını doldur.
   - Format: {{"action":"stok_sil","stok_kodu":"...","stok_adi":"..."}}

5. Stokları Listeleme (listele):
   - Kullanıcı stokları listelemek istediğinde tetiklenir.
   - Format: {{"action":"listele"}}

ÇOKLU TALİMAT YÖNETİMİ:
Kullanıcı tek bir mesajda birden fazla istek yapabilir (örn: "Şarküteri grubunu sil, Manav grubu oluştur ve içine Armut ekle").
Bu durumda tüm eylemleri sırasıyla "actions" dizisine ekle.

DÖNECEK JSON FORMATI (SADECE JSON DÖN, BAŞKA METİN EKLEME):
{{
  "actions": [
    {{ "action": "grup_sil", "grup_adi": "Şarküteri" }},
    {{ "action": "grup_ekle", "grup_adi": "Manav" }},
    {{ "action": "stok_ekle", "stok_adi": "Armut", "grubu": "Manav", "birimi": "KG", "kdv_orani": 10, "satis_fiyati_1": 0, "alis_fiyati_1": 0, "aciklama": "" }}
  ]
}}

Eğer eylem yoksa ve sadece soru soruluyorsa:
{{
  "actions": [
    {{ "action": "soru", "cevap": "Sorunun cevabı buraya gelecek." }}
  ]
}}
"""
    return prompt


def add_group_db(grup_adi):
    """Veritabanına yeni grup ekle"""
    grup_adi = grup_adi.strip()
    if not grup_adi:
        return {'success': False, 'error': 'Grup adı boş olamaz.'}

    con = get_db()
    cur = con.cursor()
    try:
        # Case-insensitive varlık kontrolü
        cur.execute("SELECT BLKODU FROM GRUP WHERE UPPER(GRUP_ADI) = UPPER(?) AND MODUL = 'STOK'", (grup_adi,))
        row = cur.fetchone()
        if row:
            return {'success': True, 'msg': f"'{grup_adi}' grubu zaten mevcut.", 'blkodu': row[0]}

        cur.execute("SELECT GEN_ID(GRUP_GEN, 1) FROM RDB$DATABASE")
        grup_blkodu = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO GRUP (BLKODU, GRUP_ADI, MODUL, WEBDE_GORUNSUN)
            VALUES (?, ?, 'STOK', 1)
        """, (grup_blkodu, grup_adi))
        con.commit()
        return {'success': True, 'msg': f"✅ '{grup_adi}' grubu başarıyla oluşturuldu.", 'blkodu': grup_blkodu}
    except Exception as e:
        con.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        cur.close()
        con.close()


def delete_group_db(grup_adi):
    """Veritabanından grubu siler"""
    grup_adi = grup_adi.strip()
    if not grup_adi:
        return {'success': False, 'error': 'Grup adı belirtilmedi.'}

    con = get_db()
    cur = con.cursor()
    try:
        cur.execute("SELECT BLKODU FROM GRUP WHERE UPPER(GRUP_ADI) = UPPER(?) AND MODUL = 'STOK'", (grup_adi,))
        row = cur.fetchone()
        if not row:
            return {'success': False, 'error': f"Silinmek istenen grup bulunamadı ({grup_adi})."}

        blkodu = row[0]
        cur.execute("DELETE FROM GRUP WHERE BLKODU = ?", (blkodu,))
        con.commit()
        return {'success': True, 'msg': f"🗑️ '{grup_adi}' grubu başarıyla silindi."}
    except Exception as e:
        con.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        cur.close()
        con.close()


def add_stock_db(stok_adi, grubu, birimi, kdv_orani, satis_fiyati_1, alis_fiyati_1, aciklama=''):
    """Veritabanına yeni stok kartı ekle"""
    con = get_db()
    cur = con.cursor()
    now = datetime.now()

    try:
        # 1. GRUP KONTROL / OLUŞTUR (Case-insensitive)
        cur.execute("SELECT BLKODU, GRUP_ADI FROM GRUP WHERE UPPER(GRUP_ADI) = UPPER(?) AND MODUL = 'STOK'", (grubu.strip(),))
        row = cur.fetchone()
        if row:
            grup_adi = row[1].strip()
        else:
            # Grup yoksa oluştur
            cur.execute("SELECT GEN_ID(GRUP_GEN, 1) FROM RDB$DATABASE")
            grup_blkodu = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO GRUP (BLKODU, GRUP_ADI, MODUL, WEBDE_GORUNSUN)
                VALUES (?, ?, 'STOK', 1)
            """, (grup_blkodu, grubu.strip()))
            grup_adi = grubu.strip()

        # 2. BİRİM KONTROL / EŞLEŞTİRME
        cur.execute("SELECT BIRIMI FROM STOK_BIRIMLERI")
        db_units = [r[0].strip() for r in cur.fetchall()]
        
        matched_unit = "ADET"
        birimi_upper = birimi.strip().upper()
        
        for u in db_units:
            u_upper = u.upper()
            if birimi_upper == u_upper:
                matched_unit = u
                break
            elif birimi_upper in u_upper or u_upper in birimi_upper:
                matched_unit = u
        
        if birimi_upper in ["KİLO", "KİLOGRAM", "KG"]:
            matched_unit = next((u for u in db_units if u.upper() == 'KG'), 'KG')
        elif birimi_upper in ["TANE", "ADET", "PIECE", "PCS"]:
            matched_unit = next((u for u in db_units if u.upper() == 'ADET'), 'ADET')
        elif birimi_upper in ["LİTRE", "LITER", "L"]:
            matched_unit = next((u for u in db_units if u.upper() in ['LİTRE', 'LITRE', 'L']), 'Litre')

        # 3. Stok ID al
        cur.execute("SELECT GEN_ID(STOK_GEN, 1) FROM RDB$DATABASE")
        stok_blkodu = cur.fetchone()[0]

        # 4. Stok kodu sayacı
        cur.execute("SELECT GEN_ID(SAYAC_ST_12_GEN, 1) FROM RDB$DATABASE")
        sayac = cur.fetchone()[0]
        stok_kodu = f"ST{sayac:05d}"

        # 5. STOK INSERT
        cur.execute("""
            INSERT INTO STOK (
                BLKODU, STOKKODU, STOK_ADI, BIRIMI, KDV_ORANI, KDV_ORANI_ALIS,
                KDV_ORANI_SATIS_TPT, KAYIT_TARIHI, GRUBU, KAYDEDEN, AKTIF,
                DEPO_ADI, SIPARIS_EKLE, SIPARIS_MINIMUM_MIKTAR, SIPARIS_EKLENECEK_MIKTAR,
                DOVIZ_KULLAN, BAKIYE_UYARI, ANA_STOK, WEBDE_GORUNSUN, SIPARIS_DURUMU,
                ALIS_ISKONTO_KULLAN, SATIS_ISKONTO_KULLAN, STISK1_KULLAN, STISK2_KULLAN,
                STISK3_KULLAN, ALISISK1_KULLAN, ALISISK2_KULLAN, ALISISK3_KULLAN,
                SERINO_KULLAN, KDV_85_KULLAN, SERILOT_MALIYET_ESLESTIR, LOT_PARCALANABILIR,
                ENTRYKDVDEPARTMAN, MUH_ALIS, MUH_SATIS_YI, MUH_SATIS_YD,
                MUH_IADE_YI, MUH_IADE_YD, MUH_MALIYET_HESABI, BIRIMLER, BARKOD_TIPI,
                ACIKLAMA1
            ) VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?
            )
        """, (
            stok_blkodu, stok_kodu, stok_adi, matched_unit, kdv_orani, kdv_orani,
            kdv_orani, now, grup_adi, 'AI_ASSISTANT', 1,
            '1', 1, 0, 0,
            0, 0, 0, 0, 1,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 1, 0,
            1, '153', '600', '601',
            '610', '610', '621', 'V01', 1,
            aciklama
        ))

        # 6. Fiyat kayıtları (4 alış + 4 satış)
        fiyat_kayitlari = [
            ('ALIŞ FİYATI -1',  1, 1, alis_fiyati_1),
            ('ALIŞ FİYATI -2',  1, 2, 0.0),
            ('ALIŞ FİYATI -3',  1, 3, 0.0),
            ('ALIŞ FİYATI -4',  1, 4, 0.0),
            ('SATIŞ FİYATI -1', 2, 1, satis_fiyati_1),
            ('SATIŞ FİYATI -2', 2, 2, 0.0),
            ('SATIŞ FİYATI -3', 2, 3, 0.0),
            ('SATIŞ FİYATI -4', 2, 4, 0.0),
        ]

        for tanimi, alis_satis, fiyat_no, fiyati in fiyat_kayitlari:
            cur.execute("SELECT GEN_ID(STOK_FIYAT_GEN, 1) FROM RDB$DATABASE")
            fiyat_blkodu = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO STOK_FIYAT (
                    BLKODU, BLSTKODU, TANIMI, HESAP, FIYATI,
                    ALIS_SATIS, KPB_MI, FIYAT_NO, FIYAT_DEG_TARIHI
                ) VALUES (?, ?, ?, 'TL', ?, ?, 1, ?, ?)
            """, (fiyat_blkodu, stok_blkodu, tanimi, fiyati, alis_satis, fiyat_no, now))

        con.commit()
        return {
            'success': True,
            'stok_kodu': stok_kodu,
            'stok_adi': stok_adi,
            'blkodu': stok_blkodu,
            'grubu': grup_adi,
            'birimi': matched_unit,
            'kdv_orani': kdv_orani,
            'satis_fiyati_1': satis_fiyati_1,
            'alis_fiyati_1': alis_fiyati_1
        }
    except Exception as e:
        con.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        cur.close()
        con.close()


def delete_stock_db(stok_kodu=None, stok_adi=None):
    """Veritabanından stok kartını ve fiyatlarını siler (Koda veya Ada göre)"""
    if not stok_kodu and not stok_adi:
        return {'success': False, 'error': 'Silinecek stok belirlenemedi.'}

    con = get_db()
    cur = con.cursor()
    try:
        # Önce stoğu bul
        if stok_kodu and stok_kodu.strip():
            cur.execute("SELECT BLKODU, STOK_ADI, STOKKODU FROM STOK WHERE UPPER(STOKKODU) = UPPER(?)", (stok_kodu.strip(),))
        else:
            cur.execute("SELECT BLKODU, STOK_ADI, STOKKODU FROM STOK WHERE UPPER(STOK_ADI) = UPPER(?)", (stok_adi.strip(),))
        
        row = cur.fetchone()
        
        # Eğer tam ad eşleşmediyse benzerlik (LIKE) ile ara
        if not row and stok_adi:
            cur.execute("SELECT BLKODU, STOK_ADI, STOKKODU FROM STOK WHERE UPPER(STOK_ADI) LIKE UPPER(?)", (f"%{stok_adi.strip()}%",))
            row = cur.fetchone()
            
        if not row:
            return {'success': False, 'error': f"Silinmek istenen stok bulunamadı ({stok_kodu or stok_adi})."}

        blkodu = row[0]
        deleted_name = row[1].strip()
        deleted_code = row[2].strip()

        # Önce fiyat kayıtlarını sil
        cur.execute("DELETE FROM STOK_FIYAT WHERE BLSTKODU = ?", (blkodu,))
        
        # Sonra stok kaydını sil
        cur.execute("DELETE FROM STOK WHERE BLKODU = ?", (blkodu,))
        
        con.commit()
        return {'success': True, 'stok_adi': deleted_name, 'stok_kodu': deleted_code}
    except Exception as e:
        con.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        cur.close()
        con.close()


def get_stocks():
    """Mevcut stok listesini getir"""
    con = get_db()
    cur = con.cursor()
    cur.execute("""
        SELECT s.BLKODU, s.STOKKODU, s.STOK_ADI, s.GRUBU, s.BIRIMI,
               s.KDV_ORANI, s.AKTIF, s.KAYIT_TARIHI
        FROM STOK s
        ORDER BY s.BLKODU DESC
    """)
    stocks = []
    for row in cur.fetchall():
        stok_blkodu = row[0]
        cur2 = con.cursor()
        cur2.execute("""
            SELECT TANIMI, FIYATI, ALIS_SATIS, FIYAT_NO
            FROM STOK_FIYAT WHERE BLSTKODU = ?
            ORDER BY ALIS_SATIS, FIYAT_NO
        """, (stok_blkodu,))
        fiyatlar = []
        for fr in cur2.fetchall():
            fiyatlar.append({
                'tanimi': fr[0].strip() if fr[0] else '',
                'fiyati': float(fr[1]) if fr[1] else 0,
                'alis_satis': fr[2],
                'fiyat_no': fr[3]
            })
        cur2.close()

        stocks.append({
            'blkodu': row[0],
            'stokkodu': row[1].strip() if row[1] else '',
            'stok_adi': row[2].strip() if row[2] else '',
            'grubu': row[3].strip() if row[3] else '',
            'birimi': row[4].strip() if row[4] else '',
            'kdv_orani': float(row[5]) if row[5] else 0,
            'aktif': row[6],
            'kayit_tarihi': row[7].strftime('%d.%m.%Y %H:%M') if row[7] else '',
            'fiyatlar': fiyatlar
        })
    cur.close()
    con.close()
    return stocks


def get_existing_groups():
    """Mevcut stok gruplarını getir"""
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT GRUP_ADI FROM GRUP WHERE MODUL = 'STOK' ORDER BY GRUP_ADI")
    groups = [row[0].strip() for row in cur.fetchall()]
    cur.close()
    con.close()
    return groups


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Mesaj boş'}), 400

    try:
        # Dinamik System Prompt oluştur
        system_prompt = build_system_prompt()

        # Groq API çağrısı
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1,
            max_tokens=500,
        )

        ai_response = response.choices[0].message.content.strip()
        tokens_used = response.usage.total_tokens if response.usage else 0

        # JSON parse
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            ai_json = json.loads(json_match.group())
        else:
            return jsonify({
                'type': 'error',
                'message': f'AI yanıtı parse edilemedi: {ai_response}',
                'tokens': tokens_used
            })

        actions = ai_json.get('actions', [])
        
        # Eğer sadece soru sorulduysa
        if len(actions) == 1 and actions[0].get('action') == 'soru':
            return jsonify({
                'type': 'answer',
                'message': actions[0].get('cevap', 'Anlayamadım.'),
                'tokens': tokens_used
            })

        # Eğer listeleme varsa
        if any(a.get('action') == 'listele' for a in actions):
            stocks = get_stocks()
            return jsonify({
                'type': 'list',
                'data': stocks,
                'tokens': tokens_used,
                'message': f'📦 Toplam {len(stocks)} stok kartı bulundu.'
            })

        # Önizleme formatında eylemleri dönelim
        return jsonify({
            'type': 'preview',
            'actions': actions,
            'tokens': tokens_used,
            'message': f"⚙️ **{len(actions)}** adet işlem planlandı. Onaylıyor musun?"
        })

    except Exception as e:
        return jsonify({'type': 'error', 'message': str(e)}), 500


@app.route('/api/confirm', methods=['POST'])
def confirm_actions():
    data = request.json
    actions = data.get('actions', [])
    
    if not actions:
        return jsonify({'error': 'İşlem bulunamadı'}), 400

    results = []
    success_count = 0

    for idx, act in enumerate(actions, 1):
        action_type = act.get('action')
        
        if action_type == 'grup_ekle':
            grup_adi = act.get('grup_adi')
            res = add_group_db(grup_adi)
            if res['success']:
                success_count += 1
                results.append(f"{idx}. {res['msg']}")
            else:
                results.append(f"{idx}. ❌ Grup Ekleme Hatası ({grup_adi}): {res['error']}")

        elif action_type == 'grup_sil':
            grup_adi = act.get('grup_adi')
            res = delete_group_db(grup_adi)
            if res['success']:
                success_count += 1
                results.append(f"{idx}. {res['msg']}")
            else:
                results.append(f"{idx}. ❌ Grup Silme Hatası ({grup_adi}): {res['error']}")

        elif action_type == 'stok_ekle':
            res = add_stock_db(
                stok_adi=act.get('stok_adi', 'Bilinmeyen'),
                grubu=act.get('grubu', 'Genel'),
                birimi=act.get('birimi', 'ADET'),
                kdv_orani=float(act.get('kdv_orani', 20)),
                satis_fiyati_1=float(act.get('satis_fiyati_1', 0)),
                alis_fiyati_1=float(act.get('alis_fiyati_1', 0)),
                aciklama=act.get('aciklama', '')
            )
            if res['success']:
                success_count += 1
                results.append(f"{idx}. ✅ **{res['stok_adi']}** eklendi! (Kod: `{res['stok_kodu']}` - Fiyat: {res['satis_fiyati_1']:.2f} TL)")
            else:
                results.append(f"{idx}. ❌ Stok Ekleme Hatası ({act.get('stok_adi')}): {res['error']}")

        elif action_type == 'stok_sil':
            stok_kodu = act.get('stok_kodu')
            stok_adi = act.get('stok_adi')
            res = delete_stock_db(stok_kodu=stok_kodu, stok_adi=stok_adi)
            if res['success']:
                success_count += 1
                results.append(f"{idx}. 🗑️ **{res['stok_adi']}** (Kod: `{res['stok_kodu']}`) başarıyla silindi.")
            else:
                results.append(f"{idx}. ❌ Stok Silme Hatası ({stok_kodu or stok_adi}): {res['error']}")

    summary_msg = f"📊 **{success_count} / {len(actions)}** işlem başarıyla tamamlandı.\n\n" + "\n".join(results)
    
    return jsonify({
        'type': 'success',
        'message': summary_msg
    })


@app.route('/api/stocks', methods=['GET'])
def list_stocks():
    try:
        stocks = get_stocks()
        return jsonify({'stocks': stocks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/groups', methods=['GET'])
def list_groups():
    try:
        groups = get_existing_groups()
        return jsonify({'groups': groups})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("  Wolvox AI Akıllı Çoklu Eylem Yönetimi Başlatıldı")
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
