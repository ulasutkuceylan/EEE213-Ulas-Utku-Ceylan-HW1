# GitHub'a yükleme ve teslim — Türkçe rehber

## Ön kontrol

- **Depo:** https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1
- **GitHub Pages:** https://ulasutkuceylan.github.io/EEE213-Ulas-Utku-Ceylan-HW1/
- **Proje kabulü:** Bu dosyalar, hocanın 9. hafta çekiliş numaranı **4** verdiği varsayımıyla hazırlanmıştır. Çekiliş numarasını doğrula. Farklı numaraysa k-NN yöntemi ve sayısal problem buna göre değişmelidir.

## A. Dosyaları GitHub'a yükle (tarayıcı)

1. ZIP dosyasını **bilgisayarında açıp bir klasöre çıkart**. ZIP'i tek parça yükleme.
2. Yukarıdaki depoyu aç. **Code** sayfasında `Add file` → `Upload files` seç.
3. Çıkarılan proje klasörünün **içindeki** dosya ve klasörleri (`code`, `data`, `lab`, `figures`, `slides`, `index.md`, `numerical.md`, `model.md`, `presentation.md`, `code.md`, `requirements.txt`, `README.md`, `results.json`, `numerical_results.json` vb.) sürükleyerek yükle. Chrome'da klasör sürükleme korunmuyorsa aşağıdaki B yöntemini kullan.
4. `Commit changes` seç ve değişiklikleri `main` dalına kaydet. `index.md` ve dört `.md` sayfası deponun **en üst dizininde** bulunmalı.
5. Depoda `code/numerical.py`, `lab/knn_project.py`, `data/ccpp.csv`, `slides/*.pptx`, `figures/*.png` ve doküman dosyaları görünmeli.
6. Bazı yüklemelerde aynı adda dosyalar için tarayıcı geçerli dosyayı değiştirmeyebilir. Bu durumda **Git komut satırı ile B yöntemini** kullan.

## B. Daha güvenilir: Git for Windows + PowerShell

1. Bilgisayarında `git --version` ile Git'in kurulu olduğunu kontrol et. Kurulu değilse resmi siteden Git for Windows yükle: https://git-scm.com/downloads/win.
2. ZIP dosyasını örneğin `C:\Users\ASUSROG\Desktop\EEE213_Tam_Proje_Paketi` klasörüne çıkart.
3. PowerShell'de şu komutları kullan (dosya yolunu gerektiği gibi düzenle):

```powershell
cd "$env:USERPROFILE\Desktop"
git clone https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1.git
# ZIP'ten çıkardığın klasörün içindekileri klonlanan deponun içine kopyala:
robocopy "$env:USERPROFILE\Desktop\EEE213_Tam_Proje_Paketi" "$env:USERPROFILE\Desktop\EEE213-Ulas-Utku-Ceylan-HW1" /E /XD .git .venv __pycache__
cd "$env:USERPROFILE\Desktop\EEE213-Ulas-Utku-Ceylan-HW1"
git add .
git commit -m "Complete EEE213 project site, numeric solution and presentation"
git push origin main
```

`robocopy` 1–7 gibi çıkış kodları bazı dosyaların kopyalandığını ifade eder; otomatik olarak hata olduğu anlamına gelmez. GitHub hesabı için oturum açma penceresi gelebilir. Parola veya token bilgilerini proje dosyalarına yazma.

Alternatif: Proje klasöründeki `UPLOAD_TO_GITHUB.bat` dosyası yüklü Git üzerinden aynı işlemleri otomatikleştirmeye yardımcı olur. Bu dosyanın önce içeriğini okuyabilir, sonra çalıştırabilirsin.

## C. GitHub Pages'i aç

1. https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1/settings/pages adresine git.
2. `Build and deployment`: **Deploy from a branch** seç.
3. `main` dalı ve `/(root)` klasörünü seç, `Save`.
4. GitHub Actions / Pages yayınlama işleminin bitmesini bekle; gerekirse `Actions` sekmesindeki Pages derleme hatalarına bak.
5. https://ulasutkuceylan.github.io/EEE213-Ulas-Utku-Ceylan-HW1/ adresini aç. Dört menünün her birini tek tek test et.
6. Sitenin açıldığını **ben uzaktan kesin doğrulayamıyorum**. Açılmadan Google Form 7.4'ün 2. ve 3. kutularını doğrulandı diye işaretleme.

## D. Python kodunu kendi bilgisayarında çalıştır

Yeni klasörün içinde Terminal/PowerShell aç. Eski PyCharm `.venv` ortamını değiştirmemek için **bu projeye özel yeni sanal ortam** oluştur. `Activate.ps1` çalıştırmaya gerek yok:

```powershell
py -3.13 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" code/run_all.py
```

`py` komutu bulunamazsa `python -m venv .venv` kullan; Python 3.13 seçili olmasına dikkat et. Bu komut önceki Python paketlerine müdahale etmez. Kod, `w09.py`, `knn_project.py`, `numerical.py` ve sonuç doğrulamasını sırayla çalıştırır. Kendi konsol çıktını kaydet ve sitedeki değerlerle karşılaştır.

## E. Teslim öncesi kontrol

- [ ] Çekiliş numaram gerçekten 4.
- [ ] 7.1'de kendi gerçek çekiliş numaram var.
- [ ] 7.2'de public repository adresi var.
- [ ] 7.3'te çalışan GitHub Pages adresi var.
- [ ] 7.4'teki üç şartın tamamı bizzat doğrulandı.
- [ ] 6.1'de eski `lab/w09.py` kalıcı commit bağlantısı geçerli (kod değiştiyse yeni permalink oluştur).
- [ ] `python code/run_all.py` veya açık `.venv` komutu hatasız çalışıyor.
- [ ] Sitenin dört sayfası ve PPTX/PDF bağlantıları açılıyor.
- [ ] Sunum için 4 dakika prova yaptım ve sınıf sunumu dosyasını açabiliyorum.
- [ ] Sayısal problemde türev, birimler, iterasyonlar ve bağımsız kontrolü açıklayabiliyorum.
- [ ] AI kullanımı açıklaması kendi kullanımımı doğru yansıtıyor.
- [ ] İstenen Google Form veya diğer ders teslimi süre dolmadan gönderildi.

**Not:** ZIP bu ortamda üretildi. Senin GitHub hesabına otomatik yazma denemesi bağlantının 403 `Resource not accessible by integration` hatası nedeniyle başarısız oldu; buradaki B yöntemiyle GitHub'a gönderme işlemini kendi Git oturumundan tamamlaman gerekiyor.
