from datetime import date
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class ToDo(models.Model):
    # duedate user(fk)
    info = models.CharField(
                    max_length=250, 
                    null=False)

    duration_hrs = models.IntegerField(
                        default=0, 
                        validators=[MinValueValidator(0), MaxValueValidator(99)], null=True)

    duration_min = models.IntegerField(
                        default=0, 
                        validators=[MinValueValidator(0), MaxValueValidator(59)], null=True)

    duedate = models.DateField( default=date.today,
                validators=[MinValueValidator(date.today)])

    status = models.BooleanField(default=False)

    color = models.CharField(max_length=10, default="green")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )