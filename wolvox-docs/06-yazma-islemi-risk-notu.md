# Wolvox Firebird Veritabanı — Yazma İşlemi Risk ve Yöntem Notu

---
**Analiz Tarihi:** 2026-07-19 15:50:10  
**Firebird Sürümü:** 2.5.6 (WI-V6.3.6.27020 Firebird 2.5)  
**Veritabanı:** DEMOWOLVOX (Wolvox 9)  
**Veritabanı Yolu:** `C:\AKINSOFT\Wolvox9\Database_FB\DEMOWOLVOX\2026\WOLVOX.fdb`  
**Charset:** WIN1254  
**Not:** Bu dokümantasyon salt-okunur analiz ile oluşturulmuştur. Wolvox güncellemelerinde şema değişebilir.

---

> ⚠️ **ÖNEMLİ UYARI:** Bu dokümandaki tüm çıkarımlar, trigger ve FK analizine dayanmaktadır. Gerçek Wolvox arayüzünden manuel bir kayıt eklenip, before-after veri karşılaştırması yapılarak doğrulanması **ZORUNLUDUR**. Wolvox, uygulama katmanında ek iş mantığı yürütüyor olabilir.

## STOK Tabloları — Yazma Analizi

### ADISYONSTOKDETAY

- **Toplam Kolon:** 23
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### BARKOD_TIPI

- **Toplam Kolon:** 7
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `TIPI` | VARCHAR(2) | YOK |

---

### ITHALAT_GIRIS_STOK

- **Toplam Kolon:** 18
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### MRP_EMIRLERI_FASON_STOK

- **Toplam Kolon:** 23
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### MRP_MAKINE_STOK

- **Toplam Kolon:** 10
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### OTEL_PANSIYON_KONSEPT_STOK

- **Toplam Kolon:** 8
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### PROMOSYON_TANIM_URUN

- **Toplam Kolon:** 13
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### PTMP_CARISTOK_ENSONSATISFYT

- **Toplam Kolon:** 8
- **Mevcut Satır:** N/A

---

### PTMP_STOKHR_SATIRBAKIYE

- **Toplam Kolon:** 3
- **Mevcut Satır:** N/A

---

### PTMP_STOK_DNMRAP

- **Toplam Kolon:** 9
- **Mevcut Satır:** N/A

---

### PTMP_STOK_ENVANTER

- **Toplam Kolon:** 17
- **Mevcut Satır:** N/A

---

### PTMP_STOK_FIFO_KALANLAR

- **Toplam Kolon:** 4
- **Mevcut Satır:** N/A

---

### PTMP_STOK_ISLEM_GORMEYEN

- **Toplam Kolon:** 9
- **Mevcut Satır:** N/A

---

### PTMP_STOK_KZB

- **Toplam Kolon:** 15
- **Mevcut Satır:** N/A

---

### PTMP_STOK_KZN

- **Toplam Kolon:** 14
- **Mevcut Satır:** N/A

---

### PTMP_STOK_KZ_OZEL

- **Toplam Kolon:** 21
- **Mevcut Satır:** N/A

---

### PTMP_STOK_MKBAKIYE

- **Toplam Kolon:** 10
- **Mevcut Satır:** N/A

---

### PTMP_STOK_YETERLILIK

- **Toplam Kolon:** 10
- **Mevcut Satır:** N/A

---

### SERVIS_SOZLESME_URUN

- **Toplam Kolon:** 3
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### SERVIS_URUN

- **Toplam Kolon:** 3
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK

- **Toplam Kolon:** 117
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `STOKKODU` | VARCHAR(30) | YOK |

**Muhtemel Generator'lar:**
- `STOKHR_MALIYET_GEN` (Mevcut değer: 0)

---

### STOKDEPO_SAYIM

- **Toplam Kolon:** 12
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOKHR

- **Toplam Kolon:** 64
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `TARIHI` | TIMESTAMP | YOK |

**İlişkili Trigger'lar:**
- `STOKHR_ONINSERT` (Tip: 17)

**Muhtemel Generator'lar:**
- `STOKHR_MALIYET_GEN` (Mevcut değer: 0)

---

### STOKHR_MALIYET

- **Toplam Kolon:** 9
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `BLSTKODU` | BIGINT | YOK |
| `BLHRKODU` | BIGINT | YOK |

**İlişkili Trigger'lar:**
- `STOKHR_MALIYET_ONINSERT` (Tip: 114)

**Muhtemel Generator'lar:**
- `STOKHR_MALIYET_GEN` (Mevcut değer: 0)

---

### STOK_ALTERNATIF

- **Toplam Kolon:** 4
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_ALT_URUNLER

- **Toplam Kolon:** 8
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `BLSTKODU` | BIGINT | YOK |

---

### STOK_BARKOD

- **Toplam Kolon:** 7
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_BIRIMLERI

- **Toplam Kolon:** 4
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `BIRIMI` | VARCHAR(15) | YOK |

---

### STOK_BLOKE

- **Toplam Kolon:** 16
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_DEPO

- **Toplam Kolon:** 12
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_DETAY_HAREKET

- **Toplam Kolon:** 20
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_EK_DETAY

- **Toplam Kolon:** 16
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_ETICVARYANT

- **Toplam Kolon:** 3
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_FIYAT

- **Toplam Kolon:** 17
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

**İlişkili Trigger'lar:**
- `STOK_FIYATUPDATE` (Tip: 3)
- `STOK_FIYAT_INSERT` (Tip: 1)
- `STOK_FIYAT_SFD_TRG` (Tip: 3)

---

### STOK_FIYAT_DEGISIM_LOG

- **Toplam Kolon:** 9
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_FIYAT_LISTE

- **Toplam Kolon:** 50
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `FIYAT_TANIMI` | VARCHAR(50) | YOK |

---

### STOK_FIYAT_LISTE_DT

- **Toplam Kolon:** 18
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

**İlişkili Trigger'lar:**
- `STOK_FIYAT_LISTE_DT_INSERT` (Tip: 1)
- `STOK_FIYAT_LISTE_DT_SFD_TRG` (Tip: 3)
- `STOK_FIYAT_LISTE_DT_UPDATE` (Tip: 3)

---

### STOK_FIYAT_LISTE_VARSAYILAN

- **Toplam Kolon:** 9
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_FIYAT_TANIM

- **Toplam Kolon:** 4
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `TANIMI` | VARCHAR(20) | YOK |

---

### STOK_GMUHASEBE

- **Toplam Kolon:** 14
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_ISKONTO

- **Toplam Kolon:** 17
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_ISKONTO_DETAY

- **Toplam Kolon:** 15
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_ISK_KIST

- **Toplam Kolon:** 18
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_ISK_KIST_DETAY

- **Toplam Kolon:** 10
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_KAREKOD_TANIM

- **Toplam Kolon:** 6
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_KATEGORI

- **Toplam Kolon:** 5
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_MRP_KK

- **Toplam Kolon:** 10
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_OZELLIK_TANIM

- **Toplam Kolon:** 3
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_OZELLIK_TANIM_DT

- **Toplam Kolon:** 6
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_PAKET

- **Toplam Kolon:** 23
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `PAKET_KODU` | VARCHAR(20) | YOK |

---

### STOK_PAKET_DT

- **Toplam Kolon:** 11
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_PAKET_DT_SRV

- **Toplam Kolon:** 6
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_SAYIM_SONUC

- **Toplam Kolon:** 15
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_SAYIM_SONUC_DT

- **Toplam Kolon:** 9
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_SIPARIS_LISTESI

- **Toplam Kolon:** 21
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_TEDARIKCI

- **Toplam Kolon:** 7
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### STOK_UYUMLU_MARKALAR

- **Toplam Kolon:** 6
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### TUPSU_STOK_ESLESTIRME

- **Toplam Kolon:** 5
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### YSURUN

- **Toplam Kolon:** 18
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### YSURUNDETAY

- **Toplam Kolon:** 10
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### YSURUNESLESME

- **Toplam Kolon:** 13
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

## CARI Tabloları — Yazma Analizi

### ADISYONCARIHR

- **Toplam Kolon:** 20
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `BLCRKODU` | BIGINT | YOK |
| `BLFISKODU` | BIGINT | YOK |

---

### CARI

- **Toplam Kolon:** 176
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `CARIKODU` | VARCHAR(30) | YOK |

---

### CARIHR

- **Toplam Kolon:** 61
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |
| `BLCRKODU` | BIGINT | YOK |

**İlişkili Trigger'lar:**
- `CARIHRK_ONINSERT` (Tip: 17)

---

### CARIHR_VALOR

- **Toplam Kolon:** 10
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CARI_ADRES

- **Toplam Kolon:** 20
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CARI_DOVIZ

- **Toplam Kolon:** 15
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CARI_EK_KESINTILER

- **Toplam Kolon:** 5
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CARI_MANUEL_YASLANDIRMA

- **Toplam Kolon:** 7
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CARI_NOTLAR

- **Toplam Kolon:** 11
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CARI_PAZ_HEDEF

- **Toplam Kolon:** 58
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CARI_SERVIS

- **Toplam Kolon:** 8
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CARI_YASL_DONEM

- **Toplam Kolon:** 27
- **Mevcut Satır:** N/A

---

### CARI_YETKILI

- **Toplam Kolon:** 18
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CARI_ZINCIR_PAZARLAMA

- **Toplam Kolon:** 4
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CRM_CARI_LISTE

- **Toplam Kolon:** 4
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### CRM_CARI_LISTE_DETAY

- **Toplam Kolon:** 5
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### KAMPANYA_MUSTERI

- **Toplam Kolon:** 4
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### OTEL_MUSTERI

- **Toplam Kolon:** 91
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### OTEL_REZERVASYON_MUSTERI

- **Toplam Kolon:** 7
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### OTEL_TARIFE_MUSTERI

- **Toplam Kolon:** 3
- **Mevcut Satır:** N/A

**Zorunlu Alanlar (NOT NULL, Default'suz):**

| Kolon | Tip | Default |
|-------|-----|--------|
| `BLKODU` | BIGINT | YOK |

---

### PTMP_CARIKPB_BAKIYE

- **Toplam Kolon:** 11
- **Mevcut Satır:** N/A

---

### PTMP_CARI_BAKIYE

- **Toplam Kolon:** 9
- **Mevcut Satır:** N/A

---

### PTMP_CARI_BAKIYE_VALOR

- **Toplam Kolon:** 9
- **Mevcut Satır:** N/A

---

### PTMP_CARI_KART_ANALIZI

- **Toplam Kolon:** 19
- **Mevcut Satır:** N/A

---

### PTMP_CARI_MANYASL

- **Toplam Kolon:** 7
- **Mevcut Satır:** N/A

---

### PTMP_CARI_MANYASL_BRC

- **Toplam Kolon:** 17
- **Mevcut Satır:** N/A

---

### PTMP_CARI_OTOYASL_CARI

- **Toplam Kolon:** 24
- **Mevcut Satır:** N/A

---

### PTMP_CARI_OTOYASL_HRK

- **Toplam Kolon:** 22
- **Mevcut Satır:** N/A

---

### PTMP_CARI_ZINCIR_TAHSILAT

- **Toplam Kolon:** 8
- **Mevcut Satır:** N/A

---

### PTMP_FATKZ_MLYTCARI

- **Toplam Kolon:** 11
- **Mevcut Satır:** N/A

---

## Doğrulama Adımları (Manuel)

Aşağıdaki adımlar, yukarıdaki analizin doğrulanması için **gereklidir**:

1. Wolvox arayüzünden test veritabanında bir **test stok kartı** oluşturun.
2. İşlemden önce ve sonra ilgili tablolardan `SELECT COUNT(*)` çalıştırın.
3. Hangi tablolara kaç satır eklendiğini karşılaştırın.
4. Generator değerlerinin değişimini kontrol edin:
   ```sql
   SELECT GEN_ID(BANKAHR_IMPORT_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(CRM_DURUM_TANIM_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(CRPOTKYN_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(DEGISIM_LOG_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(FATURAFISSAYAC_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(GEN_IDT_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(GRUP_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(KULLANICI_OZELRAPOR_UPDATE_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(OFFLINE_UPDATE_LOG_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_ADF_39_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_AF_25_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_AKT_7_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_ANK_8_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_ASP_33_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_ATK_32_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_BH_38_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_BKM_37_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_BUR_18_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_CH_3_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_CR_1_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_CSB_20_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_CS_19_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_DKM_40_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_DST_6_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_EIHR_24_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_ESF_23_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_FRS_5_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_GD_27_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_GLI_28_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_GMCR1_2_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_IHG_42_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_IHT_41_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_KH_9_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_KMP_4_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_MRF_15_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_MRH_16_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_MRO_17_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_MRP_14_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_MSF_26_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_SAE_35_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_SF_22_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_SH_13_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_SRV_36_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_ST_12_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_TDM_11_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_THM_10_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_TPS_21_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_TRI_29_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_TTL_30_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_VSP_34_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SAYAC_VTK_31_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SERVIS_FISDURUMU_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SIPARISHR_URETIM_DETAY_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(SIPARIS_DURUM_TANIM_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(STOKHR_MALIYET_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(UYARI_HATIRLATMA_GEN, 0) FROM RDB$DATABASE;
   SELECT GEN_ID(VERSION_ID_GEN, 0) FROM RDB$DATABASE;
   ```
5. Aynı adımları **cari kart ekleme** için de tekrarlayın.
6. Sonuçları bu dokümana ekleyin veya AI ajanına geri bildirin.

