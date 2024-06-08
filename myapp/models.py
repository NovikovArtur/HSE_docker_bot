from django.db import models


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserModel(TimeStampedMixin):
    user_id = models.CharField(max_length=255, unique=True, verbose_name="ID пользователя")
    username = models.CharField(max_length=32, blank=True, null=True, verbose_name="Юзернейм пользователя")
    timezone = models.IntegerField(null=True, blank=True, verbose_name="Часовой пояс")
    answer = models.TextField(null=True, blank=True, max_length=4100, verbose_name="Переменная для хранения нужной нам информации")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        try:
            return f"{self.user_id} --> {self.username[:10]}"
        except:
            return f"{self.user_id}"


class NotesModel(TimeStampedMixin):
    user = models.CharField(max_length=255, verbose_name="ID пользователя")
    text = models.TextField(max_length=4100, verbose_name="Текст сообщения")
    time = models.DateTimeField(verbose_name="Время напоминания")
    href_on_timer = models.TextField(null=True, blank=True, verbose_name="Ссылка на таймер")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"{self.user} --> {self.text}"
