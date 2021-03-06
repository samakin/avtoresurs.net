from django.db import models
from cms.models import CMSPlugin


class AssortmentItem(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название брэнда')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    image = models.ImageField(null=True, blank=True, verbose_name='Картинка')
    status = models.BooleanField(default=True, verbose_name='Активен')
    _url = models.CharField(max_length=255, verbose_name='Ссылка', null=True, db_column='url')

    @property
    def url(self):
        return self._url or '#'

    @url.setter
    def url(self, value):
        self._url = value

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Товар'
        verbose_name_plural = 'Ассортимент'


class AssortmentItemPlugin(CMSPlugin):
    latest_items = models.IntegerField(
        default=20,
    )

    def __str__(self):
        return str(self.latest_items)

    def get_items(self):
        posts = AssortmentItem.objects.all()[:self.latest_items]
        return posts
