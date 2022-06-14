from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model



def create_user(**kwargs):
    return get_user_model().objects.create_user(
        email=kwargs.get('email',"testusertocreatestore@sns.com"),
        password=kwargs.get('password',"DefTest@123"),
        name=kwargs.get('name',"Testuser store"),
        mobile=kwargs.get('mobile',"+1999999999"),
        address=kwargs.get('address',"Address default user"),
        city=kwargs.get('city',"Waterloo"),
        pincode=kwargs.get('pincode',"N2M 5H3"),
        is_staff= kwargs.get('is_staff', True)
    )

def get_new_store_detail(**kwargs):
    return {
        "name": kwargs.get('name', 'Test store'),
        "address": kwargs.get('address', 'Test address at University'),
        "city": kwargs.get('city', 'Test City'),
        "pincode": kwargs.get('pincode', 'N2M5H3')
    }


class StoreApiTest(TestCase):
    
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_store(self):
        store_detail = get_new_store_detail(name="Test create store unique")
        res = self.client.post("/api/store/", store_detail)
        assert res.status_code == 201

    def test_get_all_store_detail(self):
        res = self.client.get("/api/store/info")
        assert len(res.json()) == 0
        
        store_detail = get_new_store_detail(name="Test create store")
        res = self.client.post("/api/store/", store_detail)
        assert res.status_code == 201
        
        res = self.client.get("/api/store/info")
        assert len(res.json()) == 1
        res = res.json()[0]
        assert res['name'] == store_detail['name']
        assert res['address'] == store_detail['address']
        assert res['city'] == store_detail['city']
        assert res['pincode'] == store_detail['pincode'] 

    def test_invalid_pincode(self):
        store_detail = get_new_store_detail(name="Test create store", pincode="N2M 5H3")
        res = self.client.post("/api/store/", store_detail)
        # Response should have 400 response code, as pincode is invalid.
        assert res.status_code == 400

    def test_missing_address(self):
        store_detail = {
            "name": "Test",
            "city": "Test city",
            "pincode": "Test pincode"
        }
        res = self.client.post("/api/store/", store_detail)
        # Response should have 400 response code, as address is missing.
        assert res.status_code == 400

    def test_missing_name(self):
        store_detail = {
            "address": "Test address",
            "city": "Test city",
            "pincode": "Test pincode"
        }
        res = self.client.post("/api/store/", store_detail)
        # Response should have 400 response code, as name is missing.
        assert res.status_code == 400

    def test_missing_city(self):
        store_detail = {
            "address": "Test address",
            "name": "Test store",
            "pincode": "Test pincode"
        }
        res = self.client.post("/api/store/", store_detail)
        # Response should have 400 response code, as city is missing.
        assert res.status_code == 400

    def test_store_retrieve(self):
        store_name = "Test update store"
        new_store_name = "New Test Update store name"

        store_detail = get_new_store_detail(name=store_name)
        res = self.client.post("/api/store/", store_detail)
        assert res.status_code == 201
        
        res = self.client.get("/api/store/info")
        for store in res.json():
            if store["name"] == store_name:
                assert store['address'] == store_detail['address']
                assert store['city'] == store_detail['city']
                assert store['pincode'] == store_detail['pincode'] 
        