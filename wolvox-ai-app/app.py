# -*- coding: utf-8 -*-
"""
Wolvox AI Stok Yönetimi - Flask Backend
Groq API + Firebird veritabanı entegrasyonu
"""
from flask import Flask, render_template, request, jsonify
from groq import Groq
import fdb
import json
import re
from datetime import datetime

import os
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

# ===== SYSTEM PROMPT =====
SYSTEM_PROMPT = """Sen bir Wolvox ERP stok yönetim asistanısın. Kullanıcı sana doğal dilde stok ekleme talimatı verecek.
Görevin, kullanıcının mesajından stok bilgilerini çıkarıp JSON formatında döndürmek.

KURALLAR:
1. Kullanıcı mesajından stok bilgilerini çıkar.
2. Eksik bilgileri varsayılan değerlerle doldur.
3. SADECE aşağıdaki JSON formatında yanıt ver, başka hiçbir metin ekleme.
4. Türkçe karakterleri doğru kullan.

VARSAYILAN DEĞERLER:
- birimi: "ADET" (kullanıcı belirtmezse)
- kdv_orani: 20 (kullanıcı belirtmezse)
- satis_fiyati_1: 0 (kullanıcı belirtmezse)
- alis_fiyati_1: 0 (kullanıcı belirtmezse)
- grubu: "Genel" (kullanıcı belirtmezse)

JSON FORMATI:
{"action":"stok_ekle","stok_adi":"...","grubu":"...","birimi":"...","kdv_orani":0,"satis_fiyati_1":0,"alis_fiyati_1":0,"aciklama":"..."}

Eğer kullanıcı stok ekleme değil, stok listeleme veya başka bir şey istiyorsa:
{"action":"listele"} veya {"action":"soru","cevap":"..."}

ÖRNEKLER:
- "Kuru fasulye ekle 50 liradan alıp 75 liradan satacağım grubu bakliyat kdv %10 birimi KG"
  → {"action":"stok_ekle","stok_adi":"Kuru Fasulye","grubu":"Bakliyat","birimi":"KG","kdv_orani":10,"satis_fiyati_1":75,"alis_fiyati_1":50,"aciklama":""}

- "Çamaşır suyu ekle"
  → {"action":"stok_ekle","stok_adi":"Çamaşır Suyu","grubu":"Genel","birimi":"ADET","kdv_orani":20,"satis_fiyati_1":0,"alis_fiyati_1":0,"aciklama":""}

- "Stokları listele"
  → {"action":"listele"}
"""


def get_db():
    """Firebird veritabanı bağlantısı oluştur"""
    return fdb.connect(
        host=DB_HOST, port=DB_PORT, database=DB_PATH,
        user=DB_USER, password=DB_PASS,
        fb_library_name=FB_CLIENT, charset=DB_CHARSET
    )


def get_existing_groups():
    """Mevcut stok gruplarını getir"""
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT GRUP_ADI FROM GRUP WHERE MODUL = 'STOK' ORDER BY GRUP_ADI")
    groups = [row[0].strip() for row in cur.fetchall()]
    cur.close()
    con.close()
    return groups


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
        # Fiyatları çek
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


def add_stock(stok_adi, grubu, birimi, kdv_orani, satis_fiyati_1, alis_fiyati_1, aciklama=''):
    """Veritabanına yeni stok kartı ekle"""
    con = get_db()
    cur = con.cursor()
    now = datetime.now()

    try:
        # 1. Grup kontrol / oluştur
        cur.execute("SELECT BLKODU FROM GRUP WHERE GRUP_ADI = ? AND MODUL = 'STOK'", (grubu,))
        row = cur.fetchone()
        if not row:
            cur.execute("SELECT GEN_ID(GRUP_GEN, 1) FROM RDB$DATABASE")
            grup_blkodu = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO GRUP (BLKODU, GRUP_ADI, MODUL, WEBDE_GORUNSUN)
                VALUES (?, ?, 'STOK', 1)
            """, (grup_blkodu, grubu))

        # 2. Stok ID al
        cur.execute("SELECT GEN_ID(STOK_GEN, 1) FROM RDB$DATABASE")
        stok_blkodu = cur.fetchone()[0]

        # 3. Stok kodu sayacı
        cur.execute("SELECT GEN_ID(SAYAC_ST_12_GEN, 1) FROM RDB$DATABASE")
        sayac = cur.fetchone()[0]
        stok_kodu = f"ST{sayac:05d}"

        # 4. STOK INSERT
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
            stok_blkodu, stok_kodu, stok_adi, birimi, kdv_orani, kdv_orani,
            kdv_orani, now, grubu, 'AI_ASSISTANT', 1,
            '1', 1, 0, 0,
            0, 0, 0, 0, 1,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 1, 0,
            1, '153', '600', '601',
            '610', '610', '621', 'V01', 1,
            aciklama
        ))

        # 5. Fiyat kayıtları (4 alış + 4 satış)
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
            'grubu': grubu,
            'birimi': birimi,
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
        # Groq API çağrısı
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1,
            max_tokens=300,
        )

        ai_response = response.choices[0].message.content.strip()
        tokens_used = response.usage.total_tokens if response.usage else 0

        # JSON parse
        # Bazen model ```json ... ``` ile sarıyor, temizle
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            ai_json = json.loads(json_match.group())
        else:
            return jsonify({
                'type': 'error',
                'message': f'AI yanıtı parse edilemedi: {ai_response}',
                'tokens': tokens_used
            })

        action = ai_json.get('action', '')

        if action == 'stok_ekle':
            return jsonify({
                'type': 'preview',
                'data': ai_json,
                'tokens': tokens_used,
                'message': f"🛒 **{ai_json.get('stok_adi', '')}** eklenecek. Onaylıyor musun?"
            })

        elif action == 'listele':
            stocks = get_stocks()
            return jsonify({
                'type': 'list',
                'data': stocks,
                'tokens': tokens_used,
                'message': f'📦 Toplam {len(stocks)} stok kartı bulundu.'
            })

        elif action == 'soru':
            return jsonify({
                'type': 'answer',
                'message': ai_json.get('cevap', 'Anlayamadım.'),
                'tokens': tokens_used
            })

        else:
            return jsonify({
                'type': 'answer',
                'message': ai_response,
                'tokens': tokens_used
            })

    except Exception as e:
        return jsonify({'type': 'error', 'message': str(e)}), 500


@app.route('/api/confirm', methods=['POST'])
def confirm_add():
    data = request.json

    result = add_stock(
        stok_adi=data.get('stok_adi', 'Bilinmeyen'),
        grubu=data.get('grubu', 'Genel'),
        birimi=data.get('birimi', 'ADET'),
        kdv_orani=float(data.get('kdv_orani', 20)),
        satis_fiyati_1=float(data.get('satis_fiyati_1', 0)),
        alis_fiyati_1=float(data.get('alis_fiyati_1', 0)),
        aciklama=data.get('aciklama', '')
    )

    if result['success']:
        return jsonify({
            'type': 'success',
            'message': f"✅ **{result['stok_adi']}** başarıyla eklendi!\n\n"
                       f"📋 Stok Kodu: `{result['stok_kodu']}`\n"
                       f"📦 Grup: {result['grubu']}\n"
                       f"⚖️ Birim: {result['birimi']}\n"
                       f"💰 Satış: {result['satis_fiyati_1']:.2f} TL\n"
                       f"🛍️ Alış: {result['alis_fiyati_1']:.2f} TL\n"
                       f"📊 KDV: %{result['kdv_orani']:.0f}\n\n"
                       f"Wolvox'ta **Stok Tanımları > Bul** ile kontrol edebilirsin.",
            'data': result
        })
    else:
        return jsonify({
            'type': 'error',
            'message': f"❌ Hata: {result['error']}"
        }), 500


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
    print("  Wolvox AI Stok Yönetimi")
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
