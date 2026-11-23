# EEE213 k-NN Regression — Türkçe konuşma notları

*13 slayt için kısa anlatım taslağı. Süreyi öğretmenin verdiği sunum süresine göre ayarla; ezberlemek yerine grafikleri ve kodu anlamaya odaklan.*

1. **Kapak:** “Bugün k-en yakın komşu regresyonunu ve bu yöntemi bir santralin elektrik üretimini tahmin etmekte nasıl kullandığımı anlatacağım.”
2. **Problem:** “Girdi olarak sıcaklık, vakum, basınç ve bağıl nem kullanıyorum. Çıktı sürekli bir sayı olan PE gücü, MW cinsinden; bu yüzden regresyon.”
3. **Veri:** “UCI veri kümesinde tam yükte çalışan santrale ait 9.568 saatlik gözlem, dört girdi ve bir hedef sütunu var.”
4. **Kalite:** “Eksik veri yok, 41 tekrar var. Hoca ile aynı karşılaştırmayı yapmak için tekrarları korudum. İlk 7.654 eğitim, son 1.914 test.”
5. **Mantık:** “k-NN, benzer giriş koşullarına sahip en yakın k saati bulur ve bu saatlerin PE değerlerinin ortalamasını tahmin olarak verir.”
6. **Ölçekleme:** “Farklı ölçü birimlerine sahip dört özelliği standartlaştırdım. Bu işlem yalnızca her eğitim fold'unun verilerinden öğreniliyor.”
7. **Değerlendirme:** “Test verisine dokunmadan eğitim setinde beş katlı CV uyguladım. k değerini CV hatasına göre seçtim.”
8. **Arama:** “Denediğim k değerleri 1, 3, 5, 10, 20. En düşük ortalama CV MAE, k=3 için 2.763 MW.”
9. **Karşılaştırma:** “Son testte k-NN 2.74 MW MAE verdi. Baseline 14.72, AT doğrusal model 4.33, dört girdili doğrusal model 3.66 MW.”
10. **Bir gözlem:** “İlk test satırında gerçek PE 483.12 MW iken tahmin 484.34 MW. Mutlak fark 1.22 MW.”
11. **Diagnostik:** “Öğrenme eğrisinde daha fazla eğitim verisi ile CV hatasının azaldığını görüyoruz. Kalan hata sıcaklıkla nasıl değişiyor onu da çizdim.”
12. **Önem / sınırlama:** “Model özellikle sıcaklık bilgisinden çok yararlanıyor. Ama permutation importance nedensellik değildir; tekrarlar ve veri kümesinin yalnızca tam yük olması önemli sınırlardır.”
13. **Yeniden üretilebilirlik:** “Bütün sayılar Python dosyamdan üretiliyor. Slaytlar, veri açıklaması, kod, kaynaklar ve AI kullanım beyanı GitHub deposunda olacak.”
