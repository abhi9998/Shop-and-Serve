from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework import status as status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_all_products(request):
    
    try:
        productResponse = Product.objects.all()
        productResponseSerialized = ProductSerializer(productResponse,many=True)
    
        return JsonResponse(productResponseSerialized.data, status= status.HTTP_200_OK,safe=False)
    
    except Exception as e:

        return JsonResponse({"error":"internal error occured for getting products"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser, ))
def add_product(request):
    
    
    try:
        deserializedProduct = ProductSerializer(data=request.data)
        
        
        if deserializedProduct.is_valid():
            deserializedProduct.save()
            return JsonResponse({"success":"data added for post"},status=status.HTTP_201_CREATED)
        else:
            print(deserializedProduct.errors)
            return JsonResponse({"error":"Incorrect data for post"},status=status.HTTP_400_BAD_REQUEST);    

    except Exception as e:
        print(e)
        return JsonResponse({"error":"internal server error for posting product"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_products_by_store(request,storeid):

    try:
        param = request.GET.get('status','*')
        print(storeid)
        
        if param=='active':
            productDetailResponse = Product.objects.filter(storeid=storeid,active='Y')
            productDetailSerialized = ProductSerializer(productDetailResponse, many=True)
        elif param=='inactive':
            productDetailResponse = Product.objects.filter(storeid=storeid,active='N')
            productDetailSerialized = ProductSerializer(productDetailResponse, many=True)
        else:
            productDetailResponse = Product.objects.filter(storeid=storeid)
            productDetailSerialized = ProductSerializer(productDetailResponse, many=True)        

        return JsonResponse(productDetailSerialized.data,status=200,safe=False)
    
    except Product.DoesNotExist:
        return JsonResponse({"error":"Products not Found"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error":"internal error occured for getting products"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)    


@api_view(['PUT'])
@permission_classes((IsAuthenticated, IsAdminUser, ))
def update_status_of_product(request,productid):
    try:
    
        param = request.GET.get('makestatus','*')
        
        productInstance = Product.objects.get(id=productid)
        
        
        if param=="active" and productInstance.active =='N':    
            productInstance.active = 'Y'
            productInstance.save(update_fields=['active'])
            

        elif param=='inactive' and productInstance.active=='Y':
            productInstance.active = 'N'
            productInstance.save(update_fields=['active'])
            
        else:    
            return JsonResponse({"error":"incorrect data for put request"},status=status.HTTP_400_BAD_REQUEST)
            

        return JsonResponse({"success":"status changed"},status=status.HTTP_204_NO_CONTENT);    

    except Exception as e:

        return JsonResponse({"error":"internal server error for updating product status"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
