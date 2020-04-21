from django.db import models
from foodlog.storage import ImageStorage
from user.models import user_info
# Create your models here.

class health_element(models.Model):
    he_id = models.AutoField(primary_key=True)
    Carbohydrates = models.FloatField(default=0)
    Proteins = models.FloatField(default=0)
    Fats = models.FloatField(default=0)
    Minerals = models.FloatField(default=0)

class day_record(models.Model):
    day_record_id= models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user_info,on_delete=models.CASCADE)
    he_id = models.ForeignKey(health_element,on_delete=models.CASCADE)
    date = models.DateField()

class food_pic(models.Model):
    pic_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user_info,on_delete=models.CASCADE)
    he_id = models.ForeignKey(health_element,on_delete=models.CASCADE)
    day_record_id = models.ForeignKey(day_record,on_delete=models.CASCADE)
    img = models.FileField(upload_to="food/",storage=ImageStorage())
    upload_time = models.DateTimeField()


class box(models.Model):
    box_id = models.AutoField(primary_key=True)
    index_in_pic = models.IntegerField()
    pic_id = models.ForeignKey(food_pic,on_delete=models.CASCADE)
    he_id = models.ForeignKey(health_element,on_delete=models.CASCADE)
    left = models.FloatField()
    upper = models.FloatField()
    right = models.FloatField()
    down = models.FloatField()
    prob = models.FloatField()
    food_class = models.CharField(max_length=10)

    class Meta:
        unique_together = ("pic_id", "index_in_pic")

