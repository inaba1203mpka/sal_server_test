from django.urls import path
from sal_system import views

app_name="sal_system"
urlpatterns = [
    #-- ページ推移 --
    #マイページ ( ユーザidにしたい : mypage/ -> <int:pk> )
    path('mypage/',views.mypage,name='mypage'),
    path('guide/',views.guide,name='guide'),


    #-- 予約系 --
    #予約一覧
    path('reservation/', views.reservation_list, name='reservation_list'),
    #予約登録
    path('reservation/add/', views.reservation_edit, name='reservation_add'), 
    #予約削除
    path('reservation/del/<int:tbl_reservation_id>/', views.reservation_delete, name='reservation_delete'),


    #-- 施設系 --
    #施設検索
    path('facility/',views.facility_search,name='facility_search'),

]