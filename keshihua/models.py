from django.db import models
from django.contrib.auth.models import  AbstractUser

# Create your models here.

class Yonghu(AbstractUser):

    set_choices = (
        ('男', '男'),
        ('女', '女')
    )
    age = models.CharField(verbose_name='年龄', max_length=16, default='18')
    set = models.CharField(verbose_name='性别', max_length=12, default='男', choices=set_choices)

    def __str__(self):
        return self.username
        pass
    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class Case_item(models.Model):
    fabushijian = models.DateTimeField(default='')
    fabu_name = models.CharField(verbose_name='发布人', default='', max_length=124)
    content = models.TextField(verbose_name='内容', default='')
    status = models.CharField(verbose_name='情感状态', default='NULL', max_length=124)
    possibility = models.FloatField(verbose_name='可能性', default=0)
    zhuanfa = models.FloatField(verbose_name='转发', default=0)
    pingluns = models.FloatField(verbose_name='评论数', default=0)
    dianzan = models.FloatField(verbose_name='点赞', default=0)
    url = models.CharField(verbose_name='链接', default='', max_length=240)

    def __str__(self):
        return self.fabu_name

    class Meta:
        verbose_name = u"数据表"
        verbose_name_plural = verbose_name

