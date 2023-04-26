from django.db import models


class RequestM(models.Model):
    user = models.CharField(max_length=50)
    wave_length = models.FloatField(default=0)
    z1 = models.FloatField(default=0)
    z2 = models.FloatField(default=0)
    Rbs = models.FloatField(default=0)
    tx = models.FloatField(default=0)
    ty = models.FloatField(default=0)
    f = models.FloatField(default=0)
    picture_size = models.FloatField(default=0)
    N = models.IntegerField()
    request_time = models.DateTimeField(auto_now_add=True)


class PresetM(models.Model):
    user = models.CharField(max_length=50)
    wave_length = models.FloatField(default=0)
    z1 = models.FloatField(default=0)
    z2 = models.FloatField(default=0)
    Rbs = models.FloatField(default=0)
    tx = models.FloatField(default=0)
    ty = models.FloatField(default=0)
    f = models.FloatField(default=0)
    picture_size = models.FloatField(default=0)
    N = models.IntegerField()
