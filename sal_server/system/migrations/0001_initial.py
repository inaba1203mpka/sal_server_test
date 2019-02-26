# Generated by Django 2.1.5 on 2019-02-26 11:59

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import stdimage.models
import system.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='姓')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='名')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='メールアドレス')),
                ('phone', models.CharField(max_length=12, verbose_name='電話番号')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', system.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=30, verbose_name='エリア')),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility', models.CharField(max_length=30, verbose_name='施設名')),
                ('address', models.CharField(max_length=300, verbose_name='住所')),
                ('info', models.CharField(max_length=1000, verbose_name='詳細')),
                ('picture', stdimage.models.StdImageField(blank=True, upload_to='media/', verbose_name='画像')),
                ('Area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=10, verbose_name='姓')),
                ('first_name', models.CharField(max_length=10, verbose_name='名')),
                ('group', models.CharField(max_length=30, verbose_name='団体名')),
                ('man_in', models.PositiveIntegerField(verbose_name='市内男性人数')),
                ('man_out', models.PositiveIntegerField(verbose_name='市外男性人数')),
                ('woman_in', models.PositiveIntegerField(verbose_name='市内女性人数')),
                ('woman_out', models.PositiveIntegerField(verbose_name='市外女性人数')),
                ('email', models.EmailField(max_length=200, verbose_name='メールアドレス')),
                ('phone', models.PositiveIntegerField(verbose_name='電話番号')),
                ('date_select', models.DateTimeField(verbose_name='日付-時間')),
                ('time_for', models.PositiveIntegerField(verbose_name='利用時間[時間]')),
                ('rdm_str', models.CharField(max_length=640, verbose_name='ランダム文字列')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Facility', verbose_name='施設')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=30, verbose_name='部屋名')),
            ],
        ),
        migrations.CreateModel(
            name='UseKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use', models.CharField(max_length=50, verbose_name='利用目的')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='use_kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.UseKind', verbose_name='目的'),
        ),
        migrations.AddField(
            model_name='facility',
            name='room',
            field=models.ManyToManyField(to='system.Room'),
        ),
    ]
