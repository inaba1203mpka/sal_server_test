# setting.py

ここではsal_server/setting.pyで変更を加えた部分について記述する．  
setting.pyはdjangoの設定を管理するファイルである．

## INSTALL_APPS
```
INSTALL_APPS = [
  ...
  'system',                     # APP sysytemを使用
  'rest_framework',             # rest_frameworkを使用
  'stdimage',                   # stdimageを使用
  'bootstrap_datepicker_plus',  # bootstrap_datepicker_plusを使用
]
```

## LANGUAGE_CODE & TIME_ZONE
```
LANGUAGE_CODE = 'ja'      # 言語設定を日本語に
TIME_ZONE = 'Asia/Tokyo'  # タイムゾーン設定を東京に
```
## MEDIA
```
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR
```
MEDIA_URLで写真の置かれるディレクトリの名前指定する．  
MEDIA_ROOTで写真の置かれるMEDIAディレクトリの場所を使用する．  
ここではBASE_DIRで指定されているディレクトリ(.../sal_server_test/sal_server)が指定されており，施設オブジェクト(Facility)が作られたとき，作られたオブジェクトの画像(picture)がここに格納される．  
mediaディレクトリはgitからクローンしたときには無いので注意，施設オブジェクトが作られたときに生成される．

## ログイン系
```
AUTH_USER_MODEL = 'system_User'     # ユーザー認証するモデル
LOGIN_URL = 'system:login'          # ログインページのurl
LOGIN_REDIRECT_URL = 'system:top'   # ログイン後に飛ぶurl
```

## メール設定
```
if os.uname()[1] == 'www.ngw.net.it-chiba.ac.jp':
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.Email.backend'
  EMAIL_HOST = 'localhost'
  EMAIL_PORT = 25
  EMAIL_HOST_USER = ''
  EMAIL_HOST_PASSWORD = ''
  EMAIL_USE_TLS = False
  DEFAULT_FROM_EMAIL = 'sdv2018@www.ngw.uki.net.it-chiba.ac.jp'
else :
  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
os.uname()はOSの情報を取り出す，返り値は5つ．  
0 : OSの名前  
1 : ホスト名  
2 : OSのリリース  
3 : OSのバージョン  
4 : ハードウェア識別子   

os.uname()[1]でホスト名を取り出す．ホスト名が「www.ngw.net.it-chiba.ac.jp」のとき(学内サーバのとき)，DEFAILT_FROM_EMAILのメールアドレスでメールを送信する．
それ以外の時はコンソールにメールを表示する．

## REST_Frameworkの設定
```
REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES' : [

  ]
}
```
REST_Frameworkの設定をするところ．

#  
[前へ](../md/1-ファイル構成.md)
[目次](../md/0-はじめに.md)
[次へ](../md/3-models_py.md)