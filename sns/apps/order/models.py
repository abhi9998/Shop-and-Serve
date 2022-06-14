from email.policy import default
from django.db import models
from django.core.exceptions import ValidationError
from sns.apps.store.models import Store
from sns.apps.user.models import Group
from sns.apps.product.models import Product
from django.conf import settings


def valuePositive(value):
        if value<0:
            raise ValidationError("Price should be greater than 0")
        return True

class Order(models.Model):

    class Meta:
        db_table = "order"

    storeid = models.ForeignKey(Store,db_column='storeid', to_field='id',on_delete=models.CASCADE)
    description=models.CharField(max_length=100,default="")
    tipamount=models.DecimalField(max_digits=6,decimal_places=2,validators=[valuePositive])
    orderamount=models.DecimalField(max_digits=6,decimal_places=2,validators=[valuePositive])
    status=models.CharField(max_length=50,default="pending")
    createdtime= models.DateTimeField(auto_now_add=True, blank=True)
    checkedouttime=  models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    deliverytime=  models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    acceptedtime=  models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    canceledtime=  models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    completionconfirmedby= models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id',null=True,on_delete=models.CASCADE,db_column='completionconfirmedby',related_name='completionconfirmedby')
    orderedby= models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id',on_delete=models.DO_NOTHING,db_column='orderedby',related_name='orderedby')
    acceptedby= models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id',null=True,on_delete=models.DO_NOTHING,db_column='acceptedby',related_name='acceptedby')
    #DO_NOTHING so that we dont remove data when some user leaves the system


class OrderProduct(models.Model):

    class Meta:
        db_table = "orderproduct"

    orderid = models.ForeignKey(Order,to_field='id',db_column='orderid',on_delete=models.CASCADE)
    productid = models.ForeignKey(Product,to_field='id',db_column='productid',on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, validators=[valuePositive])
    price = models.DecimalField(null=False,decimal_places=2,max_digits=6,default=0, validators=[valuePositive])


class OrderGroup(models.Model):

    class Meta:
        db_table = "ordergroup"

    orderid = models.ForeignKey(Order,to_field='id',db_column='orderid',on_delete=models.CASCADE)
    groupid = models.ForeignKey(Group, to_field='id',db_column='groupid',on_delete=models.CASCADE)
