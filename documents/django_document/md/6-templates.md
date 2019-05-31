# Templates
ここではsystem/templatesについて説明する．  
templatesフォルダはviews.pyから送られてきたデータを表示する為のファイルが格納されているところである．  
## ファイル構成
```
.
└── system
    ├── base.html
    ├── facility_list.html
    ├── login.html
    ├── mail_templates
    │   ├── message.txt
    │   └── subject.txt
    ├── reservation_confirm_delete.html
    ├── reservation_create.html
    ├── reservation_list.html
    ├── top.html
    ├── user_create.html
    ├── user_create_complete.html
    └── user_create_done.html
```
基本的にbase.htmlを継承してページを作っている．

## 変数
viewから送られてきたデータを表示する．  
vies.pyで，def get_context_dataのcontext['〜〜'] = ~~が実行されている場合．
〜〜を変数名として，context['〜〜']に格納されているオブジェクトを表示することができる．

#  
[前へ](../md/5-views_py.md)
[目次](../md/0-はじめに.md)
[次へ](../md/7-その他.md)
