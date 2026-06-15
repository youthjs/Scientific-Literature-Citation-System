from django.db import models


class ClassCheckModel(models.Model):
    news_text = models.TextField(verbose_name='检测文字')
    check_result = models.CharField(max_length=100, verbose_name='识别结果', blank=True)
    check_time = models.DateTimeField(auto_now_add=True, verbose_name='检测时间')

    class Meta:
        db_table = 'class_check'
        verbose_name = '文字检测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str("检测文字")

class myModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    class Meta:
        db_table = 'check_table'
        verbose_name = '可视化图表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class UserInfoModel(models.Model):
    username = models.CharField(max_length=200, verbose_name='用户名')
    password = models.CharField(max_length=200, verbose_name='密码')

    class Meta:
        db_table = 'db_user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
