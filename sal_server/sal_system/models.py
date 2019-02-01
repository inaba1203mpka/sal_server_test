from django.db import models


#アカウントテーブル
"""
class Tbl_Account(models.Model) :

    ・アカウント番号 (主キー) : 
    ・姓 : last - char(max=10)
    ・名 : first - char(max=10)
    ・E-mail : email - email(max=200)
    ・パスワード : AbstractBaseUser から (?)
    ・電話番号 : callnum - int(unsigned)


    last = models.CharField(max_length = 10)
    first = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 200,unique=True)
    callnum = models.PositiveIntegerField()
"""



#予約テーブル
class Tbl_Reservation(models.Model) :
    """
    ・予約番号(主キー) :
    ・アカウント番号 : a_num - int(unsigned)
    ・姓 : last - char(max=10)
    ・名 : first - char(max=10)
    ・団体名 : group - char(max=20)
    ・施設番号 : f_num - int(unsigned)
    ・利用種別(目的) : p_num - int(unsigned)
    ・人数 市内 男 : in_men - int(unsigned)
    ・人数 市内 女 : in_women - int(unsigned)
    ・人数 市外 男 : out_men - int(unsigned)
    ・人数 市外 女 : out_women - int(unsigned)
    ・送信メアド : email - email(max=200)
    ・電話番号 : callnum - int(unsigned)
    ・日付 : select_date - datetime
    ・利用時間 : for_time - int(unsigned)

    """

    last = models.CharField("姓",max_length = 10)
    first = models.CharField("名",max_length = 10)
    group = models.CharField("団体名",max_length = 20)
    f_num = models.PositiveIntegerField("施設")
    p_num = models.PositiveIntegerField("利用種別")
    in_men = models.PositiveIntegerField("市内男性人数")
    in_women = models.PositiveIntegerField("市内女性人数")
    out_men = models.PositiveIntegerField("市外男性人数")
    out_women = models.PositiveIntegerField("市外女性人数")
    email = models.EmailField("メールアドレス",max_length = 200,unique=True)
    callnum = models.PositiveIntegerField("電話番号")
    select_date = models.DateTimeField("日付")
    for_time = models.PositiveIntegerField("利用時間")

    def __str__(self) :
        return self.group

#施設テーブル
class Tbl_Place(models.Model) :
    pass


