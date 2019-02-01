from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import Tbl_Reservation
from .forms import ReservationForm

""" ページ推移系 """
# 後 mypage(request,user_id) : title = user_id
def mypage(request) :
    title = "マイページ"
    return render(request,"sal_system/mypage.html")

def guide(request) :
    title = "利用ガイド"
    return render(request,"sal_system/guide.html")


""" 予約系 """ 
def reservation_list(request) :
    title = "予約一覧"
    reservations = Tbl_Reservation.objects.order_by("select_date")
    return render(request, "sal_system/reservlist.html",{"reservations":reservations})

def reservation_edit(request) :
    title = "予約登録"
    reservation = Tbl_Reservation()
    if request.method == "POST" :
        form = ReservationForm(request.POST)
        if form.is_valid():    # フォームのバリデーション
            reservation = form.save(commit=False)
            reservation.save()
            return redirect('sal_system:reservation_list')
    else:    # GET の時
        form = ReservationForm() 

    return render(request, 'sal_system/reservation.html', {"form" : form})

def reservation_delete(request,tbl_reservation_id) :
    title = "予約削除"
    reservation = get_object_or_404(Tbl_Reservation, pk = tbl_reservation_id)
    reservation.delete()
    return redirect('sal_system:reservation_list')


""" 施設系 """
def facility_search(request) :
    title = "施設検索"
    return render(request,"sal_system/facilitysearch.html")

