# urls.py
ここではurls.pyについて記述する．  
urls.pyはシステムのurlを管理するファイルである．
## sal_system/urls.py
djangoのシステムのurlを管理する．
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('system.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
  +staticで画像保存先のURLを指定している．ここのファイルには施設画像が入る．  
  参考URL : [https://qiita.com/okoppe8/items/86776b8df566a4513e96](https://qiita.com/okoppe8/items/86776b8df566a4513e96)
## system/urls.py
公共施設利活用システムのurlを管理する．
```
    ...
    # 普通の書式．参考書等で学習
    ...
    # ランダム文字列受け取り
    path('random_string/', views.Random_string.as_view(),name='random_string'),
```
random_stringはAPIViewを使っている．そのため，このURLはREST_Frameworkのページに移動する．


#  
[前へ](../md/3-models_py.md)
[目次](../md/0-はじめに.md)
[次へ](../md/5-views_py.md)