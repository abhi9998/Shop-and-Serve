from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

def create_user(**kwargs):
    return get_user_model().objects.create_user(
        email=kwargs.get('email',"testusertocreateproduct@sns.com"),
        password=kwargs.get('password',"DefTest@123"),
        name=kwargs.get('name',"Testuser store"),
        mobile=kwargs.get('mobile',"+1999999999"),
        address=kwargs.get('address',"Address default user"),
        city=kwargs.get('city',"Waterloo"),
        pincode=kwargs.get('pincode',"N2M 5H3"),
        is_staff= kwargs.get('is_staff', True)
    )

def get_new_product_detail(**kwargs):
    return {
        "name": kwargs.get('name', 'Test product name'),
        "brand": kwargs.get('brand', 'Test product brand'),
        "imagelink": kwargs.get('imagelink', 'https://picsum.photos/200'),
        "description": kwargs.get('description', 'test product'),
        "price": kwargs.get('price', '15.0'),
        "weight": kwargs.get('weight', '200'),
        "storeid": kwargs.get('storeid', '1')
    }

def get_new_store_detail(**kwargs):
    return {
        "name": kwargs.get('name', 'Test store'),
        "address": kwargs.get('address', 'Test address at University'),
        "city": kwargs.get('city', 'Test City'),
        "pincode": kwargs.get('pincode', 'N2M5H3')
    }

class ProductApiTest(TestCase):
    
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        store_name = "Test create store"
        store_detail = get_new_store_detail(name=store_name)
        res = self.client.post("/api/store/", store_detail)
        assert res.status_code == 201
        
        res = self.client.get("/api/store/info")
        for store in res.json():
            if store["name"] == store_name:
                self.storeid = store["id"]
                assert store['address'] == store_detail['address']
                assert store['city'] == store_detail['city']
                assert store['pincode'] == store_detail['pincode'] 



    def test_create_product(self):
        product_detail = get_new_product_detail(name="Test create product", storeid=self.storeid)
        res = self.client.post("/api/product/", product_detail)
        assert res.status_code == 201

    def test_duplicate_product(self):
        product_detail = get_new_product_detail(name="Test create product duplicate", storeid=self.storeid)
        res = self.client.post("/api/product/", product_detail)
        assert res.status_code == 201

        product_detail = get_new_product_detail(name="Test create product duplicate", storeid=self.storeid)
        res = self.client.post("/api/product/", product_detail)
        assert res.status_code == 400
