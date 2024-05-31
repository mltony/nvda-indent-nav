# GirintiDolaşımı #

Bu eklenti, NVDA kullanıcılarının satırların girinti düzeyine göre
gezinmesine olanak tanır. Birçok programlama dilinde kaynak kodu
düzenlerken, aynı girinti seviyesindeki satırlar arasında geçiş yapılmasına
olanak sağladığı gibi, daha fazla veya daha az girinti seviyesine sahip
satırları hızlı bir şekilde bulmayı da sağlar. Ağaç görünümlerinde de benzer
tuş vuruşlarını sağlar.

Ağaçta dolaşma komutlarının [Ağaç Dolaşımı
eklentisine](https://github.com/mltony/nvda-tree-nav) taşındığını lütfen
unutmayın.

## İndirmek
Lütfen NVDA eklenti mağazasından yükleyin

## VSCode ile uyumluluk hakkında not

Yerleşik VSCode erişilebilirliği çok sınırlıdır: 2024 itibariyle
erişilebilirlik API'si aracılığıyla yalnızca 500 satır kod açığa çıkarır ve
bu da Girinti Dolaşımı eklentisinin VSCode'da hatalı çalışmasına neden olur.

Varsayılan olarak Girinti Dolaşımı, VSCode ile çalışmaz ve onu kullanmaya
çalıştığınızda iki seçenek arasından seçim yapmanız gerekir:

* VSCode eklentisini yükleyin ([Eklenti
  sayfası](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))
  ([kaynak kodu](https://github.com/mltony/
  vscode-nvda-indent-nav-accessibility)) - önerilen yol. eklentiyi
  yükledikten sonra NVDA, ne kadar büyük olursa olsun belgenin tamamına
  erişebilecektir.
* VSCode'u eski modda kullanmaya devam edin - Girinti Dolaşımı ayarlarında
  bu modu etkinleştirin. NVDA yalnızca 500 satırlık belge göreceği ve kayıp
  kardeşleri/ebeveynleri yanlışlıkla bildireceği için bu önerilmez.

## Uyumluluk sorunları

Girinti Dolaşımı eklentisinin [Karakter Bilgisi
Eklentisiyle](https://addons.nvda-project.org/addons/charInfo.en.html)
uyumluluk sorunları olduğu bilinmektedir. Bu eklenti çalışırken hem Girinti
Dolaşımı eklentisini hem de sayısal tuş takımında inceleme imlecini
yapılandırmak şu anda mümkün değildir. Lütfen bu eklentiyi kaldırın veya
Girinti Dolaşımı'nda alternatif bir tuş vuruşu haritası kullanın.

## Tuş vuruşu düzenleri

Girinti Dolaşımı 3 yerleşik tuş vuruşu eşlemesi sunar:

* Eski veya dizüstü bilgisayar düzeni: Bu, Girinti Dolaşımı v1.x kullanan,
  yeni düzenler öğrenmek istemeyen kişiler veya sayısal tuş takımı olmayan
  dizüstü bilgisayar klavyeleri içindir.
* Alt+sayısal tuş takımı düzeni.
* Sayısal tuş takımı düzeni. İnceleme imleci tuş vuruşu çakışmasını
  gidermenin iki yolu vardır:

    * Düzenlenebilir öğelerde Girinti Dolaşımı için sayısal tuş takımını
      kullanın ve imleci diğer her yerde inceleyin. Düzenlenebilir öğelerde
      hâlâ inceleme imlecini kullanmanız gerekiyorsa, 'alt+Numara kilidi'
      tuşlarına basarak Girinti Dolaşımı'nı geçici olarak devre dışı
      bırakabilirsiniz.
    * İnceleme imleci komutlarını alt+Sayısal tuş takımı'na yeniden eşleyin,
      böylece tuş vuruşu çakışması önlenir.

Tuş vuruşu düzeni Girinti Dolaşımı ayarlarında seçilebilir.

## Tuş vuruşları

| Eylem | Eski Düzen | `Alt+sayısal tuş takımı` Düzeni | Sayısal tuş takımı düzeni | Tanım |
| -- | -- | -- | -- | -- |
| Girinti Dolaşımı'nı aç/kapat | `alt+Numara Kilidi` | `alt+Numara Kilidi` | `alt+Numara Kilidi` | Bu, hem NVDA hem de gözden geçirme imleç hareketleri sayısal tuş takımı'na atandığında kullanışlıdır. |
| Önceki/sonraki kardeşe atla | `NVDA+Alt+yukarı/aşağı Ok` | `alt+sayısal tuş takımı8/sayısal tuş takımı2` | `sayısal tuş takımı8/sayısal tuş takımı2` | Kardeş, aynı girinti seviyesine sahip bir satır olarak tanımlanır.<br>Bu komut, imleci geçerli kod bloğunun ötesine götürmez. |
| Dağınıklığı atlayarak önceki/sonraki kardeşe atla | N/A | `CTRL+alt+sayısal tuş takımı8/sayısal tuş takımı2` | `CTRL+sayısal tuş takımı8/sayısal tuş takımı2` | Dağınıklık normal ifadesini ayarlarda yapılandırabilirsiniz. |
| İlk/son kardeşe atla | `NVDA+Alt+shift+yukarı/aşağı Ok` | `alt+sayısal tuş takımı4/sayısal tuş takımı6` | `sayısal tuş takımı4/sayısal tuş takımı6` | Kardeş, aynı girinti seviyesine sahip bir satır olarak tanımlanır.<br>Bu komut, imleci geçerli kod bloğunun ötesine götürmez. |
| Potansiyel olarak geçerli bloğun dışındaki önceki/son kardeşe atla | `NVDA+control+Alt+yukarı/aşağı Ok` | `CTRL+alt+sayısal tuş takımı4/sayısal tuş takımı6` | `CTRL+sayısal tuş takımı4/sayısal tuş takımı6` | Bu komut başka bir bloktaki kardeşe atlamanızı sağlar. |
| Önceki/sonraki ebeveyne atla | `NVDA+Alt+sol ok`,<br>`NVDA+alt+CTRL+sol ok` | `alt+sayısal tuş takımı7/sayısal tuş takımı1` | `sayısal tuş takımı7/sayısal tuş takımı1` | Ebeveyn, daha düşük girinti seviyesine sahip bir satır olarak tanımlanır. |
| Önceki/sonraki çocuğa atla | `NVDA+Alt+CTRL+sağ ok`,<br>`NVDA+alt+sağ ok` | `alt+sayısal tuş takımı9/sayısal tuş takımı3` | `sayısal tuş takımı9/sayısal tuş takımı3` | Çocuk, girinti düzeyi daha yüksek olan bir satır olarak tanımlanır.<br>Bu komut, imleci geçerli kod bloğunun ötesine götürmez. |
| Geçerli bloğu seç | `NVDA+CTRL+i` | `CTRL+alt+sayısal tuş takımı7` | `CTRL+sayısal tuş takımı7` | Geçerli satırı ve kesinlikle daha yüksek girinti düzeyine sahip olan tüm sonraki satırları seçer.<br>Birden fazla blok seçmek için art arda basın. |
| Geçerli bloğu ve aynı girinti düzeyindeki tüm sonraki blokları seç | `NVDA+alt+i` | `CTRL+alt+sayısal tuş takımı9` | `CTRL+sayısal tuş takımı9` | Geçerli satırı ve daha büyük veya eşit girinti düzeyine sahip sonraki tüm satırları seçer. |
| Girinti-yapıştır | `NVDA+v` | `NVDA+v` | `NVDA+v` | Bir kod bloğunu farklı girinti düzeyine sahip bir yere yapıştırmanız gerektiğinde, bu komut yapıştırmadan önce girinti düzeyini ayarlayacaktır. |
| Geçmişte geri/ileri git | N/A | `CTRL+alt+sayısal tuş takımı1/sayısal tuş takımı3` | `CTRL+1/sayısal tuş takımı3` | Girinti Dolaşımı, Girinti Dolaşımı komutları aracılığıyla ziyaret ettiğiniz satırların geçmişini tutar. |
| Geçerli satırı konuş | N/A | `alt+sayısal tuş takımı5` | `sayısal tuş takımı5` | Bu gerçekten kolaylık sağlamak için yeniden eşlenen bir inceleme imleci komutudur. |
| Ebeveyn satırını konuş | `NVDA+i` | N/A | N/A | |

## Diğer özellikler

### Hızlı Bul yer imleri

Girinti Dolaşımı, kolayca atlayabileceğiniz istediğiniz sayıda yer imini
yapılandırmanıza olanak tanır. Yer imi, normal bir ifadeyle ve bir eşleşmeye
atlamak için özel bir tuş vuruşuyla tanımlanır. Önceki oluşumu bulmak için
'shift+' tuş vuruşuna basın.

### Çıtırtı:

Birçok kod satırının üzerinden atlarken, Girinti Dolaşımı, satırların
tonları atlandıkça girinti seviyelerini hızlı bir şekilde oynatmaya
çalışacaktır. Bu özellik yalnızca NVDA ayarlarında ton olarak rapor
girintisi açıkken etkinleştirilir. çıtırtı sesi Girinti Dolaşımı ayarlarında
ayarlanabilir veya devre dışı bırakılabilir.

## Kaynak kodu

Kaynak kodu şu adreste mevcuttur:
<http://github.com/mltony/nvda-indent-nav>.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav
