from django.db import models

# Create your models here.\
class user_info(models.Model):
    GENDER_CHOICES = (
        ('male', "male"),
        ('female', "female"),
        ('secret', "secret")
    )
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    height = models.FloatField(default=170)
    wight = models.FloatField(default=160)
    sex = models.CharField(max_length=6, choices=GENDER_CHOICES, default="secret")
    # email = models.EmailField()

    # class Meta:
    #     unique_together = ("username", "email")
    #     ordering = ('id',)

    def __str__(self):
        return self.username
    def __unicode__(self):
        return self.username