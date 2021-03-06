from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
from bonus.models import Bonus


class UserProfileManager(models.Manager):
    def get_queryset(self):
        qs = super(UserProfileManager, self).get_queryset().select_related('user')
        return qs


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    vip_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер карты клиента')
    fullname = models.CharField(max_length=255, blank=True, null=True, verbose_name='Полное имя')
    created = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена', blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена', blank=True)
    group = models.ForeignKey(Group, blank=True, default=1, verbose_name='Группа для скидки')
    discount = models.ForeignKey('Discount', blank=True, null=True, verbose_name='Скидка')
    points = models.PositiveIntegerField(default=0, verbose_name='Баллы')
    bonus_code = models.CharField(max_length=20, blank=True, default='', verbose_name='Бонус')

    objects = UserProfileManager()

    def __str__(self):
        return self.user.get_username()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        db_table = 'profile_profile'


class Discount(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название скидки')
    discount = models.DecimalField(max_digits=5, decimal_places=2,
                                   validators=[MinValueValidator(0.0), MaxValueValidator(100)],
                                   verbose_name='Размер скидки')
    created = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')

    def __str__(self):
        return '%s - %s' % (self.name, self.discount)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
        db_table = 'profile_discount'
