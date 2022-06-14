from django.db import models
from django.core.exceptions import ValidationError
from sns.apps.store.models import Store


class Product(models.Model):

    
    class Meta:
        db_table = "product"

    def valuePositive(value):
        if value<0:
            raise ValidationError("Price should be greater than 0")
        return True    

    def activeValidator(value):
        print(value)
        if value=='Y' or value =='N':
            return True
        raise ValidationError('Active field will be Y or N')    

    name = models.CharField(max_length=30,unique=True)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5,decimal_places=2,validators=[valuePositive])
    brand = models.CharField(max_length=20)
    imagelink = models.CharField(max_length=200)
    weight = models.DecimalField(max_digits=5,decimal_places=2,validators=[valuePositive])
    storeid = models.ForeignKey(Store, db_column='storeid',on_delete=models.CASCADE)
    active = models.CharField(max_length=1,default='Y',validators=[activeValidator])
    
