import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Steps of AB Test
# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği
# 3. Hipotezin Uygulanması
#   - p-value < 0.05 ise HO red.
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# Not:
# - Normallik sağlanmıyorsa direk 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.

control_group = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")
test_group = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")


control_group.describe().T
control_group["Purchase"].mean()

test_group.describe().T
test_group["Purchase"].mean()

# from helpers.helpers import check_df
# check_df(control_group)
# check_df(test_group)




############################
# Görev 1. A/B testinin hipotezini tanımlayınız.
############################


############################
# 1. Hipotezin kurulması
############################

# H0: M1  = M2 = (Maximum bidding teklif türü ile average bidding teklif türü arasındaki kazançlarda anlamlı bir fark yoktur?)
# H1: M1 != M2 = (...... vardır?)


# Not: Bizim işimiz Purchase değişkeniyle çünkü 2 reklam verme alternatifi sonrası müşteri kazancını önemseyecektir.


############################
# Görev 2.  Hipotez testini gerçekleştiriniz. Çıkan
#           sonuçların istatistiksel olarak anlamlı olup
#           olmadığını yorumlayınız.
############################

############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı
# Varyans Homojenliği

############################
# Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(control_group["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9773, p-value = 0.5891
# p > 0.05 olduğundan H0 RED EDILEMEZ, normallik varsayımı sağlanmaktadır


test_stat, pvalue = shapiro(test_group["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9589, p-value = 0.1541
# p > 0.05 olduğundan H0 RED EDILEMEZ, normallik varsayımı sağlanmaktadır

############################
# Varyans Homojenligi Varsayımı
############################


# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir


test_stat, pvalue = levene(control_group["Purchase"],
                           test_group["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 2.6393, p-value = 0.1083
# p-value > 0.05 olduğundan H0 RED EDILEMEZ,varyanslar homojendir.


#####################################################################
#Görev 3. Hangi testi kullandınız?, sebeplerini belirtiniz.
#####################################################################


#  yukarıdaki çıktılara bakıldığında 2 grupta da normallik varsayımı ve varyans homojenliği
#  varsayımının sağlandığı görülmektedir. Bu durumda 2 varsayım da sağlandığı için
# bağımsız iki örneklem t testi (parametrik test) uygulanmalıdır.




############################
# Görev 4. Görev 2’de verdiğiniz cevaba göre, müşteriye tavsiyeniz nedir?
############################



# H0: M1  = M2 = (Maximum bidding teklif türü ile average bidding teklif türü arasındaki kazançlarda anlamlı bir fark yoktur?)
# H1: M1 != M2 = (...... vardır?)

############################
#  Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test)
############################
test_stat, pvalue = ttest_ind(control_group["Purchase"],
                              test_group["Purchase"],
                              equal_var=True)  # yukarıda varyanslar eşit çıktığı için burayı True bıraktık

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = -0.9416, p-value = 0.3493
# p-value > 0.05 olduğu için H0 RED EDILEMEZ.

"""
 Not : Aşağıdaki hesaplama tavsilerde kullanılmak için eklenmiştir
     control_group["Purchase"].mean()
     Out: 550.8940587702316
    
     test_group["Purchase"].mean()
     Out: 582.1060966484677
    
     (582.1060966484677 / 550.8940587702316)-1
     result of % var : 0.056657060248409774
"""

# Müşteri için tavsiyeler:
"""

 Yukarıda yapılan hipotez testi sonucuna görülmektedir ki Maximum bidding ve average bidding teklif yöntemleri arasında
 anlamlı bir fark yoktur. Bu durumda average bidding yöntemi sizin için anlamlı bir fark sağlamayacaktır. Sizi anlıyorum;
 aşağıdaki control group ve test group dataların ortalama satın alımlarına bakıldığında %6 lık bir fark var bu doğru ancak
 bu fark şansa dayalı oluşmuş olabilir ve uzun dönemde bakıldığında bu şekilde bir artı elde etmediğinizi sizde göreceksiniz. 
 Gerekli istatistiksel incelemeye baktığımızda bu durumun kendini gösterdiği görülmektedir.


"""
