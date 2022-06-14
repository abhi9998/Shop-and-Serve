
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

import time

def create_user(**kwargs):
    return get_user_model().objects.create_user(
        email=kwargs.get('email',"testusertocreateorder@sns.com"),
        password=kwargs.get('password',"DefTest@123"),
        name=kwargs.get('name',"Testuser store"),
        mobile=kwargs.get('mobile',"+1999999999"),
        address=kwargs.get('address',"Address default user"),
        city=kwargs.get('city',"Waterloo"),
        pincode=kwargs.get('pincode',"N2M 5H3"),
        is_staff= kwargs.get('is_staff', False)
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

def get_unique_group_details(id):
    random_string = str(int(time.time())) + str(id)
    data = dict()
    data['name'] = 'testgroup' + random_string
    data['description'] = 'Test Group ' + random_string
    data['city'] = 'Kitchener'
    return data

class OrderApiTest(TestCase):   

    def setUp(self):
        self.admin_user = create_user(name="Test Admin User for Order", email="admin@testorder.com", mobile="+1999999998", is_staff=True)
        self.admin = APIClient()
        self.admin.force_authenticate(user=self.admin_user)

        self.client_user = create_user(name="Test User for Order", email="user@testorder.com", mobile="+1999999999", is_staff=False)
        self.client = APIClient()
        self.client.force_authenticate(user=self.client_user)

        # Create store detail
        store_name = "Test store for create order"
        store_detail = get_new_store_detail(name=store_name)
        res = self.admin.post("/api/store/", store_detail)
        assert res.status_code == 201
        
        res = self.client.get("/api/store/info")
        for store in res.json():
            if store["name"] == store_name:
                self.storeid = store["id"]
                assert store['address'] == store_detail['address']
                assert store['city'] == store_detail['city']
                assert store['pincode'] == store_detail['pincode'] 

        # Create product detail
        product_detail = get_new_product_detail(name="Test create product", storeid=self.storeid)
        res = self.admin.post("/api/product/", product_detail)
        assert res.status_code == 201

        res = self.client.get(f"/api/product/info/store/{self.storeid}?status=active").json();
        
        for _product_detail in res:
            print(_product_detail)
            if _product_detail["name"] == product_detail["name"]:
                self.productid =  _product_detail["id"]

        print(self.client)
        # res = self.client.get("/user/myprofile")
        # print(res.json())

    def test_my_order_detail(self):
        # TODO: Block on finding ordered by id.
        pass
        # order_detail = get_new_order_detail(storeid=storeid, productid=productid)
        # product_detail = get_new_order_detail(name="Test create product", storeid=self.storeid)
        # res = self.client.post("/api/product/", product_detail)
        # assert res.status_code == 201