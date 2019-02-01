from django.forms import ModelForm
from django import forms
from sal_system.models import *


#予約フォーム
class ReservationForm(ModelForm) :
    class Meta:
        model = Tbl_Reservation
        fields = ("last","first","group","f_num","p_num","in_men","in_women","out_men","out_women","email","callnum","select_date","for_time")
