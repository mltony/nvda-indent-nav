# GirintiDolaşımı #

* Yazar: Tony Malykh
* [Kararlı sürümü indir][1]

Bu eklenti NVDA kullanıcılarının girintiler, satır veya paragraflar arasında
dolaşmasını sağlar.  tarayıcılarda aynı düzeydeki paragrafları ekranın
solundan başlayarak kolayca bulmanıza yardım eder. Örneğin bu şekilde
hiyerarşik bir ağaç görünümündeki birinci seviye açıklamaları
bulabilirsiniz. Ayrıca program dillerindeki kaynak kodlarını düzenlerken,
Aynı düzey girintideki satırlara kolayca gitmenizi sağlar, buna ek olarak da
daha küçük veya daha büyük düzeydeki girinti satırlarını bulmanıza yardım
eder.

## Tarayıcılardaki kullanım
Girinti Dolaşımı eklentisi, ekranın solundan başlayarak aynı düzeyler arası
dolaşım için kullanılabilir. özellikle aynı düzeydeki paragraflar arası
dolaşım için NVDA+Alt+ aşağı veya yukarı yön tuşlarını kullanabilirsiniz.
Örnek olarak bu hiyerarşik açıklama ağaçlarında dolaşımda sadece birinci
seviye açıklamalar arasında gezip diğer tüm seviyeleri atlarken çok yararlı
olabilir (on reddit.com gibi).

Daha net konuşmak gerekirse, GirintiGezintisi NVDA programının ağaç nesne
algılaması sağladığı her uygulamada kullanılabilir.

Kısayollar:

* NVDA+Alt+Yukarı veya aşağı ok: Aynı düzeydeki önceki veya sonraki
  paragrafa gider.
* NVDA+alt+Sol Ok: Daha küçük düzeydeki bir önceki paragrafa gider.
* NVDA+Alt+Sağ ok: Daha büyük düzeydeki bir sonraki paragrafa gider.

## Metin editörlerindeki kullanım
Girinti Dolaşımı eklentisi, birçok programlama dilindeki kaynak kodları
düzenlerken de çok yararlıdır.  Python gibi diller kaynak kodların düzgün
biçimde girintilenmesini gerektirir,  Birçok programda da girintilendirme
şiddetle tavsiye edilir. Girinti Dolaşımı ile NVDA+Alt+Aşağı veya yukarı oka
basarak bir sonraki veya bir önceki aynı girintiye
gidebilirsiniz. NVDA+Alt+Sol oka  basarak bir üst düzeydeki , yani daha
düşük girintideki satıra gidebilirsiniz.  Python içinde geçerli fonksiyon
tanımını ya da sınıf tanımını kolayca bulabilirsiniz.  NVDA+Alt+Sağ oka
basarak da bir alt düzeydeki, yani daha büyük girintideki satıra
gidebilirsiniz.

Eğer NVDA satır girintilerini seslerle çalacak şekilde ayarlandıysa, bu
durumda Girinti Gezintisi eklentisi tüm atlanan satırlar için kısa bir ses
çalacaktır.  Aksi halde atlanan satırları belirtmek için minik bir çıtırtı
çıkaracaktır.

Kısayollar:

* NVDA+Alt+Yukarı veya  aşağı ok: geçerli girinti bloğundaki aynı düzeyde
  olan bir önceki veya bir sonraki satıra gider.
* NVDA+Alt+Control+Yukarı veya aşağı ok: Aynı düzeydeki bir önceki veya bir
  sonraki girintiye gitmeye zorlar. Bu komut gerekirse başka bloklardaki
  aynı düzeye gider. (diğer Python fonksiyonu gibi)..
* NVDA+alt+Sol Ok: Aynı girinti bloğundaki bir yukarı düzey satıra yani daha
  küçük girintiye gider.
* NVDA+Alt+sağ ok: Aynı girinti bloğundaki bir alt düzey satıra yani daha
  büyük girintiye gider.

## Sürüm geçmişi
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Uluslarası destek eklendi.
  * kaynak dosyalarda GPL headers eklendi.
  * küçük hata düzeltmeleri.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * İlk sürüm.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav
