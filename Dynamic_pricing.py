
# PRICING: Item fiyatı ne olmalı!
# Bir oyun şirketi bir oyununda kullanıcılarına item satın alımları için hediye paralar vermiştir.
# Kullanıcılar bu sanal paraları kullanarak karakterlerine çeşitli araçlar satın almaktadır. Oyun şirketi bir item
# için fiyat belirtmemiş ve kullanıcılardan bu item'ı istedikleri fiyattan almalarını sağlamış. Örneğin kalkan
# isimli item için kullanıcılar kendi uygun gördükleri miktarları ödeyerek bu kalkanı satın alacaklar.
# Örneğin bir kullanıcı kendisine verilen sanal paralardan 30 birim, diğer kullanıcı 45 birim ile ödeme yapabilir.
# Dolayısıyla kullanıcılar kendilerine göre ödemeyi göze aldıkları miktarlar ile bu item'ı satın alabilirler.
#
# Çözülmesi gereken problemler:
# Item'in fiyatı kategorilere göre farklılık göstermekte midir? İstatistiki olarak ifade ediniz.
# İlk soruya bağlı olarak item'ın fiyatı ne olmalıdır? Nedenini açıklayınız?
# Fiyat konusunda "hareket edebilir olmak" istenmektedir. Fiyat stratejisi için karar destek sistemi oluşturunuz.
# Olası fiyat değişiklikleri için item satın almalarını ve gelirlerini simüle ediniz.

import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import itertools
import statsmodels.stats.api as sms

pd.set_option('display.max_columns', None)
df= pd.read_csv("/Users/tugcedogan/Downloads/pricing.csv",sep=";")

df.head()
df.shape
df.isnull().sum()

#category id bir kategorik değişken olduğu için object tipine dönüştürüldü
df["category_id"].value_counts()
a = df["category_id"].unique()
print(a)
df.groupby("category_id").agg(["mean","count","median"])

# NOT: Median değerleri ile Mean değerleri arasında çok büyük farklılık var. Outlier değerler olduğu AÇIK.
# bu sebeple outlier değerleri baskılayacağız "def outlier_thresholds" ve  "def replace_with_thresholds" ile

#Ikili gruplara ayir. Mesela ilk gruplama [489756, 361254]

'''import itertools
df_keys = {"201436":'df_1', "326584":"df_2", "361254":"df_3", "489756":"df_4", "675201":"df_5", "874521":"df_6"}
liste = list(itertools.combinations(df_keys,2))
type(liste)
df_list= pd.DataFrame(liste)
df_list'''

# df combinations:
#combn = list(itertools.combinations(df_keys, 2))




# combn[i][0] and combn[i][1]


# YORUM: outlier'ı hesaplama: 1.quartile ile 3. quartile arasındaki farkı alıp (interquartile) bunun 1.5 katını alıp
# 1.ve 3. quartile lara ekliyoruz böylece dışa düşenleri buluyoruz.
# normalde üst taraf(up_limit) için %75 noktasında göre, alt taraf(low_limit) % 25 noktasına göre yapıyoruz
# aşağıdaki def outlier_thresholds fonk da quartile'lar değiştireceğimiz şekilde tanımlanmış.
# üst taraf için %98 alt taraf için %2 tanımladık.Acaba bu limitler uç değerleri baskılamak için yeterli mi? bunun kotrolünü describe ile bakabiliriz


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.02)
    quartile3 = dataframe[variable].quantile(0.98)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


#outlier baskilamadan sonra sirasiyla id,mean, median

replace_with_thresholds(df,"price")
df.describe().T
df.describe([0.01,0.05,0.15,0.25,0.50,0.75,0.95,0.96,0.97,0.98,0.99]).T

df.groupby("category_id").agg({"price": ["mean","median", "count"]})

# YORUM  üst taraf için %98 alt taraf için %2 tanımladığımızda da halen mean ve median arasında çarpıklık görüyoruz
# demekki %2 ve %98 yeterli olmamaış. aralığı genişleterek biraz daha fazla uç değeri kapsatalım;
# datayı burada capping yapıyorum yani aykırıları üst ve alt değere eşitliyorum veri kaybım yok..

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.02)
    quartile3 = dataframe[variable].quantile(0.85)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


#outlier baskilamadan sonra sirasiyla id,mean, median

replace_with_thresholds(df,"price")
df.describe().T
df.describe([0.01,0.05,0.15,0.25,0.50,0.75,0.95,0.96,0.97,0.98,0.99]).T

df.groupby("category_id").agg({"price": ["mean","median", "count"]})

import matplotlib.pyplot as plt


df.info()
df["price"].value_counts()
plt.hist(x=df["price"],bins=150)
plt.show()
# boxplot ile son capping yaptığımız halinin grafiğini çizmek istersek;
sns.catplot(x="category_id",y="price",data=df, kind="box")
plt.show()

'''
for
    # shapiro testi kodu
    if shapiro_results p>0.05:
        # levene testi kodu ->varyans homojenligi
            if varyans homojen ise:
                # parametrik ve equal_var =True kullan.
            else:
                 # parametrik ve equal_var =False kullan.
    else:
        non_parametrik test
'''
EK BİLGİ: n >30 olması, dağılımı kesikli den sürekliliğe doğru değiştirdiği için (MLT gereği) kritik bir noktadır n in 30 olması
# pazar araştırmalarında n hatta 40 alınır ki aykırı gözlemleri elediğinde(yaklaşık %5 civarı) ya da baskıladığında veri kaybı çok olmasın, yeterli büyüklüğü sağlayalım.


# itertools ile aşağıda "category_id" içerisindekileri 2'li gruplatıyoruz, 2 li KARŞILAŞTIRMA yapmak istiyoruz çünkü

import itertools
group_list = []
for i in itertools.combinations(df["category_id"].unique(), 2):
    group_list.append(i)

group_list
#df["category_id"].unique()

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dagilim varsayimi sağlanmamaktadır.

#p<0.05 -> H0 red. Normal dagilmamaktadir.
#p>0.05 ->  H0 reddedilemez. Normal dagilmaktadir.

# H0: anlamli farklilik yoktur.
# H1: anlamli farklilik vardir.

from scipy import stats
def ab_test(group_a,group_b):
    grb_a = df.loc[df["category_id"] == group_a,"price"]
    grb_b = df.loc[df["category_id"] == group_b, "price"]
    norm_a = stats.shapiro(grb_a)[1] >= 0.05
    norm_b = stats.shapiro(grb_b)[1] >= 0.05

    if norm_a and norm_b:
        var_h = stats.levene(grb_a,grb_b)[1] >= 0.05
        if var_h:
            t_test1= stats.ttest_ind(grb_a,grb_b,equal_var=True)[1]>=0.05
            if t_test1:
                print(f"{group_a} ve {group_b} param ve vary eşit-ortalamalari arasinda istatiksel anlamli farklilik yoktur")
            else:
                print(f"{group_a} ve {group_b} param ve vary eşit-ortalamalari arasinda istatiksel anlamli farklilik vardir")
        else:
            t_test2 = stats.ttest_ind(grb_a, grb_b, equal_var=False)[1] >= 0.05
            if t_test2:
                print(f"{group_a} ve {group_b} param ama vary eşit-ortalamalari arasinda istatiksel anlamli farklilik yoktur")
            else:
                print(f"{group_a} ve {group_b} param ama vary eşit-ortalamalari arasinda istatiksel anlamli farklilik vardir")
    else:
        t_test3 = stats.mannwhitneyu(grb_a, grb_b)[1] >= 0.05
        if t_test3:
            print(f"{group_a} ve {group_b} nonparam-ortalamalari arasinda istatiksel anlamli farklilik yoktur")
        else:
            print(f"{group_a} ve {group_b} nonparam-ortalamalari arasinda istatiksel anlamli farklilik vardir")



# tüm olası 2'li kombinasyon grupları içerisinde döndürmek istersek yukarıda yazdığımız fonk u for döngüsüne yerleştirmeliyiz;
for groups in group_list:
    ab_test(groups[0],groups[1])
# buradan çıkan sonuça göre; item fiyatı kategorilerin bir kısmına göre farklılık gösteriyor

######################################################################################
# SORU 2 İlk soruya bağlı olarak item'ın fiyatı ne olmalıdır? Nedenini açıklayınız
######################################################################################
#  Ürün AYNI olduğundan her kategori için ortalama bir fiyat vermek  mantıklı seçenek olabilir.
#  ürünü özelleştirip kategori özelinde, biri renkli olsun, birinin şeklinde farklılık olsun vs. o zaman fiyat farklılaştırmasına gitmek mantıklı olabilir.
# tek fiyat belirleme noktasında da;
# bir yöntem olarak; bir kategorinin medyanına bakıp fiyatı öyle belirleyebilirim diyebiliriz.
# Fakat o zamanda meydanı almış olduğumuz için verinin %50 sini otomatikman kaybetmiş olacağız. biliyoruz ki medyan orta nokta ve insanlar en yüksek medyan değeri olan 35.6 ya çıkmıyorlar
# bir başka yöntem olarak; bizim için kritik olan en büyük ve 2. büyük segment olabilir, en büyük segment 43.09 2. büyük segment 39.27 mean olarak fiyat çıkmış.

# 489756 ve 326584 için ayrı ayrı medyan değerleri fiyat olarak belirlenebilir
# 489756 ve 326584 nin mean price'i genelden yüksek fakat median değeri genele yakın

# count değeri 1705 olan grup 489756 fiyatı belirlemede (içerisinde halen biraz da olsa aykırı değerler var olsa da) yol gösterici.

df.groupby("category_id").agg(["mean","median","count","max","std"])

df.loc[df["category_id"] == 489756 ,"price"].median()

# başka bir yöntem; ortalama bir fiyat bulmak. medyana göre alt ve üst değeri almayıp ortadaki değerlere göre ort almak.(diğerleri ile aralarında anlamlı farklılık çıkaran grupları da almamak olabilir)
# yani 326584 ve 489756 grupları alma-genel kanaatin dışına çıkma yani
cat=[361254, 874521, 675201 ,201436]
total_price=0
for i in cat:
    total_price+= df.loc[df["category_id"]==i, "price"].mean()
price_ort=total_price/len(cat)
print(price_ort)
# bu yöntem ile tüm kategoriler için 37.32 price_ort kullanılabilir.


# DAGILIM NORMALSE daha optimum bir yöntem; "cut of point" yöntemi ile 30 verdim kaç kişi geldi ne kadar ciro elde ettim? 31 verdim kaç kişi geldi ne kadar ciro elde ettim..gibi %sel dağılım yapıp optimum noktayı bulabililrz
# EĞİMİN BOZULDUĞU YER KARAR NOKTAMIZ-cut of point. AUC İLE de bakabiliriz
# "one western door price sensitivity" diye hedef kitlenin alırım-almam kararını ölçen bir yöntem
# "conjoint analizi" ile tüketici önüne farklı seçenekler çıkararak pazara sunulur

above_avg=df.loc[df["price"] >=30, "price"].mean()
above_no=df.loc[df["price"] >= 30, "price"].count()

# sadece sonuçlarını yazdırmak istersek;
def dyn_price(dataframe):
    price_range=range(30,50)
    for i in price_range:
        above_avg=df.loc[df["price"] >=i, "price"].mean()
        above_no=df.loc[df["price"] >= i, "price"].count()
        perc= (df.loc[df["price"] >= i, "price"].count())/df.shape[0]
        incomes=above_no*i
        print(f"above price {i}: count: {above_no} ")
        print('above avg = %.2f, percentage = %.2f, total income = %.2f' % (above_avg, perc, incomes))

dyn_price(df)

#grafik ile çıktı oluşturmak istersek;
import seaborn as sns

count_list=[]
incomes_list=[]
perc_list=[]
def dyn_price(dataframe):
    price_range=range(20,50)
    for i in price_range:
        above_avg=df.loc[df["price"] >=i, "price"].mean()
        above_no=df.loc[df["price"] >= i, "price"].count()
        count_list.append(above_no)
        perc=(df.loc[df["price"] >= i, "price"].count())/df.shape[0]
        perc_list.append(perc)
        incomes=above_no*i
        incomes_list.append(incomes)
    return count_list, perc_list, incomes_list

count_list,perc_list,incomes_list=dyn_price(df)

df_plot=pd.DataFrame({"incomes list": incomes_list, "perc list": perc_list, "count list":count_list})
sns.scatterplot(x="incomes list",y="perc list" , hue= "count list", data=df_plot)
plt.show()

sns.barplot(x="incomes list",y="perc list" , hue= "count list", data=df_plot,dodge=False)
plt.show()

sns.catplot(x="incomes list",y="perc list" ,
            data=df_plot, kind="bar",
            height=5, aspect=0.8)
plt.show()

plt.plot(incomes_list,perc_list,)
plt.show()



######################################################################################
# SORU 3 Fiyat konusunda "hareket edebilir olmak" istenmektedir.
# Fiyat stratejisi için karar destek sistemi oluşturunuz
######################################################################################

# belirleyici sınıfın fiyatlarını biraraya getirelim
prices=[]
for category in cat:
    for i in df.loc[df["category_id"]==category,"price"]:
        prices.append(i)
sms.DescrStatsW(prices).tconfint_mean()

# fiyat aralığı  (37.01473696902742, 38.23164818970205) arasında seçilmelidir.

######################################################################################
# SORU 4 Olası fiyat değişiklikleri için item satın almalarını ve
# gelirlerini simule edin
######################################################################################

#fiyatın güven aralığının altında olması durumunda elde edilecek gelir:
below_avg= df.loc[df["price"] <=41,"price"].mean()
below_no= df.loc[df["price"] <=41,"price"].count()
income_for_below= below_no*below_avg

#fiyatın güven aralığının üzerinde olması durumunda elde edilecek gelir:
above_avg= df.loc[df["price"] >=41,"price"].mean()
above_no= df.loc[df["price"] >=41,"price"].count()
income_for_above= above_no*above_avg

# yorum: fiyatı 41 seçersen bu örn içn 887 kişi seni almaya razı. 887x41 tl den bu ürünü satarsın.
# aslında bu seçtiğin bu 887 kişi de (above_avg )61tl vermeye razıydı. yani 20x887 lik bir kaybın var ama çok önemli değil böyle çıkarmış oldu ciroyu
# toplamda income_for_above= above_no*above_avg =53500 tl cebime para koyacağım. çok da az müşteri ileilgileneceğim. 3440 müşteriden 887 sine satacağım 53500 tl para kazanacağım.

# ek yorum - fiyatı düştükçe potaya aldığım kişi sayısı artıyor buna mukabil above_avg değeri düşüyor
# ama yine de kişi sayısı arttığı için income_for_above= above_no*above_avg değeri yükseliyor
# böyle olduğunda şu sonuç çıkartılabilir; temel ürünün üzerine ek özellikler ekleyerek ve bu özellikleri pazarlayarak
# müşterilerin aslında vermeye razı oldujkları (above_avg ) meblayı, müşteriden alamaya çalışılarak mantıklı bir haraket yapılmış olur
# bir de şu var; 43 tl vermeye razı olan birisine 25tl olarak sunarsanız,
# fiyatın kalite algısı tezinden dolayı "Marka bilinirliği olmayan ürünlerin kalite algısını fiyatı belirler"

