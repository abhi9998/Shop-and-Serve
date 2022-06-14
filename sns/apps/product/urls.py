from django.urls import path
from .views import *

urlpatterns = [
    
    path("api/product/info",get_all_products),
    path("api/product/info/store/<storeid>",get_products_by_store),
    path("api/product/",add_product),
    path("api/product/productstatus/<productid>",update_status_of_product)
    
    
]