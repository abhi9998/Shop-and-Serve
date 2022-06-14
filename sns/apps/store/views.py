from django.http import JsonResponse
from sns.apps.product.models import Product
from .models import Store
from .serializers import StoreSerializer
from rest_framework.decorators import api_view
from rest_framework import status as status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_all_stores(request):

    try:
        param = request.GET.get('status','*')
        print("Param passed: " +param)

        if param=='inactive':
            storeResponse = Store.objects.filter(active='N')
        elif param=='active':
            storeResponse = Store.objects.filter(active='Y')
        else:
            storeResponse = Store.objects.all()

        storeResponseSerialized = StoreSerializer(storeResponse,many=True)

        return JsonResponse(storeResponseSerialized.data, status= status.HTTP_200_OK,safe=False)
    
    except Exception as e:
        return JsonResponse({"error":"internal error occurred for getting stores"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_store_by_id(request,storeid):

    try:
        
        storeDetailResponse = Store.objects.get(id=storeid,active='Y')
        storeDetailSerialized = StoreSerializer(storeDetailResponse)

        return JsonResponse(storeDetailSerialized.data,status=status.HTTP_200_OK,safe=False)

    except Store.DoesNotExist:
        return JsonResponse({"error":"Store not Found"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error":"internal error occurred for getting store"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)    


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_store_by_city(request,city):

    try:
        
        storeDetailResponse = Store.objects.filter(city=city,active='Y')
        storeDetailSerialized = StoreSerializer(storeDetailResponse, many=True)
        
        return JsonResponse(storeDetailSerialized.data,status=status.HTTP_200_OK,safe=False)
    
    except Store.DoesNotExist:
        return JsonResponse({"error":"Stores not Found"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error":"internal error occurred for getting stores"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)    



@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def add_store(request):
    
    try:
        deserializedStore = StoreSerializer(data=request.data)
        
        if deserializedStore.is_valid():
            deserializedStore.save()
        else:
            print(deserializedStore.errors)
            return JsonResponse({"error":"Incorrect data for post"},status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({"success":"Store added successfully"},status=status.HTTP_201_CREATED);        

    except Exception as e:        
        return JsonResponse({"error":"internal server error for posting store"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes((IsAuthenticated, IsAdminUser, ))
def update_status_of_store(request,storeid):

    try:
    
        param = request.GET.get('makestatus','*')
        
        storeInstance = Store.objects.get(id=storeid)
        
        
        if param=="active" and storeInstance.active =='N':    
            storeInstance.active = 'Y'
            storeInstance.save(update_fields=['active'])
            Product.objects.filter(storeid=storeid).update(active='Y')

        elif param=='inactive' and storeInstance.active=='Y':
            storeInstance.active = 'N'
            storeInstance.save(update_fields=['active'])
            Product.objects.filter(storeid=storeid).update(active='N')
        else:    
            return JsonResponse({"error":"incorrect data for put"},status=status.HTTP_400_BAD_REQUEST)
            

        return JsonResponse({"success":"status changed"},status=status.HTTP_204_NO_CONTENT);    

    except Exception as e:

        return JsonResponse({"error":"internal server error for updating store status"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

