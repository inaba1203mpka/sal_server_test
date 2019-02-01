from django.contrib import admin
from sal_system.models import Tbl_Reservation

#admin.site.register(Tbl_Reservation)

class Reservation_admin(admin.ModelAdmin) :
    list_display = ("id","group","select_date","for_time","f_num") #一覧に出したい項目

admin.site.register(Tbl_Reservation,Reservation_admin)
