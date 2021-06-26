from django.contrib.auth.models import AbstractUser


class GrUser(AbstractUser):
    def delete(self, *args, **kwargs):
        for article in self.article_set.all():
            article.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



