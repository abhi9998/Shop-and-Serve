from django.db import models
from django.core.exceptions import ValidationError


class Store(models.Model):

    class Meta:
        db_table = "store"

    def lengthValidator(value):
        if len(value) == 6:
            return True
        raise ValidationError("Length of pincode should be 6.")

    def activeValidator(value):
        print(value)
        if value=='Y' or value =='N':
            return True
        raise ValidationError('Active field will be Y or N')        

    name = models.CharField(max_length=30,unique=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30,default='Kitchener')
    pincode = models.CharField(max_length=6 ,validators=[lengthValidator])
    active = models.CharField(max_length=1,default='Y',validators=[activeValidator])

    
