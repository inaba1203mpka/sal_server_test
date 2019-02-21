from django.urls import path
from . import views

app_name = 'system'

urlpatterns = [
    # トップ
    path('', views.Top.as_view(), name='top'),
    # ログイン
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    # ユーザー作成
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    #予約系
    path('reservation_create/', views.Reservation_create.as_view(),name='reservation_create'),
    path('reservation_list/', views.Reservation_list.as_view(),name='reservation_list'),
    path('<int:pk>/delete/',views.Reservation_delete.as_view(), name='reservation_delete'),
    #施設検索系
    path('facility_list/', views.Facility_list.as_view(),name='facility_list'),
    #ランダム文字列受け取り
    path('random_string', views.Random_string.as_view(),name='random_string'),
]
