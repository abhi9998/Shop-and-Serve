import pytz
from django.http import JsonResponse
from .models import Order, OrderGroup, OrderProduct
from sns.apps.user.models import SnsUser
from datetime import datetime
from sns.apps.store.serializers import StoreSerializer
from sns.apps.store.models import Store
from .serializers import OrderGroupSerializer, OrderProductSerializer, OrderSerializer
from rest_framework import status as status
from rest_framework.decorators import api_view
from datetime import datetime
from django.db import transaction,connection
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes

cursor= connection.cursor()



#this will make edit to the to order table , orderproduct table, ordergroup table
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@transaction.atomic
def add_order(request):
    
    print(request.data)
    try:
        with transaction.atomic():

            orderInfo = request.data['orderDetails']
            orderItems = request.data['orderItems']
            groupInfo = request.data['group']
            
            deserializedOrder = OrderSerializer(data=orderInfo)
            
            if deserializedOrder.is_valid():
                orderObject = deserializedOrder.save()
                print("orderinfo saved successfully")
                # return JsonResponse({"success":"orderplaced"},status=status.HTTP_201_CREATED);    
            else:
                print(deserializedOrder.errors)
                raise Exception("Failed saving order")


            #add the orderid in every object of items array
            for items in orderItems:
                items['orderid']=orderObject.pk

            deserializedItems = OrderProductSerializer(data=orderItems,many = True)
                        
            if deserializedItems.is_valid():
                orderItemsObject = deserializedItems.save()
                print("order and product stored successfully")
                # return JsonResponse({"success":"orderplaced with items"},status=status.HTTP_201_CREATED);  
            else:
                print(deserializedItems.errors)
                raise Exception("Failed saving items");    
                

            orderGroupData = []
            for i in groupInfo:
                orderGroupData.append({"orderid":orderObject.pk,"groupid":i})

            
            deserializedGroups = OrderGroupSerializer(data=orderGroupData,many=True)
            print(deserializedGroups.is_valid())

            if deserializedGroups.is_valid():
                groupInfoObject = deserializedGroups.save()
                print("order and groups store successfully")
            else:
                print(deserializedGroups.errors)
                raise Exception("Failed saving groups")

            totalAmount = orderInfo['orderamount']+ orderInfo['tipamount']

            userResponse = SnsUser.objects.get(id=orderInfo['orderedby'])
            
            walletAmount = userResponse.walletamount

            if walletAmount>totalAmount:
                userResponse.walletamount=walletAmount-totalAmount
                userResponse.save()
                print("amount from wallet deducted")
            else:
                raise Exception("Order amount more than wallet amount")

            return JsonResponse({"success":"orderplaced with items"},status=status.HTTP_201_CREATED) 


    except Exception as e:
        
        return JsonResponse({"error": str(e)},status=status.HTTP_400_BAD_REQUEST)


def fetchGroupDetailsOfOrder(orderDetailsSerialized):
    
    orderDetailsSerialized = list(orderDetailsSerialized)
    
    for i in orderDetailsSerialized:
        orderid = i['id']
        groupInfo = []
        
        orderGroupResponse = OrderGroup.objects.filter(orderid=orderid)
        orderGroupSerialized = OrderGroupSerializer(orderGroupResponse,many=True)
        
        for j in list(orderGroupSerialized.data):
            
            groupId= j['groupid']
            cursor.execute(f'SELECT id, name from public.group where id = {groupId}')
            data = cursor.fetchone()
            groupDetail = {}
            groupDetail['id']=data[0]
            groupDetail['name']=data[1]
            groupInfo.append(groupDetail)

        i['groupInfo']=groupInfo
    return

def fetchProductDetailsOfOrder(orderDetailsSerialized):

    for i in orderDetailsSerialized:
        orderid = i['id']
        orderItems = []

        orderProductResponse = OrderProduct.objects.filter(orderid=orderid)
        orderProductSerialized = OrderProductSerializer(orderProductResponse,many=True)
        
        for j in list(orderProductSerialized.data):
            del j['id']
            del j['orderid']
            productId = j['productid']
            cursor.execute(f'SELECT name from public.product where id= {productId}')
            data = cursor.fetchone()
            j['name']=data[0]
            orderItems.append(j)

        i['orderItems']=orderItems
    return             
        

def fetchStoreDetailsOfOrder(orderDetailsSerialized):
    for i in orderDetailsSerialized:
        storeid = i['storeid']

        storeResponse = Store.objects.filter(id=storeid)
        storeSerialized = StoreSerializer(storeResponse,many=True)
        storeSerialized=list(storeSerialized.data)
        i['storename']=storeSerialized[0]['name']

    return
    

#this endpoint returns all orders placed by user along with details in which group its placed and the item details.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_orders_by_userid(request,placerid):

    try:
        
        param = request.GET.get('status','*')
        
        
        if param=="*":
            orderDetailResponse = Order.objects.filter(orderedby=placerid)
            orderDetailSerialized = OrderSerializer(orderDetailResponse, many=True)
            fetchGroupDetailsOfOrder(orderDetailSerialized.data)
            fetchProductDetailsOfOrder(orderDetailSerialized.data)
            fetchStoreDetailsOfOrder(orderDetailSerialized.data)
        else:
            orderDetailResponse = Order.objects.filter(orderedby=placerid,status=param)
            orderDetailSerialized = OrderSerializer(orderDetailResponse, many=True)
            fetchGroupDetailsOfOrder(orderDetailSerialized.data)
            fetchProductDetailsOfOrder(orderDetailSerialized.data)
            fetchStoreDetailsOfOrder(orderDetailSerialized.data)

        return JsonResponse(orderDetailSerialized.data,status= status.HTTP_200_OK,safe=False)

    except Order.DoesNotExist:
        return JsonResponse({"error":"Order not placed by given User"},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal server error for fetching the orders placed"},status=status.HTTP_503_SERVICE_UNAVAILABLE)    




@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_orders_by_groupid(request,groupid):

    try:
        
        param = request.GET.get('status','*')
        
        
        orderGroupResponse = OrderGroup.objects.filter(groupid=groupid)
        orderGroupSerialized = OrderGroupSerializer(orderGroupResponse, many=True)
        orderGroupSerialized = orderGroupSerialized.data
        orderArray =[]
        for j in orderGroupSerialized:
            orderArray.append(j['orderid'])

        if param=="*":
            orderDetailResponse = Order.objects.filter(id__in=orderArray)
            orderDetailSerialized = OrderSerializer(orderDetailResponse, many=True)
            fetchProductDetailsOfOrder(orderDetailSerialized.data)
            fetchStoreDetailsOfOrder(orderDetailSerialized.data)
        else:
            orderDetailResponse = Order.objects.filter(id__in=orderArray,status=param)
            orderDetailSerialized = OrderSerializer(orderDetailResponse, many=True)
            fetchProductDetailsOfOrder(orderDetailSerialized.data)
            fetchStoreDetailsOfOrder(orderDetailSerialized.data)

        return JsonResponse(orderDetailSerialized.data,status=status.HTTP_200_OK,safe=False)

    except Order.DoesNotExist:
        return JsonResponse({"error":"Order not Found for given group"},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal server error for fetching the orders placed in a given group"},status=status.HTTP_503_SERVICE_UNAVAILABLE)    



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_orders_by_storeid(request,storeid):

    try:
        
        param = request.GET.get('status','*')
        
        if param=="*":
            orderDetailResponse = Order.objects.filter(storeid=storeid)
            orderDetailSerialized = OrderSerializer(orderDetailResponse, many=True)
            fetchGroupDetailsOfOrder(orderDetailSerialized.data)
            fetchProductDetailsOfOrder(orderDetailSerialized.data)
            #fetchStoreDetailsOfOrder(orderDetailSerialized.data)
        else:
            orderDetailResponse = Order.objects.filter(storeid=storeid,status=param)
            orderDetailSerialized = OrderSerializer(orderDetailResponse, many=True)
            fetchGroupDetailsOfOrder(orderDetailSerialized.data)
            fetchProductDetailsOfOrder(orderDetailSerialized.data)
            #fetchStoreDetailsOfOrder(orderDetailSerialized.data)

        return JsonResponse(orderDetailSerialized.data,status=status.HTTP_200_OK,safe=False)

    except Order.DoesNotExist:
        return JsonResponse({"error":"Order not Found for given store"},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal server error for fetching the orders placed in a given store"},status=status.HTTP_503_SERVICE_UNAVAILABLE)    



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_orders_by_acceptorid(request,acceptorid):

    try:
        
        param = request.GET.get('status','*')
        
        
        if param=="*":
            orderDetailResponse = Order.objects.filter(acceptedby=acceptorid)
            orderDetailSerialized = OrderSerializer(orderDetailResponse, many=True)
            fetchGroupDetailsOfOrder(orderDetailSerialized.data)
            fetchProductDetailsOfOrder(orderDetailSerialized.data)
            fetchStoreDetailsOfOrder(orderDetailSerialized.data)
        else:
            orderDetailResponse = Order.objects.filter(acceptedby=acceptorid,status=param)
            orderDetailSerialized = OrderSerializer(orderDetailResponse, many=True)
            fetchGroupDetailsOfOrder(orderDetailSerialized.data)
            fetchProductDetailsOfOrder(orderDetailSerialized.data)
            fetchStoreDetailsOfOrder(orderDetailSerialized.data)

        return JsonResponse(orderDetailSerialized.data,status=status.HTTP_200_OK,safe=False)

    except Order.DoesNotExist:
        return JsonResponse({"error":"Order not Found for given acceptor"},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal server error for fetching the orders placed by a acceptor"},status=status.HTTP_503_SERVICE_UNAVAILABLE)    


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def accept_pending_order(request):
    try:

        
        orderResponse = Order.objects.get(id=request.data['orderid'])

        if orderResponse.status!= "pending":
            return JsonResponse({"error":"order is already accepted"}, status=status.HTTP_403_FORBIDDEN)

        
        if orderResponse.orderedby_id== request.data['acceptorid']:
            return JsonResponse({"error":"placer cannot accept his own order"}, status=status.HTTP_403_FORBIDDEN)

        orderResponse.acceptedby_id = request.data['acceptorid']
        orderResponse.acceptedtime = datetime.now()
        orderResponse.status = 'accepted'
        orderResponse.save()

        return JsonResponse({"success":"Order accepted successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        return JsonResponse({"error":"problem occured in accepting the order"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@transaction.atomic
def cancel_accepted_order(request):
    try:
        with transaction.atomic():
            
            orderResponse = Order.objects.get(id=request.data['orderid'])
            
            if orderResponse.orderedby_id != request.data["rejectorid"]:
                return JsonResponse({"error":"order is not canceled by placer"}, status=status.HTTP_403_FORBIDDEN)

            if orderResponse.status!= "accepted":
                return JsonResponse({"error":"only accepted order can be canceled"}, status=status.HTTP_403_FORBIDDEN)


            acceptedtime=orderResponse.acceptedtime
            acceptedtime = acceptedtime.replace(tzinfo=pytz.UTC)
            timeDifference = datetime.now().replace(tzinfo=pytz.UTC) - acceptedtime
            
            if timeDifference.total_seconds()>300:
                return JsonResponse({"error":"order accepted took more than 5 mins"}, status=status.HTTP_403_FORBIDDEN)
                
            

            userResponse = SnsUser.objects.get(id=request.data['rejectorid'])
            walletAmount = userResponse.walletamount            
            userResponse.walletamount=walletAmount+ orderResponse.tipamount +orderResponse.orderamount
            userResponse.save()
                
            
            orderResponse.status = 'canceled'
            orderResponse.acceptedtime = None
            orderResponse.acceptedby_id = None
            orderResponse.save()


            return JsonResponse({"success":"Order canceled successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal server error occurred for cancelling order"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def checked_out_order(request):
    try:

        orderResponse = Order.objects.get(id=request.data['orderid'])

        if orderResponse.acceptedby_id != request.data["acceptorid"]:
            return JsonResponse({"error":"order can be checkedout by acceptor"}, status=status.HTTP_403_FORBIDDEN)

        if orderResponse.status!= "accepted":
            return JsonResponse({"error":"only accepted order can be canceled"}, status=status.HTTP_403_FORBIDDEN)
        
        orderResponse.checkedouttime = datetime.now()
        orderResponse.status = "checkedout"
        orderResponse.save()

        return JsonResponse({"success":"Order checkedout successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal server error occured in checking out order"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@transaction.atomic
def complete_order(request):
    try:
        with transaction.atomic():
        
            orderResponse = Order.objects.get(id=request.data['orderid'])

            if request.data['placerid']==None and request.data['acceptorid'] != orderResponse.acceptedby_id:
                return JsonResponse({"error":"order can be completed by acceptor or placer only"}, status=status.HTTP_403_FORBIDDEN)

            if request.data['acceptorid']==None and request.data['placerid'] != orderResponse.orderedby_id:
                return JsonResponse({"error":"order can be completed by acceptor or placer only"}, status=status.HTTP_403_FORBIDDEN)     

            orderResponse.deliverytime = datetime.now()
            orderResponse.status = "completed"
            if request.data['acceptorid']!= None:
                orderResponse.completionconfirmedby_id = request.data['acceptorid']
            else:
                orderResponse.completionconfirmedby_id = request.data['placerid']

            orderResponse.save()

            userResponse = SnsUser.objects.get(id=orderResponse.acceptedby_id)
            walletAmount = userResponse.walletamount            
            userResponse.walletamount=walletAmount+ orderResponse.tipamount +orderResponse.orderamount
            userResponse.save()
            return JsonResponse({"success":"Order completed successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal server error occured in completing order"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)