from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages  
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.loader import get_template
from django.views import generic

from .forms import (
    LoginForm, UserCreateForm
)

from django.contrib.auth import get_user_model
User = get_user_model() #Userモデルの取得

from .models import *
from .forms import ReservationForm

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import random, string, qrcode, os, datetime, pytz

# TOPページ
class Top(LoginRequiredMixin, generic.TemplateView):
    template_name = 'system/top.html'


# ログイン系
class Login(LoginView):
    """ ログインページ """
    form_class = LoginForm
    template_name = 'system/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    """ ログアウトページ """
    template_name = 'system/top.html'
    login_url = "/login"


# ユーザ登録系
class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'system/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使う。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template('system/mail_templates/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('system/mail_templates/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('system:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'system/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'system/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


#  予約系
class Reservation_create(LoginRequiredMixin, generic.CreateView):
    """ 予約作成 """ 
    model = Reservation
    template_name = 'system/reservation_create.html'
    form_class = ReservationForm
    success_url = "/"
    login_url = "/login"

    def form_valid(self, form):
        #入力欄にないフィールドを追加
        form.instance.owner_id = self.request.user
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=640))    #ランダム文字列生成
        form.instance.rdm_str = random_string   
        qr_code = qrcode.make( random_string )  #qr_code作成
        qr_code.save("qr.png") 

        #メールの設定
        subject = "QRコード"    #題名
        message = "予約していただきありがとうございます\nこのメールには返信できません"  #文章
        from_email = "webmaster@localhost"  #送信元メールアドレス
        recipient_list = [
            form.instance.email #宛先メールアドレス
        ]
        qr_mail = EmailMessage(subject,message, from_email=from_email, to=recipient_list)
        qr_mail.attach("qr_code.png", "qr.png" , 'image/png')  #qr_code添付
        qr_mail.send()
        #os.remove("qr.png")

        #完了
        messages.success(self.request, "予約しました")
        return super(Reservation_create, self).form_valid(form)


class Reservation_list(LoginRequiredMixin, generic.ListView) :
    """ 予約一覧 """
    model = Reservation
    template_name = 'system/reservation_list.html'
    paginate_by = 5
    login_url = "/login"
    context_object_name = "my_reservations"

    # フィルターをかける
    def get_queryset(self):
        return Reservation.objects.filter(owner_id=self.request.user)

    # 別のモデルをを取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = User.objects.filter(id=self.request.user.id)[0]   # Userモデルからユーザネーム - 配列で受け取るので[0]
        return context


class  Reservation_delete(LoginRequiredMixin, generic.DeleteView):
    """ 予約削除 """
    model = Reservation
    login_url = "/login"
    form_class = ReservationForm

    success_url = reverse_lazy('system:reservation_list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result


#施設検索
class Facility_list(LoginRequiredMixin, generic.ListView):
    """ 施設一覧 """
    model = Facility
    template_name = 'system/Facility_list.html'
    paginate_by = 5
    login_url = "/login"
    context_object_name = "facilities"


#ランダム文字列受け取り : http:~~/random_string?rdm_str="~~~"
class Random_string(APIView):
    def get(self, request, format=None):
        if "rdm_str" in request.GET:
            # query_paramが指定されている場合の処理
            random_string = request.GET.get("rdm_str")
            reservation = Reservation.objects.filter(rdm_str=random_string) 
            now = pytz.ja.localize(now)
            if reservation[0].date_select - datetime.timedelta(minutes=15) <= now or \
                reservation[0].date_select + datetime.timedelta(hour=reservation[0].time_for) + datetime.timedelta(minutes=15) >= now :
                # 今が 予約時間-15分以上　かつ 予約時間+利用時間+15分以下 のとき
                return Response({"Ans": "True"},status=status.HTTP_200_OK)
            else :
                return Response({"Ans": "False_time"},status=status.HTTP_200_OK)
        else:
            # query_paramが指定されていない場合の処理
            return Response({"Ans": "False"},status=status.HTTP_200_OK)


