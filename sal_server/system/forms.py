from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Reservation

class LoginForm(AuthenticationForm):
    """ログインフォーム"""
    #Bootstrap用
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""
    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email',)
        else:
            fields = ('username', 'email')
    #Bootstarap用
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ReservationForm(forms.ModelForm):
    """予約フォーム"""
    class Meta :
        model = Reservation
        fields = ['last_name','first_name','group','facility','use_kind','man_in','woman_in','man_out','woman_out','email','phone','date_select','time_for']
    #Bootstrap用
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


