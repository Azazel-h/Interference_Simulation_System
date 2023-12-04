from django.db import models


class RequestFP(models.Model):
    user = models.CharField(max_length=50)
    wave_length = models.FloatField(default=0)
    wave_length_diff = models.FloatField(default=0)
    glasses_distance = models.FloatField(default=0)
    focal_distance = models.FloatField(default=0)
    reflection_coefficient = models.FloatField(default=0)
    refractive_index = models.FloatField(default=0)
    picture_size = models.FloatField(default=0)
    N = models.IntegerField()
    request_time = models.DateTimeField(auto_now_add=True)


class PresetFP(models.Model):
    user = models.CharField(max_length=50)
    wave_length = models.FloatField(default=0)
    wave_length_diff = models.FloatField(default=0)
    glasses_distance = models.FloatField(default=0)
    focal_distance = models.FloatField(default=0)
    reflection_coefficient = models.FloatField(default=0)
    refractive_index = models.FloatField(default=0)
    picture_size = models.FloatField(default=0)
    N = models.IntegerField()
