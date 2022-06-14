from django.urls import path
from .views import *

urlpatterns = [
    #path("api/store/", all_stores),
    path("api/store/info", get_all_stores),
    path("api/store/info/<storeid>", get_store_by_id),
    path("api/store/info/city/<city>", get_store_by_city),
    path("api/store/", add_store),
    path("api/store/storestatus/<storeid>", update_status_of_store),    
]

