from django.db import models
from django.core import validators

from users.models import GrUser
from .utils import resize_image, get_timestamp_path


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImageMixin(models.Model):
    image = models.ImageField(upload_to=get_timestamp_path)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.image:
            from PIL import Image
            img = Image.open(self.image)
            if img.size[0] > 300 or img.size[1] > 300:
                self.image = resize_image(self.image)
        super(ImageMixin, self).save()

    class Meta:
        abstract = True


# region Rubrics

class BaseRubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    slug = models.CharField(max_length=30,  unique=True, verbose_name='slug')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT
                                     , null=True, blank=True, verbose_name='Надрубрика')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('super_rubric__order', 'order')
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'


class RubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class Rubric(BaseRubric):
    objects = RubricManager()

    class Meta:
        proxy = True
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(BaseRubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'

# endregion Rubrics


class Article(TimeStampedModel, ImageMixin):
    rubric = models.ForeignKey(Rubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Текст статьи')
    source = models.TextField(verbose_name='Источник')
    characters = models.TextField(verbose_name='Упоминаются',
                                  validators=[validators.RegexValidator
                                              (regex=r'(.+\s{1}\(\d{4}\-(?:\d{4}|\d{0})\)(\,\s)?)+')],
                                  error_messages={
                                      'invalid': 'Введите в формате: "<имя> (<год_рождения>-<год_смерти>)"'
                                  })
    author = models.ForeignKey(GrUser, on_delete=models.CASCADE, verbose_name='Автор')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Показывать в списке')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class AdditionalImage(ImageMixin):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    caption = models.CharField(max_length=200, null=True, blank=True, default="", verbose_name='Подпись')

    class Meta:
        verbose_name = 'Дополнительная иллюстрация'
        verbose_name_plural = 'Дополнительные иллюстрации'


class Comment(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    author = models.ForeignKey(GrUser, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_approved = models.BooleanField(default=False, db_index=True, verbose_name='Одобрено')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created', ]


class Rating(TimeStampedModel):
    class Marks(models.IntegerChoices):
        LIKE = 1
        DISLIKE = -1
        NEUTRAL = 0

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(GrUser, on_delete=models.CASCADE)
    rating_change = models.IntegerField(choices=Marks.choices, default=Marks.NEUTRAL)

    class Meta:
        unique_together = (('article', 'user'),)
