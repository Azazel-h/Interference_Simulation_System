from django.db import models


class RequestFP(models.Model):
    COLOR = (
        ('g', 'Зеленый - 532 нм'),
        ('r', 'Красный - 630 нм')
    )
    user = models.CharField(max_length=50)
    laser_color = models.CharField(choices=COLOR, max_length=50)
    glasses_distance = models.FloatField(default=0)
    focal_distance = models.FloatField(default=0)
    stroke_difference = models.FloatField(default=0)
    reflectivity = models.FloatField(default=0)
    refractive_index = models.FloatField(default=0)
    picture_size = models.FloatField(default=0)
    incident_light_intensity = models.FloatField(default=0)
    N = models.IntegerField()


class PresetFP(models.Model):
    COLOR = (
        ('g', 'Зеленый - 532 нм'),
        ('r', 'Красный - 630 нм')
    )
    user = models.CharField(max_length=50)
    laser_color = models.CharField(choices=COLOR, max_length=50)
    glasses_distance = models.FloatField(default=0)
    focal_distance = models.FloatField(default=0)
    stroke_difference = models.FloatField(default=0)
    reflectivity = models.FloatField(default=0)
    refractive_index = models.FloatField(default=0)
    picture_size = models.FloatField(default=0)
    incident_light_intensity = models.FloatField(default=0)
    N = models.IntegerField()
