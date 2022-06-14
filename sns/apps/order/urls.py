from django.urls import path
from .views import accept_pending_order, add_order, cancel_accepted_order, checked_out_order
from .views import complete_order, get_all_orders_by_acceptorid, get_all_orders_by_groupid, get_all_orders_by_storeid, get_all_orders_by_userid

urlpatterns =[
    
    
    path("api/order/", add_order),
    path("api/order/placer/<placerid>",get_all_orders_by_userid),
    path("api/order/group/<groupid>",get_all_orders_by_groupid),
    path("api/order/store/<storeid>",get_all_orders_by_storeid), #usually would be admin/company access to this
    path("api/order/acceptor/<acceptorid>",get_all_orders_by_acceptorid),
    path("api/order/accept",accept_pending_order),
    path("api/order/cancel",cancel_accepted_order),
    path("api/order/checkout",checked_out_order),
    path("api/order/complete",complete_order),
]