from django.db import models


class Roll(models.Model):
    result = models.IntegerField()



class RoundManager(models.Manager):
    """
    RoundManager: кастомный менеджер для
    возврата проаннотированного queryset'а
    """

    def get_queryset(self):
        queryset = super().get_queryset().annotate(rolls_count=models.Count('rolls'))
        return queryset


class Round(models.Model):
    user = models.CharField(verbose_name="Пользователь", max_length=50)
    is_finished = models.BooleanField(default=False, verbose_name="Игра закончена")
    is_jackpot = models.BooleanField(default=False, verbose_name="Джекпот выигран")
    rolls = models.ManyToManyField(Roll, verbose_name="Спины раунда", blank=True)

    # переопределяем дефолтный менеджер
    objects = RoundManager()
