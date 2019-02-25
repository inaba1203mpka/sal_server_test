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
    #date_select = forms.SplitDateTimeField(label='日付-時間')
    class Meta :
        model = Reservation
        fields = ['last_name','first_name','group','facility','use_kind','man_in','woman_in','man_out','woman_out','email','phone','date_select','time_for']
        widgets = {
            'last_name': forms.TextInput(attrs={'placeholder':'例：富浦'}),
            'first_name': forms.TextInput(attrs={'placeholder':'例：太郎'}),
            'group': forms.TextInput(attrs={'placeholder':'例：チーム○○'}),
            #'facility': forms.SelectMultiple(attrs={'placeholder':'選択してください'}),
            #'use_kind': forms.SelectMultiple(attrs={'placeholder':'選択してください'}),
            'man_in': forms.NumberInput(attrs={'placeholder':'数値を入力してください'}),
            'woman_in': forms.NumberInput(attrs={'placeholder':'数値を入力してください'}),
            'man_out': forms.NumberInput(attrs={'placeholder':'数値を入力してください'}),
            'woman_out': forms.NumberInput(attrs={'placeholder':'数値を入力してください'}),
            'email': forms.TextInput(attrs={'placeholder':'例：minamiboso@example.com'}),
            'phone': forms.NumberInput(attrs={'placeholder':'例：0001111222'}),
            'date_select': forms.NumberInput(attrs={'placeholder':'例：2000-1-1'}),
            'time_for': forms.NumberInput(attrs={'placeholder':'例：1'})

        }
    #Bootstrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            


