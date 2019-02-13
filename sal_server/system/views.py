from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
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


# TOPページ
class Top(generic.TemplateView):
    template_name = 'system/top.html'

# ログイン系
class Login(LoginView):
    """ ログインページ """
    form_class = LoginForm
    template_name = 'system/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    """ ログアウトページ """
    template_name = 'system/top.html'


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