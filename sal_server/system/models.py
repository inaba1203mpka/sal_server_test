from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    #ユーザー AbstractUserをコピペし編集
    """
    User
        ユーザーネーム : username
        姓 : last_name
        名 : first_name
        メール : email
        電話番号 : phone
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('姓'), max_length=30, blank=True)
    last_name = models.CharField(_('名'), max_length=150, blank=True)
    email = models.EmailField(_('メールアドレス'), blank=True)

    #追加 電話番号
    phone = models.CharField(_('電話番号'),max_length=12)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 既存メソッドの変更
    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    #追加
    def get_phone(self):
        return self.phone

    


""" 予約 """
class Reservation(models.Model) : 
    """
        登録ユーザー : user_id
        姓 : last_name
        名 : first_name
        団体名 : group
        施設 : facility
        利用目的 : use_kind
        人数_市内_男 : man_in
        人数_市内_女 : woman_in
        人数_市外_男 : man_out
        人数_市外_女 : woman_out
        送信用メールアドレス : email
        電話番号 : phone
        予約日付 : date_select
        利用時間 : time_for
    """
    user_id : models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    last_name = models.CharField("姓",max_length=10)
    first_name = models.CharField("名",max_length=10)
    group = models.CharField("団体名",max_length=30)
    facility = models.ForeignKey('Facility',on_delete=models.CASCADE)
    use_kind = models.ForeignKey('UseKind',on_delete=models.CASCADE)
    man_in = models.PositiveIntegerField("市内男性人数")
    man_out = models.PositiveIntegerField("市内女性人数")
    woman_in = models.PositiveIntegerField("市外男性人数")
    woman_out = models.PositiveIntegerField("市外女性人数")
    email = models.EmailField("メールアドレス",max_length = 200,unique=True)
    phone = models.PositiveIntegerField("電話番号")
    date_select = models.DateTimeField("日付")
    time_for = models.PositiveIntegerField("利用時間")
    


""" 施設 """
class Facility(models.Model):
    """
        施設名 : facility
        エリア : area
        住所 : address
        画像id : picture
        部屋 : room

    """
    facility = models.CharField("施設名",max_length=30)
    Area = models.ForeignKey('Area',on_delete=models.CASCADE)
    address = models.CharField("住所",max_length=300)
    picture = models.CharField("画像",max_length=300)
    room = models.ManyToManyField('Room')

    def get_facility(self):
        return self.facility

    def get_address(self):
        return self.address

    def get_picture(self):
        return self.picture

    def get_area(self):
        return self.area

    def get_room(self):
        return self.room


""" 部屋 """
class Room(models.Model):
    """
        部屋名 : room
    """
    room = models.CharField("部屋名",max_length=30)

    def get_room(self):
        return self.room



""" 利用目的 """
class UseKind(models.Model):
    """
        利用目的 : use
    """
    use = models.CharField("利用目的",max_length=50)
    
    def get_use(self):
        return self.use



""" 検索用場所 """
class Area(models.Model):
    """
        場所 : area
    """
    area = models.CharField("エリア",max_length=30)

    def get_area(self):
        return self.area
