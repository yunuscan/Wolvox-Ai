# Wolvox Firebird Veritabanı Keşif ve Dokümantasyon Görevi

Bu dosyayı Antigravity'ye (veya benzer bir AI kod ajanına) doğrudan yapıştırabilirsin. Görev, ajanın veritabanına bağlanıp kendi kendine keşif yapması ve sonunda sana geliştirme için kullanılabilir bir dokümantasyon üretmesi üzerine kurgulanmıştır.

---

## KULLANIMDAN ÖNCE SENİN DOLDURMAN GEREKENLER

Prompt'u ajana vermeden önce aşağıdaki alanları kendi ortamına göre doldur:

```
FIREBIRD_HOST: localde çalışıyor 
FIREBIRD_PORT: 3050
FIREBIRD_DB_PATH: C:\AKINSOFT\Wolvox9\Database_FB\DEMOWOLVOX\2026\WOLVOX.fdb
FIREBIRD_USER: RAPORCU
FIREBIRD_PASSWORD: Raporcu2
FIREBIRD_VERSION: 2.5.6.27020
ÇIKTI_KLASÖRÜ: bu klasör
```

---
```
Sen bir veritabanı analiz ajanısın. Görevin, Akınsoft Wolvox ERP Retoran ve hızlı satış yazılımının kullandığı
Firebird veritabanına SADECE OKUMA amaçlı bağlanıp, şemayı, tabloları, ilişkileri ve iş
mantığını analiz ederek bir yazılım geliştiricinin bu veritabanı üzerine harici bir
uygulama (AI destekli chatbot, mobil app, web paneli vb.) geliştirebilmesi için
kullanılabilir, eksiksiz bir teknik dokümantasyon üretmektir.

## BAĞLANTI BİLGİLERİ
Host: localde çalışıyor
Port: 3050
Veritabanı yolu: C:\AKINSOFT\Wolvox9\Database_FB\DEMOWOLVOX\2026\WOLVOX.fdb
Kullanıcı: RAPORCU
Şifre: Raporcu2
Firebird sürümü: 2.5.6.27020
ÇIKTI_KLASÖRÜ: ./wolvox-docs/

## KESİN KURALLAR (İhlal edilemez)
1. Veritabanına SADECE SELECT sorguları çalıştır. INSERT, UPDATE, DELETE, DDL
   (CREATE/ALTER/DROP) komutlarını ASLA kullanma. Bağlantı zaten salt-okunur
   yetkili bir kullanıcıyla yapılacak, ama sen de kod tarafında hiçbir yazma
   komutu üretme veya çalıştırma.
2. Herhangi bir sorgu çalıştırmadan önce, o sorgunun canlı sistemde kilitlenme
   (lock) veya performans sorununa yol açıp açmayacağını düşün. Çok büyük
   tablolarda (örn. stok hareket, cari hareket) `SELECT FIRST 50 *` gibi
   limitli sorgular kullan, tüm tabloyu tek seferde çekme.
3. Wolvox aynı anda gerçek kullanıcılar tarafından kullanılıyor olabilir.
   Ağır/karmaşık JOIN'li analiz sorgularını art arda hızlı şekilde çalıştırma;
   sorgular arası makul bekleme bırak.
4. Bağlantı bilgilerini (şifre dahil) ürettiğin dokümantasyon dosyalarına
   asla yazma veya loglama. Sadece şema, tablo, kolon, ilişki ve örnek/anonim
   verileri dokümante et.
5. Kişisel veri içerebilecek örnek kayıtlarda (cari adı, telefon, adres,
   TC kimlik no gibi alanlar) gerçek değerleri dokümantasyona kopyalama;
   bunun yerine alan adını, veri tipini ve "örnek: [ANONIMLEŞTIRILDI]" notunu yaz.

## ÇALIŞMA ADIMLARI

### Faz 0 — Bağlantı Testi
- Verilen bilgilerle veritabanına bağlan (Python için `fdb` veya `firebird-driver`
  kütüphanesi kullanılabilir; hangisi ortamda kuruluysa onu tercih et, gerekirse
  `pip install firebird-driver` ile kur).
- Bağlantı başarılıysa Firebird sürümünü (`SELECT rdb$get_context('SYSTEM','ENGINE_VERSION') FROM rdb$database;`
  veya bağlantı nesnesinin sürüm bilgisiyle) doğrula ve kaydet.
- Bağlantı başarısızsa hata mesajını olduğu gibi bana raporla, devam etme.

### Faz 1 — Genel Şema Envanteri
- Sistem tablolarını (`RDB$RELATIONS`, `RDB$RELATION_FIELDS`, `RDB$FIELDS`,
  `RDB$INDICES`, `RDB$INDEX_SEGMENTS`, `RDB$REF_CONSTRAINTS`,
  `RDB$RELATION_CONSTRAINTS`, `RDB$GENERATORS`, `RDB$TRIGGERS`,
  `RDB$PROCEDURES`) sorgulayarak:
  - Kullanıcı tablolarının tam listesini çıkar (sistem tabloları hariç,
    `RDB$SYSTEM_FLAG = 0` filtresiyle).
  - Her tablo için: kolon adları, veri tipleri, null olabilirlik, default
    değerler.
  - Primary key ve foreign key ilişkilerini (hangi tablo hangi tabloya
    hangi kolonla bağlı) çıkar.
  - Tanımlı tüm index'leri listele.
  - Tanımlı tüm generator/sequence'leri listele (bunlar otomatik artan
    ID'ler için kritik — isimlerini ve mevcut değerlerini not et).
  - Tanımlı trigger'ların isimlerini ve (mümkünse) kaynak kodunu çıkar
    (`RDB$TRIGGER_SOURCE`). Trigger'lar, bir tabloya yazıldığında Wolvox'un
    arka planda başka hangi tabloları/alanları otomatik güncellediğini
    anlamak için EN KRİTİK bilgi kaynağıdır.
  - Tanımlı stored procedure'leri listele ve kaynak kodlarını çıkar
    (`RDB$PROCEDURE_SOURCE`).

### Faz 2 — İş Alanına Göre Öncelikli Tabloları Belirle ve Derinlemesine İncele
Aşağıdaki iş alanlarıyla ilgili olabilecek tabloları isimlerinden tahmin et
(Türkçe kısaltmalar olabilir: STOK, CARI, FATURA, KASA, BANKA, CEK, SENET,
DEPO, GRUP, KDV, PERSONEL, SIPARIS vb.) ve bulduklarını doğrula:
  - **Stok kartları** ve ilişkili tablolar (grup/kategori, birim, KDV oranı,
    barkod, depo bazlı stok, fiyat listesi tabloları)
  - **Cari kartları** (müşteri/tedarikçi) ve ilişkili tablolar (cari grup,
    risk/limit, adres, vergi dairesi bilgisi)
  - **Fatura / irsaliye başlık ve detay tabloları**
  - **Kasa / banka hareket tabloları**
  - **Sipariş tabloları**
  - Bulunan her ana tablo için, o tabloya bağlı (foreign key ile) TÜM alt/yan
    tabloları da haritaya dahil et. Örneğin bir "stok ekleme" işleminin kaç
    farklı tabloyu etkileyebileceğini bu ilişkilerden çıkar.

### Faz 3 — Referans/Lookup Tablolarını Çöz
Stok grubu, KDV oranı, birim, departman, cari grubu gibi alanlar genelde
kod (örn. "1", "3") olarak tutulur ve gerçek anlamı ayrı bir referans
tablosunda saklanır. Bu tabloları bul ve TÜM içeriğini (kod → açıklama
eşleşmesi) tam olarak dokümantasyona ekle. Bu, senin daha sonra AI ile
"kuru fasulye" gibi bir girdiyi doğru gruba/KDV oranına eşlemen için
mutlaka gerekli olacak. Örnek çıktı formatı:

| Kod | Açıklama |
|-----|----------|
| 1   | Bakliyat |
| 2   | Temizlik |
| ... | ...      |

### Faz 4 — Örnek Veri ile Doğrulama
Her ana tablodan (kişisel veri içermeyenlerden) `SELECT FIRST 5 *` ile
örnek satırlar çek ve gerçek verinin şemayla tutarlı olup olmadığını
doğrula. Kişisel veri içeren tablolarda (CARI gibi) sadece kolon
isimlerini ve veri tiplerini dokümante et, örnek satır ekleme.

### Faz 5 — Yazma İşlemleri İçin Risk ve Yöntem Notu Üret (Kod Yazma, Sadece Analiz)
Bu veritabanına gelecekte "stok ekleme", "cari ekleme", "cari güncelleme"
gibi yazma işlemleri yapılacak bir uygulama geliştirilecek. Bu fazda
HİÇBİR YAZMA İŞLEMİ YAPMADAN, sadece trigger ve foreign key analizinden
yola çıkarak şu soruları cevapla ve dokümana ekle:
  - "Yeni bir stok kartı eklemek" için minimum hangi tablolara hangi
    sırayla yazılması gerekiyor gibi görünüyor? (Trigger'lardan ve
    NOT NULL/foreign key zorunluluklarından çıkarım yap.)
  - Hangi generator'lar bu işlem sırasında kullanılıyor olabilir?
  - Zorunlu (NOT NULL, default'u olmayan) alanlar neler?
  - Aynı işlem "cari kart ekleme" için ayrıca yapılmalı.
  - Bu çıkarımların KESİN olmadığını, gerçek Wolvox arayüzünden manuel
    bir kayıt eklenip trigger loglarıyla/before-after veri karşılaştırmasıyla
    doğrulanması gerektiğini dokümanda açıkça belirt.

## ÇIKTI FORMATI
Aşağıdaki dosyaları {ÇIKTI_KLASÖRÜ} altına oluştur:

1. `01-genel-bakis.md` — Firebird sürümü, toplam tablo sayısı, tespit
   edilen ana iş modülleri (stok, cari, fatura vb.) özeti.
2. `02-tablo-sozlugu.md` — Her tablo için: tablo adı, tahmini amacı,
   tüm kolonlar (ad, tip, null durumu), primary key, foreign key'ler.
3. `03-iliski-haritasi.md` — Tablolar arası foreign key ilişkilerinin
   metinsel/liste halinde haritası (mümkünse ayrıca bir Mermaid ER
   diyagramı da ekle).
4. `04-referans-tablolari.md` — Faz 3'te çıkarılan tüm kod→açıklama
   eşleşmeleri (KDV, grup, birim, departman vb.) tam liste halinde.
5. `05-generator-ve-trigger-envanteri.md` — Tüm generator isimleri,
   tüm trigger isimleri ve (varsa) kaynak kodları, hangi tabloyla ilişkili
   oldukları.
6. `06-yazma-islemi-risk-notu.md` — Faz 5'in çıktısı: stok/cari ekleme
   gibi işlemler için tahmini gereksinimler ve doğrulanması gereken
   noktalar listesi.
7. `07-acik-sorular.md` — Analiz sırasında netleştirilemeyen, insan
   doğrulaması gereken noktaların listesi (örn. "X tablosunun amacı
   isminden anlaşılamadı", "Y trigger'ının kaynak kodu okunamadı" gibi).

Her dosyanın başına hangi tarihte, hangi Firebird sürümü ve hangi Wolvox
kurulumu üzerinde bu analizin yapıldığını yazan bir üst bilgi ekle —
Wolvox güncellemelerinde şema değişebilir, bu yüzden dokümantasyonun
"tarihli" olması önemli.

## İŞ BİTİNCE BANA RAPORLA
- Kaç tablo, kaç trigger, kaç generator bulundu (özet sayılar).
- Faz 5'teki risk notunda hangi belirsizlikler kaldı.
- Dokümantasyonun hangi kısımlarının manuel doğrulama (gerçek Wolvox
  arayüzünden test kaydı girip karşılaştırma) gerektirdiğini net şekilde
  vurgula.
```

---

## Prompt'u kullandıktan sonra senin yapman gereken ek adım

Ajan dokümantasyonu çıkardıktan sonra, **yazma (INSERT/UPDATE) mantığını doğrulamak için** şunu mutlaka manuel yap (bu kısmı hiçbir ajan senin yerine güvenli şekilde yapamaz):

1. Wolvox arayüzünden elle bir test stok kartı oluştur (test veritabanında).
2. Bu işlemden hemen önce ve hemen sonra, ajanın Faz 5'te belirlediği tablolardan `SELECT COUNT(*)` ve son eklenen satırları karşılaştır.
3. Hangi tablolara kaç satır eklendiğini, hangi generator değerlerinin arttığını gözlemle.
4. Bu gözlemi ajana geri ver, dokümantasyonu bu gerçek veriyle güncellet.

Bu adım, "tahmine dayalı şema analizi"ni "gerçek doğrulanmış davranışa" dönüştürmek için gerekli — aksi halde yazma işlemleri sırasında öngörmediğin bir tabloyu atlayıp Wolvox'ta tutarsız kayıt oluşturma riskin yüksek kalır.
