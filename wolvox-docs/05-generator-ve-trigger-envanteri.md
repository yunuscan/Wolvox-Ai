# Wolvox Firebird Veritabanı — Generator ve Trigger Envanteri

---
**Analiz Tarihi:** 2026-07-19 15:50:10  
**Firebird Sürümü:** 2.5.6 (WI-V6.3.6.27020 Firebird 2.5)  
**Veritabanı:** DEMOWOLVOX (Wolvox 9)  
**Veritabanı Yolu:** `C:\AKINSOFT\Wolvox9\Database_FB\DEMOWOLVOX\2026\WOLVOX.fdb`  
**Charset:** WIN1254  
**Not:** Bu dokümantasyon salt-okunur analiz ile oluşturulmuştur. Wolvox güncellemelerinde şema değişebilir.

---

## Generator / Sequence Listesi

| # | Generator Adı | Mevcut Değer |
|---|--------------|---------------|
| 1 | `BANKAHR_IMPORT_GEN` | 0 |
| 2 | `CRM_DURUM_TANIM_GEN` | 5 |
| 3 | `CRPOTKYN_GEN` | 10 |
| 4 | `DEGISIM_LOG_GEN` | 1 |
| 5 | `FATURAFISSAYAC_GEN` | 42 |
| 6 | `GEN_IDT_GEN` | 6 |
| 7 | `GRUP_GEN` | 10 |
| 8 | `KULLANICI_OZELRAPOR_UPDATE_GEN` | 1 |
| 9 | `OFFLINE_UPDATE_LOG_GEN` | 0 |
| 10 | `SAYAC_ADF_39_GEN` | 0 |
| 11 | `SAYAC_AF_25_GEN` | 0 |
| 12 | `SAYAC_AKT_7_GEN` | 0 |
| 13 | `SAYAC_ANK_8_GEN` | 0 |
| 14 | `SAYAC_ASP_33_GEN` | 0 |
| 15 | `SAYAC_ATK_32_GEN` | 0 |
| 16 | `SAYAC_BH_38_GEN` | 0 |
| 17 | `SAYAC_BKM_37_GEN` | 0 |
| 18 | `SAYAC_BUR_18_GEN` | 0 |
| 19 | `SAYAC_CH_3_GEN` | 0 |
| 20 | `SAYAC_CR_1_GEN` | 0 |
| 21 | `SAYAC_CSB_20_GEN` | 0 |
| 22 | `SAYAC_CS_19_GEN` | 0 |
| 23 | `SAYAC_DKM_40_GEN` | 0 |
| 24 | `SAYAC_DST_6_GEN` | 0 |
| 25 | `SAYAC_EIHR_24_GEN` | 0 |
| 26 | `SAYAC_ESF_23_GEN` | 0 |
| 27 | `SAYAC_FRS_5_GEN` | 0 |
| 28 | `SAYAC_GD_27_GEN` | 0 |
| 29 | `SAYAC_GLI_28_GEN` | 0 |
| 30 | `SAYAC_GMCR1_2_GEN` | 0 |
| 31 | `SAYAC_IHG_42_GEN` | 0 |
| 32 | `SAYAC_IHT_41_GEN` | 0 |
| 33 | `SAYAC_KH_9_GEN` | 0 |
| 34 | `SAYAC_KMP_4_GEN` | 0 |
| 35 | `SAYAC_MRF_15_GEN` | 0 |
| 36 | `SAYAC_MRH_16_GEN` | 0 |
| 37 | `SAYAC_MRO_17_GEN` | 0 |
| 38 | `SAYAC_MRP_14_GEN` | 0 |
| 39 | `SAYAC_MSF_26_GEN` | 0 |
| 40 | `SAYAC_SAE_35_GEN` | 0 |
| 41 | `SAYAC_SF_22_GEN` | 0 |
| 42 | `SAYAC_SH_13_GEN` | 0 |
| 43 | `SAYAC_SRV_36_GEN` | 0 |
| 44 | `SAYAC_ST_12_GEN` | 0 |
| 45 | `SAYAC_TDM_11_GEN` | 0 |
| 46 | `SAYAC_THM_10_GEN` | 0 |
| 47 | `SAYAC_TPS_21_GEN` | 0 |
| 48 | `SAYAC_TRI_29_GEN` | 0 |
| 49 | `SAYAC_TTL_30_GEN` | 0 |
| 50 | `SAYAC_VSP_34_GEN` | 0 |
| 51 | `SAYAC_VTK_31_GEN` | 0 |
| 52 | `SERVIS_FISDURUMU_GEN` | 5 |
| 53 | `SIPARISHR_URETIM_DETAY_GEN` | 0 |
| 54 | `SIPARIS_DURUM_TANIM_GEN` | 13 |
| 55 | `STOKHR_MALIYET_GEN` | 0 |
| 56 | `UYARI_HATIRLATMA_GEN` | 1 |
| 57 | `VERSION_ID_GEN` | 9032 |

## Trigger Listesi

### CARIHRK_ONINSERT

- **Tablo:** `CARIHR`
- **Tip:** TYPE 17
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
DECLARE VARIABLE DOVIZ2KULLAN SMALLINT;
BEGIN
  SELECT CARIHR_DOVIZ2_KULLAN FROM AYAR INTO :DOVIZ2KULLAN;

  IF ((:DOVIZ2KULLAN <> 1) OR (COALESCE(NEW.DOVIZ_BIRIMI2,'')='') OR (NEW.DOVIZ_BIRIMI2=NEW.DOVIZ_BIRIMI)) THEN
  BEGIN
    NEW.DOVIZ_BIRIMI2 = NEW.DOVIZ_BIRIMI;
    NEW.DVZ_BTUT2     = NEW.DVZ_BTUT;
    NEW.DVZ_ATUT2     = NEW.DVZ_ATUT;
    NEW.DOVIZ_ALIS2   = NEW.DOVIZ_ALIS;
    NEW.DOVIZ_SATIS2  = NEW.DOVIZ_SATIS;
  END
END
```

---

### TRG_SA_ENT

- **Tablo:** `SATINALMA_ENTEGRASYON`
- **Tip:** TYPE 114
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
DECLARE VARIABLE MODUL_KODU VARCHAR(20);
DECLARE VARIABLE NEW_STATE SMALLINT;
DECLARE VARIABLE BLSAKODU BIGINT;
BEGIN
  BLSAKODU = NEW.BLSAKODU; --AFTER INSERT
  IF (:BLSAKODU IS NULL) THEN
    BLSAKODU = OLD.BLSAKODU; --AFTER DELETE

  SELECT FIRST 1 MODUL_KODU FROM SATINALMA_ENTEGRASYON
    WHERE BLSAKODU=:BLSAKODU AND COALESCE(SILINDI,0)=0
    ORDER BY BLKODU DESC INTO :MODUL_KODU;
  NEW_STATE = NULL;

  IF ((:MODUL_KODU = 'FATURA') OR (:MODUL_KODU = 'IRSALIYE')) THEN
    NEW_STATE = 4;
  ELSE IF (:MODUL_KODU = 'TEKLIF') THEN
    NEW_STATE = 3;
  ELSE IF (:MODUL_KODU = 'SIPARIS') THEN
    NEW_STATE = 2;
  ELSE
    NEW_STATE = 1;

  UPDATE STOK_SIPARIS_LISTESI SET DURUMU = :NEW_STATE WHERE BLKODU=:BLSAKODU;
END
```

---

### STOKHR_ONINSERT

- **Tablo:** `STOKHR`
- **Tip:** TYPE 17
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
    DECLARE VARIABLE KPB_GMIK_M DOUBLE PRECISION;
    DECLARE VARIABLE KPB_GFYT_M DOUBLE PRECISION;
    DECLARE VARIABLE KPB_CMIK_M DOUBLE PRECISION;
    DECLARE VARIABLE KPB_CFYT_M DOUBLE PRECISION;

    DECLARE VARIABLE DVZ_GMIK_M DOUBLE PRECISION;
    DECLARE VARIABLE DVZ_GFYT_M DOUBLE PRECISION;
    DECLARE VARIABLE DVZ_CMIK_M DOUBLE PRECISION;
    DECLARE VARIABLE DVZ_CFYT_M DOUBLE PRECISION;
BEGIN
    SELECT SUM(CASE WHEN ISLEM_TIPI = 2 THEN SM.MIKTARI ELSE 0 END), SUM(CASE WHEN ISLEM_TIPI = 2 THEN SM.MIKTARI ELSE 0 END),
        SUM(CASE WHEN ISLEM_TIPI = 1 THEN SM.KPB_FIYATI ELSE 0 END), SUM(CASE WHEN ISLEM_TIPI = 1 THEN SM.DVZ_FIYATI ELSE 0 END) FROM STOKHR_MALIYET SM
        WHERE SM.BLHRKODU=NEW.BLKODU AND COALESCE(SM.SILINDI,0)=0
        INTO :KPB_GMIK_M, :DVZ_GMIK_M, :KPB_GFYT_M, :DVZ_GFYT_M;

    IF (NEW.TUTAR_TURU = 1) THEN
    BEGIN --GIRIS ISLEMI
        NEW.KPB_GMIK_M = NEW.KPB_GMIK + COALESCE(KPB_GMIK_M, 0);
        NEW.KPB_GFYT_M = NEW.KPB_FIYATI + COALESCE(KPB_GFYT_M, 0);
    
        IF ((NEW.DOVIZ_KULLAN = 1) AND (NEW.DOVIZ_HES_ISLE = 1)) THEN
        BEGIN
            NEW.DVZ_GMIK_M = NEW.DVZ_GMIK + COALESCE(DVZ_GMIK_M, 0);
            NEW.DVZ_GFYT_M = NEW.DOVIZ_FIYATI + COALESCE(DVZ_GFYT_M, 0);
        END

        NEW.KPB_CMIK_M = NULL;
        NEW.KPB_CFYT_M = NULL;
        NEW.DVZ_CMIK_M = NULL;
        NEW.DVZ_CFYT_M = NULL;
   END ELSE
   BEGIN --CIKIS ISLEMI
        NEW.KPB_CMIK_M = NEW.KPB_CMIK + COALESCE(KPB_CMIK_M, 0);
        NEW.KPB_CFYT_M = NEW.KPB_FIYATI + COALESCE(KPB_CFYT_M, 0);
    
        IF ((NEW.DOVIZ_KULLAN = 1) AND (NEW.DOVIZ_HES_ISLE = 1)) THEN
        BEGIN
            NEW.DVZ_CMIK_M = NEW.DVZ_CMIK + COALESCE(DVZ_CMIK_M, 0);
            NEW.DVZ_CFYT_M = NEW.DOVIZ_FIYATI + COALESCE(DVZ_CFYT_M, 0);
        END

        NEW.KPB_GMIK_M = NULL;
        NEW.KPB_GFYT_M = NULL;
        NEW.DVZ_GMIK_M = NULL;
        NEW.DVZ_GFYT_M = NULL;
   END
END
```

---

### STOKHR_MALIYET_ONINSERT

- **Tablo:** `STOKHR_MALIYET`
- **Tip:** TYPE 114
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
DECLARE VARIABLE xBLHRKODU BIGINT;
BEGIN
  IF (DELETING) THEN
    xBLHRKODU = OLD.BLHRKODU;
  ELSE
    xBLHRKODU = NEW.BLHRKODU;

  UPDATE STOKHR SET ACIKLAMA=ACIKLAMA WHERE BLKODU = :xBLHRKODU;
END
```

---

### STOK_FIYATUPDATE

- **Tablo:** `STOK_FIYAT`
- **Tip:** BEFORE UPDATE
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
BEGIN
    IF ((NEW.ALIS_SATIS = 1) AND (NEW.FIYATI <> OLD.FIYATI)) THEN
        NEW.ALIS_FIYATI_DEGISTI = 1;

    IF ((NEW.ALIS_SATIS = 2) AND (NEW.FIYATI <> OLD.FIYATI)) THEN
        NEW.SF_ETIKET_BASILACAK = 1;

    IF (NEW.FIYATI <> OLD.FIYATI) THEN
        NEW.FIYAT_DEG_TARIHI = CURRENT_TIMESTAMP;
END
```

---

### STOK_FIYAT_INSERT

- **Tablo:** `STOK_FIYAT`
- **Tip:** BEFORE INSERT
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
BEGIN
    IF (NEW.FIYAT_DEG_TARIHI IS NULL) THEN
        NEW.FIYAT_DEG_TARIHI = CURRENT_TIMESTAMP;
END
```

---

### STOK_FIYAT_SFD_TRG

- **Tablo:** `STOK_FIYAT`
- **Tip:** BEFORE UPDATE
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
    DECLARE SFLT SMALLINT;
    DECLARE BLKODU BIGINT;
    DECLARE USER_NAME VARCHAR(20);
BEGIN
    SELECT COALESCE(STOK_FIYAT_LOG_TURU,0) FROM AYAR INTO :SFLT;

    IF ((OLD.ALIS_SATIS=1) AND NOT (:SFLT IN (1,3))) THEN
        EXIT;

    IF ((OLD.ALIS_SATIS=2) AND NOT (:SFLT IN (2,3))) THEN
        EXIT;

    IF (NEW.FIYATI=OLD.FIYATI OR COALESCE(OLD.FIYATI,0)=0) THEN
        EXIT;

    EXECUTE STATEMENT 'SELECT GEN_VALUE FROM SP_GEN_ID(''FIYAT_DEGISIM_LOG_GEN'', 1)' INTO :BLKODU;
    SELECT RDB$GET_CONTEXT('USER_SESSION', 'USER_NAME') FROM RDB$DATABASE INTO :USER_NAME;

    INSERT INTO  STOK_FIYAT_DEGISIM_LOG(BLKODU,BLSTKODU,HESAP,FIYATI,KAYDEDEN,KAYIT_TARIHI,FIYAT_NO, ALIS_SATIS)
        VALUES(:BLKODU,OLD.BLSTKODU,OLD.HESAP,OLD.FIYATI,:USER_NAME,CURRENT_TIMESTAMP,OLD.FIYAT_NO, OLD.ALIS_SATIS);
END
```

---

### STOK_FIYAT_LISTE_DT_INSERT

- **Tablo:** `STOK_FIYAT_LISTE_DT`
- **Tip:** BEFORE INSERT
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
BEGIN
    IF (NEW.FIYAT_DEG_TARIHI IS NULL) THEN
        NEW.FIYAT_DEG_TARIHI = CURRENT_TIMESTAMP;
END
```

---

### STOK_FIYAT_LISTE_DT_SFD_TRG

- **Tablo:** `STOK_FIYAT_LISTE_DT`
- **Tip:** BEFORE UPDATE
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
    DECLARE SFLT SMALLINT;
    DECLARE BLKODU BIGINT;
    DECLARE USER_NAME VARCHAR(20);
BEGIN
    SELECT COALESCE(STOK_FIYAT_LOG_TURU,0) FROM AYAR INTO :SFLT;

    IF (:SFLT NOT IN (2,3)) THEN
        EXIT;
        
    IF (NEW.FIYATI=OLD.FIYATI OR COALESCE(OLD.FIYATI,0)=0) THEN
        EXIT;

    EXECUTE STATEMENT 'SELECT GEN_VALUE FROM SP_GEN_ID(''FIYAT_DEGISIM_LOG_GEN'', 1)' INTO :BLKODU;
    SELECT RDB$GET_CONTEXT('USER_SESSION', 'USER_NAME') FROM RDB$DATABASE INTO :USER_NAME;

    INSERT INTO  STOK_FIYAT_DEGISIM_LOG(BLKODU,BLSTKODU,FIYATI,KAYDEDEN,KAYIT_TARIHI,BLGFDTKODU, ALIS_SATIS)
        VALUES(:BLKODU,OLD.BLSTKODU,OLD.FIYATI,:USER_NAME,CURRENT_TIMESTAMP,OLD.BLKODU,2);
END
```

---

### STOK_FIYAT_LISTE_DT_UPDATE

- **Tablo:** `STOK_FIYAT_LISTE_DT`
- **Tip:** BEFORE UPDATE
- **Sıra:** 0
- **Durum:** 🟢 AKTİF

**Kaynak Kodu:**
```sql
AS
BEGIN
    IF (NEW.FIYATI <> OLD.FIYATI) THEN
        NEW.FIYAT_DEG_TARIHI = CURRENT_TIMESTAMP;
END
```

---

## Stored Procedure Listesi

| # | Procedure Adı | Input Param | Output Param |
|---|--------------|-------------|---------------|
| 1 | `ADISYON_KF` | 2 | 2 |
| 2 | `ASORTI_MIK_HES` | 2 | 6 |
| 3 | `BAKIYEDEGERBUL` | 3 | 2 |
| 4 | `BONUS_BAKIYE` | 2 | 0 |
| 5 | `CARIKPB_BAKIYE` | 3 | 0 |
| 6 | `CARISTOK_ENSONSATISFYT` | 4 | 0 |
| 7 | `CARI_BAKIYE` | 5 | 0 |
| 8 | `CARI_BAKIYE_VALOR` | 10 | 0 |
| 9 | `CARI_KART_ANALIZI` | 12 | 0 |
| 10 | `CARI_MAN_YASLANDIRMA` | 9 | 0 |
| 11 | `CARI_OTO_YASLANDIRMA` | 11 | 0 |
| 12 | `CARI_ZINCIR_TAHSILAT` | 7 | 0 |
| 13 | `CRDNM_BAKIYE` | 7 | 0 |
| 14 | `CRDNM_BAKIYE_TAKSIT` | 7 | 0 |
| 15 | `CSCARIBUL` | 6 | 6 |
| 16 | `DEPO_ENVANTERI` | 16 | 0 |
| 17 | `DEPO_LOKASYON_OLUSTUR` | 2 | 0 |
| 18 | `DEPO_SIPARIS_LISTESI` | 5 | 0 |
| 19 | `FATKZ_MLYTCARI` | 10 | 0 |
| 20 | `FATURA_KF` | 4 | 3 |
| 21 | `FATURA_STOKTAHS_TURU` | 3 | 0 |
| 22 | `FNAN_TAHMINI` | 4 | 3 |
| 23 | `HIZMET_RAPORU` | 9 | 0 |
| 24 | `ISTATISTIKAYARLA` | 4 | 0 |
| 25 | `ISTATISTIKAYARLA_2` | 13 | 1 |
| 26 | `KURKONTROL` | 3 | 2 |
| 27 | `MRP_EMIRLERI_FASON_KARS` | 4 | 10 |
| 28 | `MRP_MAKINE_CALISMA` | 1 | 4 |
| 29 | `MRP_OPERASYON_KARS` | 4 | 10 |
| 30 | `MRP_URETILEN_MIKTAR` | 2 | 3 |
| 31 | `ONODEMEKONTROL` | 1 | 3 |
| 32 | `OTEL_ENVANTER_LISTESI` | 3 | 9 |
| 33 | `OTEL_INTLOGUCRET` | 0 | 15 |
| 34 | `OTEL_KURKONTROL` | 4 | 2 |
| 35 | `OTEL_ODA_BILGI` | 3 | 5 |
| 36 | `OTEL_ODA_LISTESI` | 0 | 5 |
| 37 | `OTEL_ODA_LISTESI_2` | 0 | 4 |
| 38 | `OTEL_REZERVASYON_BILGI` | 1 | 3 |
| 39 | `OTEL_REZERVASYON_LISTE` | 2 | 0 |
| 40 | `OTEL_REZERVASYON_LISTE_2` | 1 | 11 |
| 41 | `P_SATIS_FIYATI_BUL` | 7 | 1 |
| 42 | `P_SATIS_FIYATLARI` | 4 | 5 |
| 43 | `P_SATIS_FIYATLARI_2` | 4 | 4 |
| 44 | `P_SATIS_FIYATLARI_LISTE` | 6 | 1 |
| 45 | `ROTA_RAPORU` | 2 | 6 |
| 46 | `SERILOT_ENVBAKIYE` | 7 | 0 |
| 47 | `SERILOT_MALIYET` | 8 | 0 |
| 48 | `SERINOBAKIYEBUL` | 3 | 4 |
| 49 | `SERINORAPORU` | 3 | 0 |
| 50 | `SIPARIS_URETIM_BILGI` | 1 | 3 |
| 51 | `SP_GEN_ID` | 3 | 1 |
| 52 | `STOKHAREKETTOPLA` | 10 | 0 |
| 53 | `STOKHR_SATIRBAKIYE` | 4 | 0 |
| 54 | `STOKKZ_LIFOFIFO` | 13 | 2 |
| 55 | `STOK_ALIS_FIYATI_DEGISTIR` | 6 | 0 |
| 56 | `STOK_BARKOD_BUL` | 1 | 3 |
| 57 | `STOK_BARKOD_BUL_TEK` | 2 | 1 |
| 58 | `STOK_BARKOD_BUL_TUMU` | 1 | 3 |
| 59 | `STOK_DNMRAP` | 3 | 0 |
| 60 | `STOK_ENVANTER` | 17 | 0 |
| 61 | `STOK_ENVANTER_DEPO` | 4 | 0 |
| 62 | `STOK_FIFO_KALANLAR` | 9 | 0 |
| 63 | `STOK_FIYATLARI_BUL` | 3 | 32 |
| 64 | `STOK_FIYATLARI_BUL2` | 7 | 48 |
| 65 | `STOK_ISLEM_GORMEYEN` | 7 | 0 |
| 66 | `STOK_KZB` | 12 | 0 |
| 67 | `STOK_KZN` | 12 | 0 |
| 68 | `STOK_KZ_OZEL` | 15 | 0 |
| 69 | `STOK_RAPOR_FIYAT` | 6 | 1 |
| 70 | `STOK_YETERLILIK` | 8 | 0 |
| 71 | `TAKSIT_BAKIYE` | 2 | 0 |
| 72 | `TUPSUGUNCEL` | 2 | 0 |
| 73 | `VALOR_HESAPLA` | 4 | 3 |

### ADISYON_KF

**Parametreler:**
- INPUT: `BLFISKODU`
- INPUT: `KPBONDALIK`
- OUTPUT: `KF_TUTARI`
- OUTPUT: `KF_ACIKLAMA`

**Kaynak Kodu:** Okunamadı veya boş.

---

### ASORTI_MIK_HES

**Parametreler:**
- INPUT: `BLHARKODU`
- INPUT: `ST_STKODU`
- OUTPUT: `TBLMASKODU`
- OUTPUT: `TBLSTKODU`
- OUTPUT: `MIKTARI`
- OUTPUT: `MIKTARI_TESLIM`
- OUTPUT: `MIKTARI_IPTAL`
- OUTPUT: `MIKTARI_KALAN`

**Kaynak Kodu:** Okunamadı veya boş.

---

### BAKIYEDEGERBUL

**Parametreler:**
- INPUT: `BORC`
- INPUT: `ALACAK`
- INPUT: `ONDALIK`
- OUTPUT: `BAKIYE`
- OUTPUT: `BTR`

**Kaynak Kodu:** Okunamadı veya boş.

---

### BONUS_BAKIYE

**Parametreler:**
- INPUT: `USERID`
- INPUT: `EKSART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CARIKPB_BAKIYE

**Parametreler:**
- INPUT: `USERID`
- INPUT: `EKSART`
- INPUT: `KURTIPI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CARISTOK_ENSONSATISFYT

**Parametreler:**
- INPUT: `USERID`
- INPUT: `STOKSART`
- INPUT: `CARISART`
- INPUT: `SON_FIYAT_SAYISI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CARI_BAKIYE

**Parametreler:**
- INPUT: `USERID`
- INPUT: `CARISART`
- INPUT: `ILKISLEMTARIHI`
- INPUT: `DONEMSEL_BAKIYE`
- INPUT: `DOVIZ_KULLAN`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CARI_BAKIYE_VALOR

**Parametreler:**
- INPUT: `USERID`
- INPUT: `CARISART`
- INPUT: `CARIHRSART`
- INPUT: `ILKISLEMTARIHI`
- INPUT: `DONEMSEL_VALOR`
- INPUT: `DOVIZ_KULLAN`
- INPUT: `VALOR_FIELD`
- INPUT: `BUGUN_TARIHI`
- INPUT: `BKY_ODEME_TARIHI`
- INPUT: `DNM_VALOR_DRM`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CARI_KART_ANALIZI

**Parametreler:**
- INPUT: `USERID`
- INPUT: `FILTRESART`
- INPUT: `EKSART_ACIKHES`
- INPUT: `EKSART_CEKSEN`
- INPUT: `IRSALIYETOPLA`
- INPUT: `EKSART_IRS`
- INPUT: `HESAP`
- INPUT: `CEKSENETTOPLA`
- INPUT: `SIPARISTOPLA`
- INPUT: `EKSART_SIP`
- INPUT: `KPBOND`
- INPUT: `DVZOND`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CARI_MAN_YASLANDIRMA

**Parametreler:**
- INPUT: `USERID`
- INPUT: `ONDALIK`
- INPUT: `CARISART`
- INPUT: `HRK_ILKSART`
- INPUT: `HRK_SONSART`
- INPUT: `VALOR_TIPI`
- INPUT: `VALOR_BUGUN`
- INPUT: `HESAP`
- INPUT: `VALORU_ACIKHRK_HESAPLA`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CARI_OTO_YASLANDIRMA

**Parametreler:**
- INPUT: `USERID`
- INPUT: `YASLI_TIPI`
- INPUT: `CARI_SART`
- INPUT: `HRK_SART`
- INPUT: `RAPOR_HESAP`
- INPUT: `YASLANDIRMA_GRUBU`
- INPUT: `VALOR_BUGUN`
- INPUT: `HASOND`
- INPUT: `SIRALAMA_TIPI`
- INPUT: `TAKSITLI`
- INPUT: `VALORU_ACIKHRK_HESAPLA`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CARI_ZINCIR_TAHSILAT

**Parametreler:**
- INPUT: `USERID`
- INPUT: `TARIH1`
- INPUT: `TARIH2`
- INPUT: `EKSART`
- INPUT: `DURUM`
- INPUT: `FILTRE_BLCRKODU`
- INPUT: `ISLEM_GORMEYENLER`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CRDNM_BAKIYE

**Parametreler:**
- INPUT: `USERID`
- INPUT: `KPBOND`
- INPUT: `DVZOND`
- INPUT: `EKSART`
- INPUT: `SART_BORC`
- INPUT: `SART_ALACAK`
- INPUT: `DOVIZ_BIRIMI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CRDNM_BAKIYE_TAKSIT

**Parametreler:**
- INPUT: `USERID`
- INPUT: `KPBOND`
- INPUT: `DVZOND`
- INPUT: `EKSART`
- INPUT: `SART_BORC`
- INPUT: `SART_ALACAK`
- INPUT: `DOVIZ_BIRIMI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### CSCARIBUL

**Parametreler:**
- INPUT: `BLCSKODU`
- INPUT: `EVRAK_TURU`
- INPUT: `BLCRKODU`
- INPUT: `CIROBLCRKODU`
- INPUT: `TEMINATMI`
- INPUT: `EVRAK_DURUMU`
- OUTPUT: `GCARIKODU`
- OUTPUT: `GTICARI_UNVANI`
- OUTPUT: `GADI_SOYADI`
- OUTPUT: `CCARIKODU`
- OUTPUT: `CTICARI_UNVANI`
- OUTPUT: `CADI_SOYADI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### DEPO_ENVANTERI

**Parametreler:**
- INPUT: `USERID`
- INPUT: `ENVDRM`
- INPUT: `SART`
- INPUT: `KALANMIKTAR`
- INPUT: `RAPORHESAP`
- INPUT: `KPBDVZAYIR`
- INPUT: `MIKTAR_ENV`
- INPUT: `ANASTOK_ENVANTER`
- INPUT: `ILK_TARIH`
- INPUT: `SON_TARIH`
- INPUT: `DONEMSEL_ISTATISTIK`
- INPUT: `SUBEKODU_SART`
- INPUT: `DEVIRLERI_EKLE`
- INPUT: `BLOKE_TOPLA`
- INPUT: `EKMLY_EKLE`
- INPUT: `VARYANT_DETAYLI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### DEPO_LOKASYON_OLUSTUR

**Parametreler:**
- INPUT: `USER_ID`
- INPUT: `DEPO_SART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### DEPO_SIPARIS_LISTESI

**Parametreler:**
- INPUT: `USERID`
- INPUT: `SART`
- INPUT: `DEPO_SART`
- INPUT: `SUBE_SART`
- INPUT: `BLOKE_TOPLA`

**Kaynak Kodu:** Okunamadı veya boş.

---

### FATKZ_MLYTCARI

**Parametreler:**
- INPUT: `USERID`
- INPUT: `ISTDRM`
- INPUT: `RAPORHESAP`
- INPUT: `SART`
- INPUT: `KPBDVZAYIR`
- INPUT: `DONEMSEL_ISTATISTIK`
- INPUT: `SUBE_SART`
- INPUT: `EKMLY_EKLE`
- INPUT: `HIZMETLERI_EKLE`
- INPUT: `VARYANT_DETAYLI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### FATURA_KF

**Parametreler:**
- INPUT: `BLFTKODU`
- INPUT: `FAT_TURU`
- INPUT: `KPB_TOPLAM`
- INPUT: `KPBONDALIK`
- OUTPUT: `KF_TUTARI`
- OUTPUT: `KF_DURUMU`
- OUTPUT: `KF_ACIKLAMA`

**Kaynak Kodu:** Okunamadı veya boş.

---

### FATURA_STOKTAHS_TURU

**Parametreler:**
- INPUT: `USERID`
- INPUT: `HESAP`
- INPUT: `EK_SART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### FNAN_TAHMINI

**Parametreler:**
- INPUT: `ILKDATE`
- INPUT: `SONDATE`
- INPUT: `BORC_TUTARI`
- INPUT: `ALACAK_TUTARI`
- OUTPUT: `TARIHI`
- OUTPUT: `BORC`
- OUTPUT: `ALACAK`

**Kaynak Kodu:** Okunamadı veya boş.

---

### HIZMET_RAPORU

**Parametreler:**
- INPUT: `USERID`
- INPUT: `MIKOND`
- INPUT: `KPBOND`
- INPUT: `DVZOND`
- INPUT: `EKSART`
- INPUT: `SUBEKODU_SART`
- INPUT: `RAPORHESAP`
- INPUT: `KPBDVZAYIR`
- INPUT: `VERGILI_TOPLAM`

**Kaynak Kodu:** Okunamadı veya boş.

---

### ISTATISTIKAYARLA

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `HESAP`
- INPUT: `KPBDVZAYIR`
- INPUT: `SQLSART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### ISTATISTIKAYARLA_2

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `ISTDRM`
- INPUT: `KPBDVZ`
- INPUT: `DVZBRM`
- INPUT: `KPBDVZAYIR`
- INPUT: `KPB_DVZBRM`
- INPUT: `SON_TARIH`
- INPUT: `TPLCIKAN_MIKTAR`
- INPUT: `CIKAN_MIKTAR`
- INPUT: `LFFF_ONCESI`
- INPUT: `SUBEKODU_SART`
- INPUT: `EKMLY_EKLE`
- INPUT: `VARYANT_KODU`
- OUTPUT: `RFIYAT`

**Kaynak Kodu:** Okunamadı veya boş.

---

### KURKONTROL

**Parametreler:**
- INPUT: `DVZBRM`
- INPUT: `TARIH`
- INPUT: `SUBEKODU_SART`
- OUTPUT: `RALIS`
- OUTPUT: `RSATIS`

**Kaynak Kodu:** Okunamadı veya boş.

---

### MRP_EMIRLERI_FASON_KARS

**Parametreler:**
- INPUT: `BLMASKODU`
- INPUT: `FASON_TIPI`
- INPUT: `MIKTAR_ONDALIK`
- INPUT: `BIRIM_MALIYETI`
- OUTPUT: `URT_BLSTKODU`
- OUTPUT: `URT_STOK_ADI`
- OUTPUT: `URT_MIKTARI`
- OUTPUT: `URT_MIKTARI_FIRE`
- OUTPUT: `URT_FIRE_YUZDESI`
- OUTPUT: `URT_GIDIS_TARIHI`
- OUTPUT: `URT_GELIS_TARIHI`
- OUTPUT: `URT_GIDIS_PARTI_SAYISI`
- OUTPUT: `URT_GELIS_PARTI_SAYISI`
- OUTPUT: `URT_BIRIM_MALIYETI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### MRP_MAKINE_CALISMA

**Parametreler:**
- INPUT: `ABLURKODU`
- OUTPUT: `BLURKODU`
- OUTPUT: `MAKINE_ADI`
- OUTPUT: `TOPLAM_SURE`
- OUTPUT: `NET_CALISMA`

**Kaynak Kodu:** Okunamadı veya boş.

---

### MRP_OPERASYON_KARS

**Parametreler:**
- INPUT: `BLURHRKODU`
- INPUT: `BLOPRKODU`
- INPUT: `BLMAKINEKODU`
- INPUT: `MIKOND`
- OUTPUT: `PURETIM_MIKTARI`
- OUTPUT: `PNET_CALISMA`
- OUTPUT: `PBASLAMA_ZAMANI`
- OUTPUT: `PBITIS_ZAMANI`
- OUTPUT: `SURETILEN_MIKTAR`
- OUTPUT: `SONAYLANAN_MIKTAR`
- OUTPUT: `SFIRE_MIKTARI`
- OUTPUT: `SNET_CALISMA`
- OUTPUT: `SBASLAMA_ZAMANI`
- OUTPUT: `SBITIS_ZAMANI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### MRP_URETILEN_MIKTAR

**Parametreler:**
- INPUT: `BLURHRKODU`
- INPUT: `MIKTAROND`
- OUTPUT: `URETILEN_MIKTAR`
- OUTPUT: `ONAYLANAN_MIKTAR`
- OUTPUT: `FIRE_MIKTARI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### ONODEMEKONTROL

**Parametreler:**
- INPUT: `BLONODEMEKODU`
- OUTPUT: `KALAN`
- OUTPUT: `KULLANILAN`
- OUTPUT: `DURUM`

**Kaynak Kodu:** Okunamadı veya boş.

---

### OTEL_ENVANTER_LISTESI

**Parametreler:**
- INPUT: `BLENVANTERKODU`
- INPUT: `KIRA_BASLANGIC_TARIHI`
- INPUT: `KIRA_BITIS_TARIHI`
- OUTPUT: `ENVANTER_ADI`
- OUTPUT: `KATEGORI`
- OUTPUT: `SORUMLU_BIRIM`
- OUTPUT: `FIYAT_GRUBU`
- OUTPUT: `FIYATI`
- OUTPUT: `SAATLIK_CALISTIR`
- OUTPUT: `HESAP_DEPARTMANI`
- OUTPUT: `ENVANTER_ADETI`
- OUTPUT: `MEVCUT_ADETI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### OTEL_INTLOGUCRET

**Parametreler:**
- OUTPUT: `SUBE_KODU`
- OUTPUT: `REZERVASKONKODU`
- OUTPUT: `MUSTERIKODU`
- OUTPUT: `ACENTAKODU`
- OUTPUT: `ODA_ADI`
- OUTPUT: `MUSTERI_ADI`
- OUTPUT: `MUSTERI_SOYADI`
- OUTPUT: `TC_KIMLIK_NO`
- OUTPUT: `PASAPORT_NO`
- OUTPUT: `DOGUM_TARIHI`
- OUTPUT: `CHECK_IN_TARIHI`
- OUTPUT: `CHECK_OUT_TARIHI`
- OUTPUT: `ACENTA_TANIM`
- OUTPUT: `ACENTA_ADI`
- OUTPUT: `ACENTA_SOYADI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### OTEL_KURKONTROL

**Parametreler:**
- INPUT: `DVZBRM`
- INPUT: `TARIH`
- INPUT: `SUBEKODU_SART`
- INPUT: `KUR_TURU`
- OUTPUT: `RALIS`
- OUTPUT: `RSATIS`

**Kaynak Kodu:** Okunamadı veya boş.

---

### OTEL_ODA_BILGI

**Parametreler:**
- INPUT: `ABLODAKODU`
- INPUT: `AGIRIS_TARIHI`
- INPUT: `ACIKIS_TARIHI`
- OUTPUT: `BLREZKODU`
- OUTPUT: `DURUMU`
- OUTPUT: `ARIZA`
- OUTPUT: `GIRISTARIHI`
- OUTPUT: `CIKISTARIHI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### OTEL_ODA_LISTESI

**Parametreler:**
- OUTPUT: `BLODAKODU`
- OUTPUT: `BLREZERVASYONKODU`
- OUTPUT: `BLODASAHIBIKODU`
- OUTPUT: `MUSTERILER`
- OUTPUT: `MUSTERI_PROBLEM`

**Kaynak Kodu:** Okunamadı veya boş.

---

### OTEL_ODA_LISTESI_2

**Parametreler:**
- OUTPUT: `BLODAKODU`
- OUTPUT: `BLREZERVASYONKODU`
- OUTPUT: `BLODASAHIBIKODU`
- OUTPUT: `MUSTERILER`

**Kaynak Kodu:** Okunamadı veya boş.

---

### OTEL_REZERVASYON_BILGI

**Parametreler:**
- INPUT: `BLREZERVASYONKODU`
- OUTPUT: `DGUNU`
- OUTPUT: `EYILDONUMU`
- OUTPUT: `KONAKLAMA`

**Kaynak Kodu:** Okunamadı veya boş.

---

### OTEL_REZERVASYON_LISTE

**Parametreler:**
- INPUT: `USERID`
- INPUT: `EK_SART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### OTEL_REZERVASYON_LISTE_2

**Parametreler:**
- INPUT: `BLRZKODU`
- OUTPUT: `BLREZERVASYONKODU`
- OUTPUT: `BLODASAHIBIKODU`
- OUTPUT: `BLACENTAKODU`
- OUTPUT: `BLTARIFEKODU`
- OUTPUT: `ODALAR`
- OUTPUT: `ODABLKODLARI`
- OUTPUT: `MISAFIRLER`
- OUTPUT: `MISAFIRBLKODLARI`
- OUTPUT: `BLGRUPKODU`
- OUTPUT: `BLODAKODU`
- OUTPUT: `MUSTERI_PROBLEM`

**Kaynak Kodu:** Okunamadı veya boş.

---

### P_SATIS_FIYATI_BUL

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `BLCRKODU`
- INPUT: `BIRIMI`
- INPUT: `HESAP`
- INPUT: `SUBE_KODU`
- INPUT: `ADRES_TANIMI`
- INPUT: `VARYANT_KODU`
- OUTPUT: `GECERLI_FIYAT`

**Kaynak Kodu:** Okunamadı veya boş.

---

### P_SATIS_FIYATLARI

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `HESAP`
- INPUT: `SUBE_KODU`
- INPUT: `VARYANT_DETAYLI`
- OUTPUT: `LISTE_FIYAT_1`
- OUTPUT: `LISTE_FIYAT_2`
- OUTPUT: `LISTE_FIYAT_3`
- OUTPUT: `LISTE_FIYAT_4`
- OUTPUT: `VARYANT_KODU`

**Kaynak Kodu:** Okunamadı veya boş.

---

### P_SATIS_FIYATLARI_2

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `HESAP`
- INPUT: `SUBE_KODU`
- INPUT: `BIRIMI`
- OUTPUT: `LISTE_FIYAT_1`
- OUTPUT: `LISTE_FIYAT_2`
- OUTPUT: `LISTE_FIYAT_3`
- OUTPUT: `LISTE_FIYAT_4`

**Kaynak Kodu:** Okunamadı veya boş.

---

### P_SATIS_FIYATLARI_LISTE

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `BIRIMI`
- INPUT: `HESAP`
- INPUT: `LISTEKODU`
- INPUT: `SUBE_KODU`
- INPUT: `VARYANT_KODU`
- OUTPUT: `FIYAT`

**Kaynak Kodu:** Okunamadı veya boş.

---

### ROTA_RAPORU

**Parametreler:**
- INPUT: `BLCRKODU`
- INPUT: `ZIYARET_ARALIK`
- OUTPUT: `SON_ZIYARET_TARIHI`
- OUTPUT: `GUN_FARK`
- OUTPUT: `SON_BLPAZKODU`
- OUTPUT: `SONRAKI_ZIYARET_TARIHI`
- OUTPUT: `GECIKME_GUN`
- OUTPUT: `PLANLAMA_TARIHI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### SERILOT_ENVBAKIYE

**Parametreler:**
- INPUT: `USERID`
- INPUT: `ISLEM_TIPI`
- INPUT: `KPBMI`
- INPUT: `MIKOND`
- INPUT: `FIYATOND`
- INPUT: `TUTAROND`
- INPUT: `SART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### SERILOT_MALIYET

**Parametreler:**
- INPUT: `USERID`
- INPUT: `ISLEM_TIPI`
- INPUT: `KPBMI`
- INPUT: `MIKOND`
- INPUT: `FIYATOND`
- INPUT: `TUTAROND`
- INPUT: `SART`
- INPUT: `EKMLY_EKLE`

**Kaynak Kodu:** Okunamadı veya boş.

---

### SERINOBAKIYEBUL

**Parametreler:**
- INPUT: `SERINO`
- INPUT: `SUBEKODU_SART`
- INPUT: `DEPOADI_SART`
- OUTPUT: `BLSTKODU`
- OUTPUT: `DEPO_ADI`
- OUTPUT: `IZLEME_TIPI`
- OUTPUT: `BAKIYE`

**Kaynak Kodu:** Okunamadı veya boş.

---

### SERINORAPORU

**Parametreler:**
- INPUT: `USERID`
- INPUT: `SART`
- INPUT: `EKSART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### SIPARIS_URETIM_BILGI

**Parametreler:**
- INPUT: `BLSHKODU`
- OUTPUT: `URETIM_MODUL`
- OUTPUT: `URETIM_KODU`
- OUTPUT: `URETIM_DURUMU`

**Kaynak Kodu:** Okunamadı veya boş.

---

### SP_GEN_ID

**Parametreler:**
- INPUT: `GEN_NAME`
- INPUT: `INCREMENT`
- INPUT: `DONGU`
- OUTPUT: `GEN_VALUE`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOKHAREKETTOPLA

**Parametreler:**
- INPUT: `USERID`
- INPUT: `STOKSART`
- INPUT: `STOKHRSART`
- INPUT: `DEPOADI`
- INPUT: `DEVIR`
- INPUT: `MIKOND`
- INPUT: `BLOKETOPLA`
- INPUT: `TERMINTOPLA`
- INPUT: `BLOKESART`
- INPUT: `SUBE_SART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOKHR_SATIRBAKIYE

**Parametreler:**
- INPUT: `USERID`
- INPUT: `SQLSART`
- INPUT: `DEVIR_BAKIYE`
- INPUT: `MIKOND`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOKKZ_LIFOFIFO

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `ISTDRM`
- INPUT: `KPBHESAP`
- INPUT: `HESAP`
- INPUT: `EKSART`
- INPUT: `ENV_ONCESI_CIKAN`
- INPUT: `MIKTAR_CIKAN`
- INPUT: `MIKOND`
- INPUT: `STBRFYTOND`
- INPUT: `FIYATOND`
- INPUT: `SUBE_SART`
- INPUT: `EKMLY_EKLE`
- INPUT: `LFFO_IADE_DHET`
- OUTPUT: `BIRIM_FIYATI`
- OUTPUT: `CIKIS_TUTARI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_ALIS_FIYATI_DEGISTIR

**Parametreler:**
- INPUT: `BLMASKODU`
- INPUT: `STOK_DOVIZ_HES_ISLE`
- INPUT: `MASTER_MODUL`
- INPUT: `ALIS_FIYATI_STR`
- INPUT: `KPBSIMGE`
- INPUT: `KAYNAK_FIYAT_DURUMU`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_BARKOD_BUL

**Parametreler:**
- INPUT: `INBARKOD`
- OUTPUT: `BLSTKODU`
- OUTPUT: `BIRIMI`
- OUTPUT: `RST_DURUM`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_BARKOD_BUL_TEK

**Parametreler:**
- INPUT: `INBARKOD`
- INPUT: `INBLSTKODU`
- OUTPUT: `RBLSTKODU`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_BARKOD_BUL_TUMU

**Parametreler:**
- INPUT: `INBARKOD`
- OUTPUT: `BLSTKODU`
- OUTPUT: `BIRIMI`
- OUTPUT: `RST_DURUM`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_DNMRAP

**Parametreler:**
- INPUT: `USERID`
- INPUT: `SART`
- INPUT: `VARYANT_DETAYLI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_ENVANTER

**Parametreler:**
- INPUT: `USERID`
- INPUT: `ENVDRM`
- INPUT: `SART`
- INPUT: `TARIH1`
- INPUT: `TARIH2`
- INPUT: `RAPORHESAP`
- INPUT: `KPBDVZAYIR`
- INPUT: `KALANMIKTAR`
- INPUT: `MIKTAR_ENV`
- INPUT: `ANASTOK_ENVANTER`
- INPUT: `DOVIZ_BRM`
- INPUT: `DONEMSEL_ISTATISTIK`
- INPUT: `SUBEKODU_SART`
- INPUT: `TRSIRS_TOPLAMA`
- INPUT: `EKMLY_EKLE`
- INPUT: `BLOKE_TOPLA`
- INPUT: `VARYANT_DETAYLI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_ENVANTER_DEPO

**Parametreler:**
- INPUT: `USERID`
- INPUT: `SART`
- INPUT: `SUBEKODU_SART`
- INPUT: `DEPO_SART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_FIFO_KALANLAR

**Parametreler:**
- INPUT: `USERID`
- INPUT: `BLSTKODU`
- INPUT: `KPBDVZ`
- INPUT: `DVZBRM`
- INPUT: `KPBDVZAYIR`
- INPUT: `KPB_DVZBRM`
- INPUT: `SON_TARIH`
- INPUT: `EKMLY_EKLE`
- INPUT: `EK_SART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_FIYATLARI_BUL

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `KPBPRBRM`
- INPUT: `DOVIZ_BIRIMI`
- OUTPUT: `KSF1`
- OUTPUT: `KSF2`
- OUTPUT: `KSF3`
- OUTPUT: `KSF4`
- OUTPUT: `KAF1`
- OUTPUT: `KAF2`
- OUTPUT: `KAF3`
- OUTPUT: `KAF4`
- OUTPUT: `DSF1`
- OUTPUT: `DSF2`
- OUTPUT: `DSF3`
- OUTPUT: `DSF4`
- OUTPUT: `DAF1`
- OUTPUT: `DAF2`
- OUTPUT: `DAF3`
- OUTPUT: `DAF4`
- OUTPUT: `KSF_BIRIMI1`
- OUTPUT: `KSF_BIRIMI2`
- OUTPUT: `KSF_BIRIMI3`
- OUTPUT: `KSF_BIRIMI4`
- OUTPUT: `KAF_BIRIMI1`
- OUTPUT: `KAF_BIRIMI2`
- OUTPUT: `KAF_BIRIMI3`
- OUTPUT: `KAF_BIRIMI4`
- OUTPUT: `DSF_BIRIMI1`
- OUTPUT: `DSF_BIRIMI2`
- OUTPUT: `DSF_BIRIMI3`
- OUTPUT: `DSF_BIRIMI4`
- OUTPUT: `DAF_BIRIMI1`
- OUTPUT: `DAF_BIRIMI2`
- OUTPUT: `DAF_BIRIMI3`
- OUTPUT: `DAF_BIRIMI4`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_FIYATLARI_BUL2

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `KPBPRBRM`
- INPUT: `DOVIZ_BIRIMI`
- INPUT: `FIYAT1_IND`
- INPUT: `FIYAT2_IND`
- INPUT: `FIYAT3_IND`
- INPUT: `FIYAT4_IND`
- OUTPUT: `KSF1`
- OUTPUT: `KSF2`
- OUTPUT: `KSF3`
- OUTPUT: `KSF4`
- OUTPUT: `KAF1`
- OUTPUT: `KAF2`
- OUTPUT: `KAF3`
- OUTPUT: `KAF4`
- OUTPUT: `DSF1`
- OUTPUT: `DSF2`
- OUTPUT: `DSF3`
- OUTPUT: `DSF4`
- OUTPUT: `DAF1`
- OUTPUT: `DAF2`
- OUTPUT: `DAF3`
- OUTPUT: `DAF4`
- OUTPUT: `KSF1DT`
- OUTPUT: `KSF2DT`
- OUTPUT: `KSF3DT`
- OUTPUT: `KSF4DT`
- OUTPUT: `KAF1DT`
- OUTPUT: `KAF2DT`
- OUTPUT: `KAF3DT`
- OUTPUT: `KAF4DT`
- OUTPUT: `DSF1DT`
- OUTPUT: `DSF2DT`
- OUTPUT: `DSF3DT`
- OUTPUT: `DSF4DT`
- OUTPUT: `DAF1DT`
- OUTPUT: `DAF2DT`
- OUTPUT: `DAF3DT`
- OUTPUT: `DAF4DT`
- OUTPUT: `KSF_BIRIMI1`
- OUTPUT: `KSF_BIRIMI2`
- OUTPUT: `KSF_BIRIMI3`
- OUTPUT: `KSF_BIRIMI4`
- OUTPUT: `KAF_BIRIMI1`
- OUTPUT: `KAF_BIRIMI2`
- OUTPUT: `KAF_BIRIMI3`
- OUTPUT: `KAF_BIRIMI4`
- OUTPUT: `DSF_BIRIMI1`
- OUTPUT: `DSF_BIRIMI2`
- OUTPUT: `DSF_BIRIMI3`
- OUTPUT: `DSF_BIRIMI4`
- OUTPUT: `DAF_BIRIMI1`
- OUTPUT: `DAF_BIRIMI2`
- OUTPUT: `DAF_BIRIMI3`
- OUTPUT: `DAF_BIRIMI4`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_ISLEM_GORMEYEN

**Parametreler:**
- INPUT: `USERID`
- INPUT: `STOK_SART`
- INPUT: `OLU_STOK_GUN`
- INPUT: `HAREKETSIZ_STOK_GUN`
- INPUT: `DONEM_BASLAMA_TARIHI`
- INPUT: `VARYANT_DETAYLI`
- INPUT: `HR_SART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_KZB

**Parametreler:**
- INPUT: `USERID`
- INPUT: `ISTDRM`
- INPUT: `SART`
- INPUT: `RAPORHESAP`
- INPUT: `ANASTOK_KZ`
- INPUT: `KALAN_ISTDRM`
- INPUT: `TARIH1`
- INPUT: `DONEMSEL_ISTATISTIK`
- INPUT: `SUBE_SART`
- INPUT: `KPBDVZAYIR`
- INPUT: `EKMLY_EKLE`
- INPUT: `VARYANT_DETAYLI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_KZN

**Parametreler:**
- INPUT: `USERID`
- INPUT: `ISTDRM`
- INPUT: `SART`
- INPUT: `TARIH1`
- INPUT: `TARIH2`
- INPUT: `RAPORHESAP`
- INPUT: `ANASTOK_KZ`
- INPUT: `DONEMSEL_ISTATISTIK`
- INPUT: `SUBE_SART`
- INPUT: `KPBDVZAYIR`
- INPUT: `EKMLY_EKLE`
- INPUT: `VARYANT_DETAYLI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_KZ_OZEL

**Parametreler:**
- INPUT: `USERID`
- INPUT: `ISTDRM`
- INPUT: `SART`
- INPUT: `RAPORHESAP`
- INPUT: `KALAN_ISTDRM`
- INPUT: `TARIH1`
- INPUT: `TARIH2`
- INPUT: `DONEMSEL_ISTATISTIK`
- INPUT: `SUBE_SART`
- INPUT: `KPBDVZAYIR`
- INPUT: `EKMLY_EKLE`
- INPUT: `OALAN1`
- INPUT: `OALAN2`
- INPUT: `OALAN3`
- INPUT: `OALAN4`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_RAPOR_FIYAT

**Parametreler:**
- INPUT: `BLSTKODU`
- INPUT: `FIYAT_HESAP`
- INPUT: `SONUC_HESAP`
- INPUT: `FIYAT_NO`
- INPUT: `ALIS_SATIS`
- INPUT: `TARIH`
- OUTPUT: `FIYATI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### STOK_YETERLILIK

**Parametreler:**
- INPUT: `USERID`
- INPUT: `EKSART`
- INPUT: `DONEM_BASLAMA_TARIHI`
- INPUT: `DONEM_BITIS_TARIHI`
- INPUT: `SIPARIS_TALEP_GUN`
- INPUT: `SIPARIS_TOLERANS`
- INPUT: `SIPARIS_YUVARLAMA`
- INPUT: `VARYANT_DETAYLI`

**Kaynak Kodu:** Okunamadı veya boş.

---

### TAKSIT_BAKIYE

**Parametreler:**
- INPUT: `USERID`
- INPUT: `EKSART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### TUPSUGUNCEL

**Parametreler:**
- INPUT: `USERID`
- INPUT: `SART`

**Kaynak Kodu:** Okunamadı veya boş.

---

### VALOR_HESAPLA

**Parametreler:**
- INPUT: `BORC`
- INPUT: `ALACAK`
- INPUT: `VALOR_BORC`
- INPUT: `VALOR_ALACAK`
- OUTPUT: `VL_BORC`
- OUTPUT: `VL_ALACAK`
- OUTPUT: `VALOR`

**Kaynak Kodu:** Okunamadı veya boş.

---

